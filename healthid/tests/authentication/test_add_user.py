from healthid.tests.base_config import BaseConfiguration
from healthid.tests.test_fixtures.authentication import \
    add_user_query


class TestAddUser(BaseConfiguration):
    """
    Testing Adding user by the Master Admin
    """

    def test_add_user(self):
        """
        test user creation
        """
        email = 'test@gmail.com'
        mobile_number = '+256 754434487'
        user_data = {
            'email': email,
            'mobileNumber': mobile_number,
            'outletId': self.outlet.id,
            'roleId': self.role.id

        }
        resp = self.query_with_token(
            self.access_token_master, add_user_query.format(**user_data))
        self.assertIn('data', resp)
        self.assertEqual(resp['data']['addUser']['errors'], None)
        self.assertEqual(resp['data']['addUser']
                         ['user']['email'], email)
        self.assertEqual(resp['data']['addUser']
                         ['user']['mobileNumber'], mobile_number)

    def test_wrong_email(self):
        """
        test wrong email
        """
        email = 'test@gmail'
        mobile_number = '+256 754434487'
        user_data = {
            'email': email,
            'mobileNumber': mobile_number,
            'outletId': self.outlet.id,
            'roleId': self.role.id
        }

        resp = self.query_with_token(
            self.access_token_master, add_user_query.format(**user_data))
        self.assertIn("Please input a valid email",
                      resp['errors'][0]['message'])

    def test_wrong_mobile_number(self):
        """
        test wrong mobile_number
        """
        email = 'test@gmail.com'
        mobile_number = '+256 754434487aer'
        user_data = {
            'email': email,
            'mobileNumber': mobile_number,
            'outletId': self.outlet.id,
            'roleId': self.role.id

        }

        resp = self.query_with_token(
            self.access_token_master, add_user_query.format(**user_data))
        self.assertIn("Please input a valid mobile number",
                      resp['errors'][0]['message'])

    def test_existing_email(self):
        # test if the email already exists
        email = 'john.doe@gmail.com'
        mobile_number = '+256 754434487'
        user_data = {
            'email': email,
            'mobileNumber': mobile_number,
            'outletId': self.outlet.id,
            'roleId': self.role.id

        }
        resp = self.query_with_token(
            self.access_token_master, add_user_query.format(**user_data))
        self.assertEqual(resp['data']['addUser']
                         ['errors'], ['Something went wrong: User with email '
                                      'john.doe@gmail.com already exists'])
