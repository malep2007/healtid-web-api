from graphql import GraphQLError


class ValidateProduct:
    """Class to validate product and batch fields
    """

    def validate_batch(self, **kwargs):
        """Method to validate batch fields when reconciling an order
        """
        if not kwargs['supplier_id'] or kwargs['supplier_id'].isspace():
            raise GraphQLError('Supplier ID is required!')
        if not kwargs['product'] and not kwargs['quantities']:
            raise GraphQLError('Product and Quantity are required!')
        if not kwargs['unit_cost']:
            raise GraphQLError('Unit cost is required!')


validate = ValidateProduct()
