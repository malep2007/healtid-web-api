import csv
from rest_framework.exceptions import ValidationError

from healthid.utils.messages.common_responses import ERROR_RESPONSES


def validate_products_csv_upload(io_string):
    """
        Validate products info from an appropriately formatted CSV file.

        arguments:
            io_string(obj): 'io.StringIO' object containing a list
                            of products in CSV format

        returns:
            array: a list of products
        """
    [row_count, csv_columns, products, csv_errors] = [0, [], [], {}]
    valid_columns = {
        'name': 'required',
        'description': 'required',
        'brand': 'required',
        'manufacturer': 'required',
        'dispensing size': 'required',
        'preferred supplier': 'required',
        'backup supplier': 'required',
        'category': 'required',
        'loyalty weight': 'not required',
        'vat status': 'not required',
        'tags': 'not required',
        'product image': 'not required',
    }
    for row in csv.reader(io_string):
        csv_columns = list(map(lambda column: column.lower().strip(), row))
        break

    for column in csv_columns:
        csv_errors = {
            **csv_errors,
            'columns': [
                *(csv_errors.get('column') or []),
                ERROR_RESPONSES['not_allowed_field'].format(column)
            ]
        } if column.lower().strip() not in valid_columns else csv_errors

    for row in csv.reader(io_string):
        row_count += 1
        [i, product, row_errors] = [0, {}, []]
        while i < len(row):
            if valid_columns.get(csv_columns[i]) == 'required' and not row[i]:
                row_errors = [
                    *row_errors,
                    ERROR_RESPONSES['required_field'].format(csv_columns[i])
                ]

            product = {
                **product,
                csv_columns[i]: row[i]
            } if csv_columns[i] else product

            i += 1

        csv_errors = {
            **csv_errors,
            f'row-{row_count}': row_errors
        } if len(row_errors) else csv_errors

        products = [*products, product]

    if len(csv_columns) < 10 or len(csv_columns) > 12:
        message = {
            'error': 'csv file missing column(s)'
            if len(csv_columns) < 10 else 'csv file has more column(s)'
        }
        raise ValidationError(message)

    if len(csv_errors):
        raise ValidationError(csv_errors)

    return products
