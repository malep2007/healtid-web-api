from healthid.tests.base_config import BaseConfiguration
from healthid.tests.test_fixtures.customers import (create_customer)


class TestCustomerCreation(BaseConfiguration):
    def test_create_customer(self):
        """Test method for creating a customer"""
        response = self.query_with_token(
            self.access_token,
            create_customer.format(**self.create_customer_data))
        expected_message = "Customer Created successfully"
        self.assertEqual(
            expected_message,
            response["data"]["createCustomer"]["message"])
        self.assertNotIn("errors", response)

    def test_create_customer_invalid_firstname(self):
        """Test method for creating a customer with invalid firstname"""
        self.create_customer_data['first_name'] = "H@#@qwer"
        response = self.query_with_token(
            self.access_token,
            create_customer.format(**self.create_customer_data))
        expected_message = "special characters not allowed"
        self.assertEqual(
            expected_message,
            response['errors'][0]['message'])

    def test_create_customer_invalid_email(self):
        """Test method for creating a customer with invalid email"""
        self.create_customer_data['email'] = "talktohabibgmail.com"
        response = self.query_with_token(
            self.access_token,
            create_customer.format(**self.create_customer_data))
        expected_message = "Please input a valid email"
        self.assertEqual(
            expected_message,
            response['errors'][0]['message'])

    def test_create_customer_firstname_as_empty_string(self):
        """Test method for creating a customer with invalid firstname"""
        self.create_customer_data['first_name'] = ""
        response = self.query_with_token(
            self.access_token,
            create_customer.format(**self.create_customer_data))
        expected_message = "first_name can't be an empty String"
        self.assertEqual(
            expected_message,
            response['errors'][0]['message'])

    def test_create_customer_mobileNumber_as_empty_string(self):
        """Test method for creating a customer with invalid mobileNumber"""
        self.create_customer_data['primary_mobile_number'] = "23456"
        response = self.query_with_token(
            self.access_token,
            create_customer.format(**self.create_customer_data))
        self.assertEqual(
            "Mobile number must have a 9-15 digits (ex. +2346787646)",
            response['errors'][0]['message'])
