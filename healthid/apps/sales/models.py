from django.db import models
from django.db.models import Sum
from django.db.models.signals import pre_save

from healthid.apps.authentication.models import User
from healthid.apps.outlets.models import Outlet
from healthid.apps.products.models import Product
from healthid.apps.profiles.models import Profile
from healthid.models import BaseModel
from healthid.utils.app_utils.database import (SaveContextManager,
                                               get_model_object)
from healthid.utils.app_utils.id_generator import id_gen
from healthid.utils.sales_utils.initiate_sale import initiate_sale
from healthid.utils.sales_utils.validate_sale import SalesValidator


class PromotionType(BaseModel):
    id = models.CharField(max_length=9, primary_key=True,
                          default=id_gen, editable=False)
    name = models.CharField(max_length=140, unique=True)

    def __str__(self):
        return self.name


class Promotion(BaseModel):
    id = models.CharField(max_length=9, primary_key=True,
                          default=id_gen, editable=False)
    title = models.CharField(max_length=140, unique=True)
    promotion_type = models.ForeignKey(PromotionType, on_delete=models.CASCADE)
    description = models.TextField()
    products = models.ManyToManyField(Product, blank=True)
    discount = models.DecimalField(decimal_places=2, max_digits=10)
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class SalesPrompt(BaseModel):
    prompt_title = models.CharField(max_length=244, unique=True)
    description = models.CharField(
        max_length=244, default="Sales prompt descripttion:")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE)

    def __str__(self):
        return self.prompt_title


class Cart(models.Model):
    '''
    defines cart model.

    args:
        user: owner of the cart.
        items: products along with the quantity and their total that
               have been added to the cart
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('CartItem')

    @property
    def total(self):
        '''
        method that calculates the total price of all the items in cart
        '''
        return self.items.all().aggregate(Sum('item_total'))['item_total__sum']


class CartItem(models.Model):
    '''
    defines cart item model

    args:
        product: product to be added to cart
        quantity: amount of product to be added to cart
        item_total: price of the product based on the quantity
    '''
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    item_total = models.DecimalField(default=0.00,
                                     max_digits=10,
                                     decimal_places=2)

    def __str__(self):
        return str(self.id)


def update_item_total(**kwargs):
    """
    function that calculates the price of product being added to cart
    based on the quantity being added, this is triggered before a cart
    item is saved
    """
    cart_item = kwargs.get('instance')
    cart_item.item_total = \
        cart_item.product.pre_tax_retail_price * cart_item.quantity


pre_save.connect(update_item_total, sender=CartItem)


class Sale(BaseModel):
    """
    Defines sale model

    Attributes:
            sales_person: Holds employee who made the transaction
            outlet: Holds outlet referencing id.
            customer: Holds a customer who bought the drugs if provided..
            sub_total: Holds the total minus discount.
            amount_to_pay = Holds the total amount including discounts.
            paid_cash  = Holds the paid cash amount
            change_due = Holds the remaining balance
            payment_method: Holds payment method e.g. cash/cash
            notes: Holds note about the sale
    """
    sales_person = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sold_by')
    customer = models.ForeignKey(
        Profile,  on_delete=models.CASCADE, null=True)

    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE)
    amount_to_pay = models.DecimalField(max_digits=12, decimal_places=2)
    discount_total = models.DecimalField(max_digits=12, decimal_places=2)
    sub_total = models.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2)
    change_due = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=35, default="cash")
    notes = models.TextField(blank=True, null=True)

    def _validate_sales_details(self, **kwargs):
        """
        This method handles all validations related to sale fields

        Arguments:
            kwargs: information about sale
        """
        sold_products = kwargs.get('products')
        sales_validator = SalesValidator(sold_products)
        sales_validator.check_sales_fields_validity(**kwargs)
        sales_validator.check_validity_of_ids()
        sales_validator.check_product_discount()
        sales_validator.check_product_price()
        sold_product_instances = sales_validator.check_validity_quantity_sold()
        return sold_product_instances

    def create_sale(self, info, **kwargs):
        """
        This method create a sale after it has been validated
        by _validate_sales_details()

        Arguments:
            kwargs: information about sale
            info: information about the logged in user
        """
        sales_person = info.context.user

        customer_id = kwargs.get('customer_id')
        outlet_id = kwargs.get('outlet_id')
        sold_products = kwargs.get('products')
        discount_total = kwargs.get('discount_total')
        sub_total = kwargs.get('sub_total')
        amount_to_pay = kwargs.get('amount_to_pay')
        paid_amount = kwargs.get('paid_amount')
        payment_method = kwargs.get('payment_method')
        change_due = kwargs.get('change_due')
        notes = kwargs.get('notes')

        outlet = get_model_object(Outlet, "id", outlet_id)

        sold_product_instances = Sale._validate_sales_details(self, **kwargs)

        sale = Sale(sales_person=sales_person,
                    outlet=outlet,
                    payment_method=payment_method,
                    discount_total=discount_total,
                    sub_total=sub_total,
                    amount_to_pay=amount_to_pay,
                    paid_amount=paid_amount,
                    change_due=change_due,
                    notes=notes)

        with SaveContextManager(sale) as sale:
            if customer_id:
                customer = get_model_object(Profile, "id", customer_id)
                sale.customer = customer
                sale.save()
            initiate_sale(sold_product_instances,
                          sold_products, sale, SaleDetail)
        return sale


class SaleDetail(BaseModel):
    """
    Defines sale detail model

    Attributes:
        product: Holds a reference to products to be sold
        sale:  Holds a sale reference to this product
        quantity:  Holds the quantity to be sold of a product
        price: Holds the price for each product
        note: Holds note about the product
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    discount = models.FloatField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    note = models.TextField(blank=True, null=True)
