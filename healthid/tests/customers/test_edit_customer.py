from healthid.tests.base_config import BaseConfiguration
from healthid.tests.test_fixtures.customers import edit_customer_basic_profile


class TestCustomerProfileEdit(BaseConfiguration):
    def test_no_edit(self):
        """Test method for unchanged profile fields"""

        response = self.query_with_token(
            self.access_token, edit_customer_basic_profile(
                self.customer_fields_to_dict(self.customer_1)))

        message = response["data"]["editCustomerBasicProfile"]["message"]
        expected_message = "Profile fields unchanged, nothing to edit"

        self.assertEqual(expected_message, message)

    def test_profile_edit_with_invalid_email(self):
        """Test method for a profile edit with invalid email"""
        customer_data = self.customer_fields_to_dict(self.customer_1)
        customer_data["email"] = "invalid email"

        response = self.query_with_token(
            self.access_token, edit_customer_basic_profile(customer_data))

        message = response["errors"][0]["message"]
        expected_message = "Please input a valid email"

        self.assertEqual(expected_message, message)
        self.assertEqual(None, response["data"]["editCustomerBasicProfile"])

    def test_profile_edit_with_invalid_name(self):
        """Test method for a profile edit with invalid first name"""
        customer_data = self.customer_fields_to_dict(self.customer_1)
        customer_data["first_name"] = ""

        response = self.query_with_token(
            self.access_token, edit_customer_basic_profile(customer_data))

        message = response["errors"][0]["message"]
        expected_message = "first_name can't be an empty String"

        self.assertEqual(expected_message, message)
        self.assertEqual(None, response["data"]["editCustomerBasicProfile"])

    def test_profile_edit_with_invalid_mobileNumber(self):
        """Test method for a profile edit with invalid primary mobile number"""
        customer_data = self.customer_fields_to_dict(self.customer_1)
        customer_data['primary_mobile_number'] = "23456"

        response = self.query_with_token(
            self.access_token, edit_customer_basic_profile(customer_data))

        message = response["errors"][0]["message"]

        self.assertEqual(
            "Mobile number must have a 9-15 digits (ex. +2346787646)", message)
        self.assertEqual(None, response["data"]["editCustomerBasicProfile"])

    def test_profile_edit_with_valid_data(self):
        """Test method for a valid profile edit"""
        customer_data = self.customer_fields_to_dict(self.customer_1)
        customer_data["first_name"] = "Rollo"
        customer_data["lastName"] = "Ragnar"
        customer_data["email"] = "people@vikings.mail"
        customer_data["loyaltyMember"] = "false"

        first_name = customer_data["first_name"]

        response = self.query_with_token(
            self.access_token, edit_customer_basic_profile(customer_data))
        response_data = response["data"]["editCustomerBasicProfile"]

        message = response_data["message"]
        expected_message = f"Successfully updated {first_name}'s" \
            " basic profile"

        self.assertEqual(expected_message, message)
        self.assertEqual(
            customer_data["first_name"],
            response_data["customer"]["firstName"])
        self.assertEqual(
            customer_data["email"],
            response_data["customer"]["email"])
        self.assertNotIn("errors", response)
