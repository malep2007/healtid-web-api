import json

from django.test import Client, TestCase

from healthid.apps.authentication.models import User, Role
from healthid.apps.outlets.models import Outlet, OutletKind, Country, City
from healthid.apps.business.tests.utils import create_business
from healthid.tests.test_fixtures.authentication import login_user_query


class BaseConfiguration(TestCase):
    """
    Base configuration file for all tests.
    """
    @classmethod
    def setUpClass(cls):

        # We need to first run setUpClass function that we
        # inherited from TestCase.
        super(BaseConfiguration, cls).setUpClass()

        # Set up test client for all test classes
        # that will inherit from this class.
        cls.client = Client()

    @classmethod
    def query(cls, query: str = None):
        # Method to run all queries and mutations for tests.
        body = dict()
        body['query'] = query
        response = cls.client.post(
            '/healthid/', json.dumps(body), content_type='application/json')
        json_response = json.loads(response.content.decode())
        return json_response

    @classmethod
    def query_with_token(cls, access_token, query: str = None):
        # Method to run queries and mutations using a logged in user
        # with an authentication token
        body = dict()
        body['query'] = query
        http_auth = 'JWT {}'.format(access_token)
        url = '/healthid/'
        content_type = 'application/json'

        response = cls.client.post(
            url, json.dumps(body),
            HTTP_AUTHORIZATION=http_auth,
            content_type=content_type)
        json_response = json.loads(response.content.decode())
        return json_response

    def setUp(self):
        """
        Configurations to be made available before each
        individual test case inheriting from this class.
        """
        self.new_user = {
            "email": "john.doe@gmail.com",
            "mobile_number": "+256 770777777",
            "password": "Password123"
        }
        self.master_admin = {
            "email": "you@example.com",
            "mobile_number": "+256 770777797",
            "password": "Password123"
        }
        self.login_user = {
            "email": "john.doe@gmail.com",
            "password": "Password123"
        }
        self.login_master_admin = {
            "email": "you@example.com",
            "password": "Password123"
        }

        self.business = create_business()
        self.outlet_kind = self.create_outlet_kind()
        self.outlet = self.create_outlet()
        self.role = self.create_role(role_name="Cashier")

        # register and log in user
        self.register_user()
        self.access_token = self.user_login()
        self.register_master_admin()
        self.access_token_master = self.admin_login()

    def assertResponseNoErrors(self, resp: dict, expected: dict):
        self.assertNotIn("errors", resp, "Response had errors")
        self.assertEqual(resp["data"], expected, "Response has correct data")

    def register_user(self):
        """
        register a new user
        """
        email = self.new_user["email"]
        mobile_number = self.new_user["mobile_number"]
        password = self.new_user["password"]
        user = User.objects.create_user(email=email,
                                        mobile_number=mobile_number,
                                        password=password)
        user.is_active = True
        user.save()

    def register_master_admin(self):
        """
        register a master admin
        """
        email = self.master_admin["email"]
        mobile_number = self.master_admin["mobile_number"]
        password = self.master_admin["password"]
        user = User.objects.create_user(email=email,
                                        mobile_number=mobile_number,
                                        password=password)
        user.is_active = True
        user.role = Role.objects.create(name='Master Admin')
        user.save()

    def user_login(self):
        """
        Log in registered user and return a token
        """
        response = self.query(login_user_query.format(**self.login_user))
        return response['data']['tokenAuth']['token']

    def admin_login(self):
        """
        Log in registered user and return a token
        """
        response = self.query(
            login_user_query.format(**self.login_master_admin))
        return response['data']['tokenAuth']['token']

    def create_outlet_kind(self):
        country = Country.objects.create(name='Peru')
        city = City.objects.create(name="Chiclayo", country_id=country.id)
        outlet_kind = OutletKind.objects.create(name="Warehouse")
        info = {"city_id": city.id, "outlet_kindid": outlet_kind.id}
        return info

    def create_outlet(self):
        info = self.outlet_kind
        return Outlet.objects.create(
            name="bingo", kind_id=info["outlet_kindid"],
            address_line1="wandegya", phone_number="254745345342",
            address_line2="Central, Kla", lga="KCCA",
            city_id=info["city_id"], date_launched="1995-10-20",
            business_id=self.business.id)

    def create_role(self, role_name):
        return Role.objects.create(
            name=role_name
        )
