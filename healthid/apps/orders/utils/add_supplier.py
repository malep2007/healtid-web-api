import csv
from graphql.error import GraphQLError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound, ValidationError
from healthid.apps.orders.models import Suppliers, Tier, PaymentTerms
from healthid.apps.outlets.models import City


class AddSupplier:

    def __init__(self):
        self.exclude_list = [
            'DoesNotExist',
            '_meta',
            'MultipleObjectsReturned',
            'city',
            'tier',
            'payment_terms']
        self.safe_list = [
            each for each in Suppliers.__dict__ if not
            each.startswith('__') and each not in
            self.exclude_list
            ]

    @staticmethod
    def create_supplier(instance, input):
        try:
            email = Suppliers.objects.get(email=input.email)
            if email:
                raise GraphQLError(
                    "Supplier with email {} already exists".format(
                        input.email))
        except ObjectDoesNotExist:
            for (key, value) in input.items():
                setattr(instance, key, value)
            instance.save()

    def handle_csv_upload(self, io_string):
        for column in csv.reader(io_string, delimiter=','):
            dict_object = dict(zip(self.safe_list, column))
            instance = Suppliers()
            for (key, value) in dict_object.items():
                if key == 'email':
                    self.catch_duplicate_email(value)
                if key == 'rating':
                    value = int(value)
                if key == 'city_id':
                    value = self.get_model_instance_id(
                        City, value.title(), 'city')
                if key == 'tier_id':
                    value = self.get_model_instance_id(
                        Tier, value.lower(), 'tier')
                if key == 'payment_terms_id':
                    value = self.get_model_instance_id(
                        PaymentTerms, value.lower(), 'payment term')
                setattr(instance, key, value)
            instance.save()

    def get_model_instance_id(self, model, name, description):
        try:
            model_object = model.objects.get(name=name)
            return model_object.id
        except ObjectDoesNotExist:
            message = {"error": f"{description} {name} doesnot exist"}
            raise NotFound(message)

    def catch_duplicate_email(self, email):
        try:
            supplier = Suppliers.objects.get(email=email)
            if supplier:
                message = {
                    "error": f"supplier with email {supplier.email} " +
                    "already exists"
                    }
                raise ValidationError(message)
        except ObjectDoesNotExist:
            return email


add_supplier = AddSupplier()