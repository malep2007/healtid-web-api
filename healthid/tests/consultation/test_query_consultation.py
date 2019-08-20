from faker import Faker
from healthid.tests.base_config import BaseConfiguration

from healthid.tests.test_fixtures.consultations import (
    retrieve_consultations)
from healthid.tests.test_fixtures.consultations import (
    retrieve_consultation)
from healthid.tests.factories import (
    ConsultationItemFactory, CustomerFactory, CustomerConsultationFactory,
    OutletFactory)

fake = Faker()


class TestQueryConsultation(BaseConfiguration):
    def setUp(self):
        super(TestQueryConsultation, self).setUp()
        self.consultation_item = ConsultationItemFactory(
            consultation_name=fake.word(),
            description=fake.text(max_nb_chars=50),
            consultant_role="Pharmacist",
            approved_delivery_formats=["Telephonic"],
            outlet_id=self.outlet.id,
            minutes_per_session=fake.random_int(min=1, max=60),
            price_per_session=fake.random_int()
        )
        self.new_outlet = OutletFactory(name=fake.word())
        self.customer_2 = CustomerFactory()
        self.customer_consultation = CustomerConsultationFactory(
            customer=self.customer_2)

    def test_user_can_retrieve_consultations(self):
        response = self.query_with_token(
            self.access_token, retrieve_consultations)
        self.assertEqual(
            response['data']['consultations'][0]['id'],
            str(self.consultation_item.id))

    def test_user_queries_from_a_different_outlet(self):
        self.consultation_item2 = ConsultationItemFactory(
            consultation_name=fake.word(),
            description=fake.text(max_nb_chars=50),
            consultant_role="Pharmacist",
            approved_delivery_formats=["Telephonic"],
            outlet_id=self.new_outlet.id,
            minutes_per_session=fake.random_int(min=1, max=60),
            price_per_session=fake.random_int()
        )
        response = self.query_with_token(
            self.access_token, retrieve_consultation.format(
                consultation_id=self.consultation_item2.id))
        self.assertEqual(response['errors'][0]['message'],
                         'Consultation doesnot belong in your outlet')

    def test_consultation_id_doesnot_exist(self):
        response = self.query_with_token(
            self.access_token, retrieve_consultation.format(
                consultation_id=0))
        self.assertEqual(response['errors'][0]['message'],
                         'Consultation id should be a positive number.')
