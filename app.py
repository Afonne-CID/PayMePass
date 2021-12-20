import json
import shortuuid
from validate_nigerian_phone import NigerianPhone
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

def valid_number(input):
    """ Validates `input` phone number
    """
    if (NigerianPhone(input).is_valid()):
        return str(NigerianPhone(input).get_network()).lower()
    else:
        return "invalid phone"

def get_result(form):
    """Process input and generates result for user
    """
    result = []
    ticket = str(shortuuid.uuid()[:8])
    phone = str(request.form['msg'])
    gift = ""
    network = valid_number(phone)
    result.append("Ticket for: " + phone + ' (' + network + ')')

    registered_users = reload("registered_users.json")
    if (network == "invalid phone"):
            result.append("invalid phone")

    elif ((network not in registered_users.keys()
            or registered_users == {})):
        registered_users[network] = {}
        registered_users[network][ticket] = [phone, gift]
        result.append(ticket)
        save(registered_users)
        phone_num(registered_users)

    elif ((network in registered_users.keys()
            and ticket not in registered_users[network].keys())):
        registered_users[network][ticket] = [phone, gift]
        result.append(ticket)
        save(registered_users)
        phone_num(registered_users)
        
    else:
        for each in registered_users[network].keys():
            user = registered_users[network][each]
            if phone == user[0]:
                result.append(each)

    return result

def save(a_dict):
    """Serializes a_dict to a file
    """
    with open("registered_users.json", "w") as f:
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