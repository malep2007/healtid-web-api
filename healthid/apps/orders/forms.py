from django import forms

from graphql.error import GraphQLError

from healthid.apps.outlets.models import Outlet
from healthid.apps.orders.models import Order
from healthid.apps.products.models import BatchInfo, Product
from healthid.apps.preference.models import OutletPreference

from healthid.utils.app_utils.database import get_model_object


class BarcodeScanForm(forms.Form):
    """Clean and sanitise user input data.

    Validate the types, and format of the input data.

    Args:
        scanned_number (str): The number scanned from the barcode
        batch_id (str): The batch id
        order_id (int): The order id
        product_id (int): The product id
        outlet_id (int): The business outlet id

    Raises:
        ValidationError: if any of the fields does not meet validation
        criteria.

        GraphQLError: if instances do not have the correct relationships.

    """
    scanned_number = forms.CharField(max_length=100, min_length=1,
                                     required=True)
    batch_id = forms.CharField(max_length=100, min_length=1,
                               required=True)
    order_id = forms.IntegerField(required=True)
    product_id = forms.IntegerField(required=True)
    outlet_id = forms.IntegerField(required=True)
    count = forms.IntegerField(min_value=1)

    def clean_scanned_number(self):
        """Check whether the scanned number is as expected.

        Returns:
            scanned_number (str)

        Raises:
            ValidationError: if the scanned_number is not twelve digits
            and cannot be transformed into an integer.
        """
        scanned_number = self.cleaned_data['scanned_number']

        validation_exception = GraphQLError(f"{scanned_number} is not"
                                            " a valid Barcode number")

        if len(scanned_number) != 12:
            raise validation_exception

        try:
            int(scanned_number)
        except ValueError:
            raise validation_exception

        return scanned_number

    def clean(self):
        """Check the validity of input fields.

        Make sure the order, product and batch_Info referenced are all
        valid and have the correct relations to one another.

        Returns:
            cleaned_data (dict)
        """
        cleaned_data = super().clean()

        order = get_model_object(Order, 'id',
                                 cleaned_data['order_id'])
        product = get_model_object(Product, 'id', cleaned_data['product_id'])
        batch_info = get_model_object(BatchInfo, 'id',
                                      cleaned_data['batch_id'])
        outlet = get_model_object(Outlet, 'id', cleaned_data['outlet_id'])
        preference = get_model_object(OutletPreference, 'outlet_id', outlet.id)

        if not preference.barcode_preference:
            raise GraphQLError("Barcode scanning is disabled")

        if not order.closed:
            raise GraphQLError("Scan rejected: this order"
                               " is not marked closed.")

        if batch_info not in outlet.outlet_batches.all():
            raise GraphQLError("Scan rejected: BatchInfo does"
                               " not match the provided outlet")

        if product not in batch_info.product.all():
            raise GraphQLError("Scan rejected: Product does"
                               " not match the provided BatchInfo")

        return cleaned_data
