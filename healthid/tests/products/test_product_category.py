from healthid.tests.base_config import BaseConfiguration
from healthid.tests.test_fixtures.products import (create_product_category)
from healthid.utils.messages.common_responses import\
     SUCCESS_RESPONSES, ERROR_RESPONSES


class TestProductCategory(BaseConfiguration):
    """
    class handles tests for product category
    """

    def test_create_product_category(self):
        """
        test product category creation
        """
        response = self.query_with_token(
            self.access_token_master,
            # create_product_category.format(outlet_id=self.outlet.id)
            create_product_category.format(business_id=self.business.id)
        )
        self.assertIn(SUCCESS_RESPONSES[
                      "creation_success"].format("Product Category"),
                      "".join(response['data'][
                                       'createProductCategory']['message']))
        self.assertIn('data', response)
        self.assertNotIn('errors', response)

    def test_duplicate_product_categopry(self):
        """
        test product category creation
        """
        self.query_with_token(
            self.access_token_master,
            create_product_category.format(business_id=self.business.id)
        )
        duplicate_category = self.query_with_token(
            self.access_token_master,
            create_product_category.format(business_id=self.business.id)
        )
        self.assertIn(ERROR_RESPONSES[
                      "duplication_error"
                      ].format("ProductCategory with name panadol"),
                      duplicate_category['errors'][0]['message'])
        self.assertIn('errors', duplicate_category)
