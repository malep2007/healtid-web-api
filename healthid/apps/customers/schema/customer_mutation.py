import graphene
from graphql_jwt.decorators import login_required
from django.forms import model_to_dict
from healthid.apps.customers.schema.customer_schema import (
                                                        CustomerProfileType)
from healthid.apps.profiles.models import Profile
from healthid.utils.app_utils.database import (SaveContextManager,
                                               get_model_object)
from healthid.utils.customer_utils.create_customer_validation \
     import (validate_customer_fields)


class CreateCustomer(graphene.Mutation):
    """
    Creates a Customer


    Args:
        first_name (str) the customers first name
        last_name (str) the customers last name
        primary_mobile_number (str) the customers mobile number
        secondary_mobile_number (str) the customers mobile number 2
        email (email) the customers email
        address_line_1 (str) the customers address 1
        address_line_2 (str) the customers address 2
        local_government_area (str) the customers lga
        city_id (int) foreign key, city of the customer
        country_id (int) foreign key, country of the customer
        emergency_contact_name (Str) customer emergency contact name
        emergency_contact_number (Str) customer emergency contact mobile number
        emergency_contact_email (email) customer emergency contact email
        loyalty_member (bool)

    returns:
         success message and details of customer created if successful,
         otherwise a GraphqlError is raised
    """
    customer = graphene.Field(CustomerProfileType)
    message = graphene.String()

    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String()
        primary_mobile_number = graphene.String()
        secondary_mobile_number = graphene.String()
        email = graphene.String()
        address_line_1 = graphene.String()
        address_line_2 = graphene.String()
        local_government_area = graphene.String()
        city_id = graphene.Int(required=True)
        country_id = graphene.Int(required=True)
        emergency_contact_name = graphene.String()
        emergency_contact_number = graphene.String()
        emergency_contact_email = graphene.String()
        loyalty_member = graphene.Boolean(required=True)

    @login_required
    def mutate(self, info, **kwargs):
        customer = validate_customer_fields(Profile(), **kwargs)
        with SaveContextManager(customer, model=Profile) as customer:
            return CreateCustomer(
                message="Customer Created successfully",
                customer=customer)


class EditCustomerBasicProfile(graphene.Mutation):
    """
    Edits a Customer's basic profile

    Args:
        id (int) profile ID
        first_name (str) customer first name
        last_name (str)  customer last name
        primary_mobile_number (str) customer's primary number
        secondary_mobile_number (str) customer's secondary number
        email (email) customer's email
        address_line_1 (str) customer's address 1
        address_line_2 (str) customer's address 2
        local_government_area (str) customer's LGA
        city_id (int) customer's city
        country_id (int) customer's country
        emergency_contact_name (Str) customer's emergency contact's name
        emergency_contact_number (Str) customer's emergency contact's number
        emergency_contact_email (email) customer's emergency contact's email
        loyalty_member (bool)

    returns:
         success message and details of customer Edited if successful,
         otherwise GraphqlError instances are raised
    """
    customer = graphene.Field(CustomerProfileType)
    message = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)
        first_name = graphene.String()
        last_name = graphene.String()
        primary_mobile_number = graphene.String()
        secondary_mobile_number = graphene.String()
        email = graphene.String()
        address_line_1 = graphene.String()
        address_line_2 = graphene.String()
        local_government_area = graphene.String()
        city_id = graphene.Int()
        country_id = graphene.Int()
        emergency_contact_name = graphene.String()
        emergency_contact_number = graphene.String()
        emergency_contact_email = graphene.String()
        loyalty_member = graphene.Boolean()

    @login_required
    def mutate(self, info, id, **kwargs):
        customer = get_model_object(
            Profile, "id", id, message="Customer profile cannot be found")
        existing_fields = model_to_dict(customer)
        if "city_id" in kwargs:
            kwargs["city"] = kwargs.pop("city_id")
        if "country_id" in kwargs:
            kwargs["country"] = kwargs.pop("country_id")
        # add fields with changed values to new dictionary
        changed_fields = {
            key: kwargs.get(key)
            for key, value in existing_fields.items()
            if key in kwargs and value != kwargs.get(key)}
        if not changed_fields:
            return EditCustomerBasicProfile(
                message='Profile fields unchanged, nothing to edit',
                customer=customer)
        if "city" in changed_fields:
            changed_fields["city_id"] = changed_fields.pop("city")
        if "country" in changed_fields:
            changed_fields["country_id"] = changed_fields.pop("country")
        customer = validate_customer_fields(customer, **changed_fields)
        with SaveContextManager(customer, model=Profile) as customer:
            message = f"Successfully updated {customer.first_name}'s"\
                " basic profile"
            return EditCustomerBasicProfile(
                message=message,
                customer=customer)


class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    edit_customer_basic_profile = EditCustomerBasicProfile.Field()
