import unittest
from web_app import app


class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)  # Good request
        expected_response = {'message': 'Hello, world!'}
        self.assertEqual(expected_response, response.get_json())

    def test_country_code(self):
        response = self.app.get('/v1/phone-numbers?phoneNumber=%2B15756210000')
        self.assertEqual(response.status_code, 200)  # Good request
        expected_response = {'countryCode': 'US'}
        self.assertTrue(expected_response.items() <= response.get_json().items())

        response = self.app.get('/v1/phone-numbers?phoneNumber=1%20575%206210000')
        self.assertEqual(response.status_code, 200)  # Good request
        expected_response = {'countryCode': 'US'}
        self.assertTrue(expected_response.items() <= response.get_json().items())

        response = self.app.get('/v1/phone-numbers?phoneNumber=%2B1%20575%206210000')
        self.assertEqual(response.status_code, 200)  # Good request
        expected_response = {'countryCode': 'US'}
        self.assertTrue(expected_response.items() <= response.get_json().items())

        response = self.app.get('/v1/phone-numbers?phoneNumber=1%20575%206210000&countryCode=CA')
        self.assertEqual(response.status_code, 200)  # Good request
        expected_response = {'countryCode': 'CA'}
        self.assertTrue(expected_response.items() <= response.get_json().items())

    def test_area_code(self):
        response = self.app.get('/v1/phone-numbers?phoneNumber=%2B15756210000')
        self.assertEqual(response.status_code, 200)  # Good request
        expected_response = {'areaCode': '575'}
        self.assertTrue(expected_response.items() <= response.get_json().items())

        response = self.app.get('/v1/phone-numbers?phoneNumber=1%20575%206210000')
        self.assertEqual(response.status_code, 200)  # Good request
        expected_response = {'areaCode': '575'}
        self.assertTrue(expected_response.items() <= response.get_json().items())

        response = self.app.get('/v1/phone-numbers?phoneNumber=1%20575%206210000&countryCode=CA')
        self.assertEqual(response.status_code, 200)  # Good request
        expected_response = {'areaCode': '575'}
        self.assertTrue(expected_response.items() <= response.get_json().items())

    def test_missing_country_code(self):
        response = self.app.get('/v1/phone-numbers?phoneNumber=6313118150')
        self.assertEqual(response.status_code, 200)
        expected_error = {
            "countryCode": "required value is missing"
        }
        self.assertTrue(expected_error.items() <= response.get_json().get("error", {}).items())

    def test_invalid_country_code(self):
        response = self.app.get('/v1/phone-numbers?phoneNumber=%2B28313118150')
        self.assertEqual(response.status_code, 200)
        expected_error = {
            "countryCode": "invalid"
        }
        self.assertTrue(expected_error.items() <= response.get_json().get("error", {}).items())

        response = self.app.get('/v1/phone-numbers?phoneNumber=28 313118150')
        self.assertEqual(response.status_code, 200)
        expected_error = {
            "countryCode": "invalid"
        }
        self.assertTrue(expected_error.items() <= response.get_json().get("error", {}).items())

    def test_missing_country_code_with_parameter(self):
        response = self.app.get('/v1/phone-numbers?phoneNumber=6313118150?countryCode=GB')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("countryCode", response.get_json().get("error", {}))

        response = self.app.get('/v1/phone-numbers?phoneNumber=34%20915%20872200')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("countryCode", response.get_json().get("error", {}))

        response = self.app.get('/v1/phone-numbers?phoneNumber=6313118150&countryCode=VL')
        self.assertEqual(response.status_code, 200)
        expected_error = {
            "countryCode": "invalid"
        }
        self.assertTrue(expected_error.items() <= response.get_json().get("error", {}).items())

    def test_missing_area_code(self):
        response = self.app.get('/v1/phone-numbers?phoneNumber=%2B157')
        self.assertEqual(response.status_code, 200)
        expected_error = {
            "areaCode": "missing"
        }
        self.assertTrue(expected_error.items() <= response.get_json().get("error", {}).items())

    def test_missing_local_phone_numer(self):
        response = self.app.get('/v1/phone-numbers?phoneNumber=%2B1575')
        self.assertEqual(response.status_code, 200)
        expected_error = {
            "localPhoneNumber": "missing"
        }
        self.assertTrue(expected_error.items() <= response.get_json().get("error", {}).items())

    def test_invalid_characters(self):
        response = self.app.get('/v1/phone-numbers?phoneNumber=631311%8150?countryCode=GB')
        self.assertEqual(response.status_code, 200)
        expected_error = {
            "characters": "invalid"
        }
        # Check if an entry is inside another dict. Alternative to the deprecated assertDictContainsSubset
        self.assertTrue(expected_error.items() <= response.get_json().get("error", {}).items())

    def test_space(self):
        response = self.app.get('/v1/phone-numbers?phoneNumber=%2B12125690123')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("space", response.get_json().get('error', {}))

        response = self.app.get('/v1/phone-numbers?phoneNumber=%2B52%20631%203118150')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("space", response.get_json().get('error', {}))

        response = self.app.get('/v1/phone-numbers?phoneNumber=34%20915%20872200')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("space", response.get_json().get('error', {}))

        response = self.app.get('/v1/phone-numbers?phoneNumber=351%2021%20094%202000')
        self.assertEqual(response.status_code, 200)
        expected_error = {
            "space": "invalid"
        }
        self.assertTrue(expected_error.items() <= response.get_json().get('error', {}).items())

        response = self.app.get('/v1/phone-numbers?phoneNumber=%20+12125690123')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(expected_error.items() <= response.get_json().get('error', {}).items())

        response = self.app.get('/v1/phone-numbers?phoneNumber=%2B12125690123%20')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(expected_error.items() <= response.get_json().get('error', {}).items())

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
