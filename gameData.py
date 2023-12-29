import qrcode
from io import BytesIO
import base64

data = {
        "icon": "https://cdn-icons-png.flaticon.com/128/10693/10693535.png",
        "Words": ["Lisa", "Klaus", "Peter", "Marc"],
        "Opponent": ["Sport", "Chess", "Music"],
        "Exclude": ["AAA", "BBB", "CCC"]
    }

def generate_qr_code(data):
    img_qr = qrcode.make(data)
    buffered = BytesIO()
    img_qr.save(buffered, format="PNG")
    qr_code_base64 = base64.b64encode(buffered.getvalue()).decode()
    return qr_code_base64

# Generate a QR code for the register page
def generate_register_qr_code(serverURL):
    img = qrcode.make(serverURL+'/register')
    img.save("static/register_qr.png")



def replace_values(data, key, values):
    """
    This function replaces the values associated with the given key in the provided data dictionary.

    :param data: Dictionary representing the JSON structure.
    :param key: Key whose values need to be replaced.
    :param values: New values to be set for the given key.
    :return: Dictionary with updated values for the given key.
    """
    if key in data:
        data[key] = values
    else:
        print(f"{key} does not exist in the provided data.")
    return data

def delete_key(data, key):
    """
    This function deletes the specified key from the provided data dictionary.

    :param data: Dictionary representing the JSON structure.
    :param key: Key to be deleted.
    :return: Dictionary without the deleted key.
    """
    if key in data:
        data.pop(key)
    else:
        print(f"{key} does not exist in the provided data.")
    return data

def add_array(data, key, values):
    """
    This function adds a new array to the provided data dictionary.

    :param data: Dictionary representing the JSON structure.
    :param key: Key for the new array to be added.
    :param values: List of values to be set for the new key.
    :return: Dictionary with the new key-value pair added.
    """
    if key in data:
        print(f"{key} already exists in the provided data. Overwriting the existing values.")
    data[key] = values
    return data

