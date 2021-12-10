from types import NoneType
import shortuuid
import datetime
import json
from flask import Flask, request, render_template, url_for

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    """Renders the index.html, and returns a modified page
    with the ticket number if exists, or appropriate msg
    if not"""
    output_for_user = False
    input_from_user = False
    if request.method == 'POST':
        form = request.form
        output = get_result(form)
        input_from_user = str(output[0])
        output_for_user = str(output[1])

    if output_for_user == "Invalid purchase code":
        return render_template('index.html', output_for_user=output_for_user)
    return render_template('index.html', output_for_user=output_for_user, input_from_user=input_from_user)

def get_result(form):
    result = []
    input = request.form['msg']
    result.append("Ticket for: " + input)

    luck_bags = reload("file.json")

    if (input not in luck_bags.keys()):
        error_msg = "Invalid purchase code"
        result.append(error_msg)
    else:
        result.append(luck_bags[input])

    return result

def process():
    """Loads previous (if exists) or/and generates
    key/value pairs and save into `file.json`
    """
    date_value = datetime.date.today()
    post_yr = date_value.strftime("%Y")[-2:]
    month_str = date_value.strftime("%b")

    luck_bag = reload("file.json")

    for i in range(101):
        id = shortuuid.uuid()
        value = id[:8]
        key = str(post_yr) + (str(month_str)
             + str(id[-4:])).upper()

        if ((key not in luck_bag.keys())
            and (value not in luck_bag.values())):
            luck_bag[key] = value

    save(luck_bag)

def save(a_dict):
    """Serializes a_dict to a file
    """
    splited = str(a_dict.keys()).split(',')
    purchase_codes = '\n'.join(splited)
    with open("Purcahse_codes", "w") as f:
        f.write(purchase_codes)

    with open("file.json", "w") as f:
        json.dump(a_dict, f, indent=6)

def reload(file):
    """Deserializes the JSON file a_dict if it exists,
    or do nothing if doesn't exist
    """
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {}

# total days in every month during non leap years
M_DAYS = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def isleap(year):
    """Return True for leap years, False for non-leap years."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def days_in_month(year, month):
    """Returns total number of days in a month accounting for leap years."""
    return M_DAYS[month] + (month == 2 and isleap(year))

def is_monthend(ref_date):
    """Checks whether a date is also a monthend"""
    return ref_date.day == days_in_month(ref_date.year, ref_date.month)


if __name__ == '__main__':
    app.run(debug=False, host="127.0.0.1", port="5500")