""" Contains business logic for calculating sales velocity."""
from graphql import GraphQLError

from healthid.apps.products.models import Product


class SalesVelocity():
    """docstring for SalesVelocity"""
    def __init__(self, product_name, *weekly_sales, minimum_weeks=2, reorder_point=10, reorder_max=70):
        super(SalesVelocity, self).__init__()
        self.product_name = product_name
        self.weekly_sales = weekly_sales
        self.minimum_weeks = minimum_weeks
        self.total_sales = sum(weekly_sales)
        self.reorder_max = reorder_max
        self.reorder_point = reorder_point
        
    def velocity_calculator(self):
        """
        Calculates sales velocity
        Args:
            product_name (str)
            minimum_weeks (int) How many weeks of data are needed to 
                populate the sales velocity
            weekly_sales (array) A list containing integers representing 
                sales per week
        Returns:
             sales_velocity(float) if calculation is successful or 
             a GraphQLError is the number of weekly sales provided 
             are less than the minimum_weeks
        """
        weeks_count = len(self.weekly_sales)

        #If this error is raised, make sure to return the default sales velocity provided by the user
        if weeks_count < self.minimum_weeks:
            raise GraphQLError('Not enough data to populate sales velocity')

        sales_velocity = round(self.total_sales/weeks_count, 2)

        return sales_velocity


    def inventory_check(self):
        """
        Checks whether current inventory can last till reorder point.
        Args:
            product_name (str)
            weekly_sales (array) A list containing integers representing 
                sales per week
        Returns:
            A dictionary object containing -
                1. reorder (Boolean) Whether new inventory needs to be 
                    ordered
                2. remaining_stock (int) Current inventory levels
                3. time_to_depletion (float) How many weeks left before 
                    current inventory is depleted based on current 
                    sales velocity. 
                4. time_to_reorder (float) How many weeks before a reorder 
                    is necessary based on preset reorder point.
                5. quantity_to_reorder (int) Amount of inventory that should 
                    be reordered based on preset maximum inventory that can be 
                    held(reorder_max). 
        """
        product_instance = Product.objects.get(product_name=self.product_name)
        reorder_point = product_instance.reorder_point

        if reorder_point == 0:
            reorder_point = self.reorder_point

        remaining_stock = product_instance.quantity

        sales_velocity = self.velocity_calculator()

        time_to_depletion = round(remaining_stock/sales_velocity, 1)
        time_to_reorder = round(time_to_depletion - reorder_point, 1)

        if time_to_reorder <= 2:
            reorder = True
            quantity_to_reorder = self.reorder_max - remaining_stock
        else:
            reorder = False
            quantity_to_reorder = None

        return ({
            'reorder': reorder,
            'remaining_stock': remaining_stock,
            'time_to_depletion': time_to_depletion,
            'time_to_reorder': time_to_reorder,
            'quantity_to_reorder': quantity_to_reorder,
            })
