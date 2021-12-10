import shortuuid
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

    return render_template('index.html', output_for_user=output_for_user, input_from_user=input_from_user)

def get_result(form):
    """Process input and generates result for user
    """
    result = []
    input = str(request.form['msg'])
    result.append("Ticket for: " + input)
    
    value = shortuuid.uuid()[:8]
    key = input

    luck_bag = reload("luck_bag.json")
    if (key not in luck_bag.keys()):
        luck_bag[key] = value
        result.append(value)
        save(luck_bag)
        phone_num(luck_bag)
    else:
        result.append(luck_bag[key])

    return result

def save(a_dict):
    """Serializes a_dict to a file
    """
    with open("luck_bag.json", "w") as f:
        json.dump(a_dict, f, indent=6)

def reload(file):
    """Deserializes the JSON file `file` if it exists,
    or do nothing if doesn't
    """
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {}

def phone_num(a_dict):
    """Generates all available phone numbers
    """
    raw = str(a_dict.keys()).split(',')
    phones = '\n'.join(raw)
    with open("Phone Nos.txt", "w") as f:
        f.write(phones)

if __name__ == '__main__':
    app.run(debug=False, host="127.0.0.1", port="5500")