# Flask App

## Installation and Execution Instruction

### Introduction
This is a simple Flask app that parses a telephone number from a GET request.

### Installation
1. Create a virtual environment: `python3 -m venv venv`
2. Activate the virtual environment:
   - For Windows: `venv\Scripts\activate`
   - For macOS/Linux: `source venv/bin/activate`
3. Install the required dependencies: `pip install -r requirements.txt` 

### Run the application on local machine
1. Run the Flask app: `python web_app.py`


### Make a GET request
1. Visit `http://127.0.0.1:5000` for the homepage
2. Visit `http://127.0.0.1:5000/v1/phone-numbers?phoneNumber=1234567890` to parse the phone number `1234567890`
3. Visit `http://127.0.0.1:5000/v1/phone-numbers?phoneNumber=1234567890&countryCode=CA` to parse the phone number `1234567890` and country `CA`

### File Structure
Run unit test:`python3 unit_tests.py`.

### File Structure
- `web_app`: The main Flask application file.
- `unit_tests.py`: The unit test file for the Flask app.
- `requirements.txt`: File listing the required Python packages.

## Programming Language and Framework

Flask is a very popular framework for creating a simple web application, and Python is very popular programming language. That is why I used Flask and Python for this assignment.

In this application, I used the Python library `phonenumbers` because this library has many good features and data for country phone code in digit and in ISO 3166-1 alpha-2 formats.

## Deployment

One free lightweight for deployment an Flask app on cloud is `PythonAnywhere` ([https://www.pythonanywhere.com](https://www.pythonanywhere.com))

Try following the instruction from: [https://help.pythonanywhere.com/pages/Flask/](https://help.pythonanywhere.com/pages/Flask/)

For example, this Flask app has been deployed to: [http://khoihd.pythonanywhere.com](http://khoihd.pythonanywhere.com)

## Assumptions

In this application, I made a few assumptions:

1. If a phone number starts with the plus sign `+` (encoded as `%2B`), then it starts with the country code. For example, the phone number `%2B12345678901` (or `+12345678901`) has country code `1` for country `US`.

2. If a number has some space (encoded as `%20`), then the first group of number is the country code. For example, `1%20234%205678901` (or `1 234 5678901`) has country code `1` for country `US`.

3. If a given country code has potential multiple countries, then `countryCode` parameter will be used if they match. For example, if `+1` is the country code and `countryCode=CA`, then the country is `CA`. If the `countryCode` is not provided or not matched, then the first country from the list `phonenumbers.COUNTRY_CODE_TO_REGION_CODE` will be used.

4. Only those countries in `NANP` have area code. I also assume the area code always has 3 digits.

## Potential Improvements

1. Make `countryCode` a required parameter instead of an optional parameter. We will ask user not to include the country code in their phone number. This can prevent the case where different countries share the same country phone code, and this can also make the implementation simpler and less prone to bugs.

2. Have the option to make a `POST` request and submit the information as a form. We can allow users to choose their country from a list instead of manually inputting `countryCode` as ISO 3166-1 alpha-2 format because regular users might not be familiar with this format.

