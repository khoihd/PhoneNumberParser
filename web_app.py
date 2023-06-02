from flask import Flask, jsonify, request
from phonenumbers import COUNTRY_CODE_TO_REGION_CODE, SUPPORTED_REGIONS
from phonenumbers.phonenumberutil import is_nanpa_country

app = Flask(__name__)

SPACE = " "
PLUS_SIGN = "+"
AREA_CODE_LENGTH = 3


@app.route('/', methods=['GET'])
def hello():
    return jsonify(message='Hello, world!')


def get_initial_error(phone_number):
    error_msg = {}

    # Check for invalid characters
    clean_phone_number = phone_number
    if phone_number.startswith(PLUS_SIGN):
        clean_phone_number = phone_number.replace(PLUS_SIGN, "", 1)

    if not clean_phone_number.replace(SPACE, "").isdigit():
        error_msg["characters"] = "invalid"

    # Check for leading or trailing space
    if phone_number.startswith(SPACE) or phone_number.endswith(SPACE):
        error_msg["space"] = "invalid"
        phone_number = phone_number.strip()

    # Check if having more than 3 group of numbers
    split_numbers = phone_number.split(SPACE)
    split_numbers = [e for e in split_numbers if e != '']
    if len(split_numbers) > 3:
        error_msg["space"] = "invalid"

    return error_msg


def get_country_code(phone_number_parameter, country_code_parameter):
    result, error = {}, {}
    phone_number = phone_number_parameter
    # If the phone number has PLUS_SIGN, then parse the country code and check for error
    phone_country_code = -1
    if phone_number_parameter.startswith(PLUS_SIGN):
        phone_number = phone_number_parameter.replace(PLUS_SIGN, "", 1)  # delete the first occurrence of PLUS_SIGN
        if int(phone_number[0]) in COUNTRY_CODE_TO_REGION_CODE:
            country_code_length = 1
        elif int(phone_number[:2]) in COUNTRY_CODE_TO_REGION_CODE:
            country_code_length = 2
        elif int(phone_number[:3]) in COUNTRY_CODE_TO_REGION_CODE:
            country_code_length = 3
        else:
            error["countryCode"] = "invalid"
            return result, error, phone_number_parameter

        phone_country_code = int(phone_number[:country_code_length])
        phone_number = phone_number[country_code_length:]
        phone_number = phone_number.lstrip()  # space could appear after +country_code
    # No leading PLUS SIGN, but has SPACE in between
    # Leading and trailing spaces have been handled earlier
    elif SPACE in phone_number_parameter:
        split_phone_number = phone_number_parameter.split(SPACE)

        phone_country_code = int(split_phone_number[0])
        if phone_country_code not in COUNTRY_CODE_TO_REGION_CODE:
            error["countryCode"] = "invalid"
            return result, error, phone_number_parameter
        phone_number = " ".join(split_phone_number[1:])

    if phone_country_code == -1:
        if not country_code_parameter:
            error["countryCode"] = "required value is missing"
            return result, error, phone_number_parameter
        else:
            if country_code_parameter in SUPPORTED_REGIONS:
                result['countryCode'] = country_code_parameter
            else:
                error["countryCode"] = "invalid"
                return result, error, phone_number_parameter
    else:
        # If there are multiple countries for the same code, then get the country code from parameter if matched
        # Otherwise, just get the first country
        if country_code_parameter in COUNTRY_CODE_TO_REGION_CODE[phone_country_code]:
            result['countryCode'] = country_code_parameter
        else:
            result['countryCode'] = COUNTRY_CODE_TO_REGION_CODE[phone_country_code][0]

    return result, error, phone_number


def get_area_code(phone_number, country_code):
    result, error = {}, {}
    if is_nanpa_country(country_code):
        if SPACE in country_code:
            area_code = country_code.split(SPACE)[0]
            phone_number = country_code.replace(area_code, "").replace(SPACE, "")
            result['areaCode'] = area_code
            result['localPhoneNumber'] = phone_number
        else:
            area_code = phone_number[:AREA_CODE_LENGTH]
            phone_number = phone_number[AREA_CODE_LENGTH:]
            if len(area_code) < AREA_CODE_LENGTH:
                error = {"areaCode": "missing"}
                return None, error
            if not phone_number:
                error = {"localPhoneNumber": "missing"}
                return None, error

            result['areaCode'] = area_code
            result['localPhoneNumber'] = phone_number
    else:
        result['areaCode'] = ""
        result['localPhoneNumber'] = phone_number

    return result, None


# [+][country code][area code][local phone number]
# + is optional = '%2B'
# Assumption: Country code is identified by PLUS_SIGN or by spacing
# If potential multiple country codes, then get the country code from the country_code argument
def parse_phone_number(phone_number_parameter, country_code_parameter):
    result_msg = {}

    phone_error_msg = get_initial_error(phone_number_parameter)
    if phone_error_msg:
        error_msg = {"phoneNumber": phone_number_parameter, 'error': phone_error_msg}
        return error_msg

    country_code_result_msg, country_code_error_msg, phone_number = get_country_code(phone_number_parameter,
                                                                                     country_code_parameter)
    result_msg.update(country_code_result_msg)
    if country_code_error_msg:
        error_msg = {"phoneNumber": phone_number_parameter, 'error': country_code_error_msg}
        return error_msg

    area_code_result_msg, area_code_error_msg = get_area_code(phone_number, country_code_result_msg['countryCode'])
    if area_code_error_msg:
        error_msg = {"phoneNumber": phone_number_parameter, 'error': area_code_error_msg}
        return error_msg

    result_msg.update(area_code_result_msg)

    return result_msg


@app.route('/v1/phone-numbers', methods=['GET'])
def get_phone_number_info():
    phone_number = request.args.get('phoneNumber')
    country_code_parameter = request.args.get('countryCode')

    result = parse_phone_number(phone_number, country_code_parameter)

    return jsonify(result)


if __name__ == '__main__':
    app.run()
