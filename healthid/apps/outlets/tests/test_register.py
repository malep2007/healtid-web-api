from django.test import Client, TestCase
from healthid.apps.authentication.models import User, Role
from healthid.apps.business.tests.utils import create_business
from healthid.apps.outlets.models import City, Country, Outlet, OutletKind, Register, Receipt

import json


class GraphQLTestCase(TestCase):
    """
    Testing the role functions
    """

    def create_default_role(self):
        return Role.objects.create(name="Master Admin")

    def setUp(self):
        self._client = Client()
        self.user = User.objects.create_user(
            email="mymail@gmail.com", password="mypassword123"
        )
        self.user.role = self.create_default_role()
        self.user.is_active = True
        self.user.save()
        self._client.login(email="mymail@gmail.com", password="mypassword123")



    def query(self, query: str):
        body = {"query": query}
        resp = self._client.post(
            "/healthid/", json.dumps(body), content_type="application/json"
        )
        jresp = json.loads(resp.content.decode())
        return jresp

    def assertResponseNoErrors(self, resp: dict, expected: dict):
        self.assertNotIn("errors", resp, "Response had errors")
        self.assertEqual(resp["data"], expected, "Response has correct data")

    def create_city(self):
        country = Country.objects.create(name='Uganda')
        city = City.objects.create(name="Kampala", country_id=country.id)
        outlet_kind = OutletKind.objects.create(name="Warehouse")
        info = {"city_id": city.id, "outlet_kindid": outlet_kind.id}
        return info

    def create_outlet(self):
        info = self.create_city()
        business = create_business()
        return Outlet.objects.create(
            name="bingo", kind_id=info["outlet_kindid"],
            address_line1="wandegya", phone_number="254745345342",
            address_line2="Central, Kla", lga="KCCA",
            city_id=info["city_id"], date_launched="1995-10-20",
            business_id=business.id)

    def make_user_masteradmin(self):
        self.user.role = self.create_default_role()
        self.user.save()
        self._client.login(email='mymail@gmail.com', password='mypassword123')

    def create_receipt(self):
        return Receipt.objects.create(
            cashier="Habib",
            discount = 2345,
            subtotal = 2000,
            tax = 3000,
            amount_to_pay = 30400,
            purchase_total = 40000,
            change_due = 50000,
            loyal = 500)

    def create_register(self):
        outlet = self.create_outlet()
        receipt = self.create_receipt()
        return Register.objects.create(
            name="liver moore",
            outlet_id = outlet.id,
            receipt_id = receipt.id)

    def test_create_register(self):
        outlet = self.create_outlet()
        receipt = self.create_receipt()
        response = self.query(
            (f'''
                    mutation{{
                        createRegister(
                 name: "liver moore"
                 outletId:{outlet.id},
                 receiptId:\"{receipt.id}\",)
                   {{
                    register{{id name}}
                }}
            }}
            '''),
        )
        self.assertResponseNoErrors(
            response, {"createRegister": {
                'register': {'id': '1', 'name': 'liver moore'}
            }})

    def test_update_register(self):
        """ Update name to 'ever moore' """

        register = self.create_register()
        response = self.query((f'''
            mutation updateRegister {{
               updateRegister (id:{register.id}, input:{{
                  name: "ever moore"
              }}) {{
                success
                  register {{
                    name
                  }}
                
              }}
            }}
            
           '''),)

        self.assertResponseNoErrors(
            response, {"updateRegister": {"success": True, 'register': {'name': 'ever moore'}}})


    def test_delete_register(self):

        """ Delete register a given ID"""

        register = self.create_register()
        response = self.query(
            f'mutation{{deleteRegister(id: {register.id}){{success}}}}')
        self.assertIn("success", response["data"]["deleteRegister"])


