import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from healthid.apps.outlets.models import Outlet
from healthid.apps.products.models import Product
from healthid.apps.sales.models import Sale, SalesPrompt
from healthid.apps.sales.schema.sales_schema import SalesPromptType, SaleType
from healthid.utils.app_utils.database import (SaveContextManager,
                                               get_model_object)
from healthid.utils.auth_utils.decorator import user_permission


class CreateSalesPrompts(graphene.Mutation):
    """
    This Creates a Sales Prompt for a group of products particular Product
    """
    sales_prompts = graphene.List(SalesPromptType)
    message = graphene.String()

    class Arguments:
        prompt_titles = graphene.List(graphene.String, required=True)
        descriptions = graphene.List(graphene.String, required=True)
        product_ids = graphene.List(graphene.Int, required=True)
        outlet_ids = graphene.List(graphene.Int, required=True)

    @login_required
    @user_permission('Manager')
    def mutate(self, info, **kwargs):
        product_ids = kwargs.get('product_ids')
        titles = kwargs.get('prompt_titles')
        prompt_descriptions = kwargs.get('descriptions')
        outlet_ids = kwargs.get('outlet_ids')
        sales_prompt_count = 0
        valid_list = all(len(product_ids) == len(list_inputs)
                         for list_inputs in
                         [titles, prompt_descriptions, outlet_ids])

        if not valid_list or len(product_ids) < 1:

            raise GraphQLError('List inputs are incomplete or empty')

        for title, description in zip(titles, prompt_descriptions):
            if title.strip() == "" or description.strip() == "":
                raise GraphQLError("Titles and discription must contain words")
        created_prompts = []
        for index, title in enumerate(titles, 0):

            params = {'model': SalesPrompt}
            sales_prompt = SalesPrompt(
                prompt_title=title.title(),
                description=prompt_descriptions[index],
                product_id=get_model_object(Product, 'id',
                                            product_ids[index]).id,
                outlet_id=get_model_object(Outlet, 'id',
                                           outlet_ids[index]).id)

            with SaveContextManager(sales_prompt, **params) as sales_prompt:
                created_prompts.append(sales_prompt)
                sales_prompt_count += 1

        return CreateSalesPrompts(
            sales_prompts=created_prompts,
            message=f'Successfully created {sales_prompt_count} sales prompt')


class UpdateSalesPrompt(graphene.Mutation):
    """
    This Updates a Sales prompt
    """
    success = graphene.String()
    salesPrompt = graphene.Field(SalesPromptType)

    class Arguments:
        id = graphene.Int(required=True)
        prompt_title = graphene.String()
        description = graphene.String()
        product_id = graphene.Int()
        outlet_id = graphene.Int()

    @login_required
    @user_permission('Manager')
    def mutate(self, info, id, **kwargs):
        salesPrompt = get_model_object(SalesPrompt, 'id', id)
        for key, value in kwargs.items():
            if key in ["prompt_title", "description"]:
                if value.strip() == "":
                    raise GraphQLError(
                        "Titles or discription must contain words")
            setattr(salesPrompt, key, value)
        params = {'model': SalesPrompt}
        with SaveContextManager(salesPrompt, **params) as salesPrompt:
            return UpdateSalesPrompt(
                success='Sales prompt was updated successfully',
                salesPrompt=salesPrompt)


class DeleteSalesPrompt(graphene.Mutation):
    """
    This deletes a Sales prompt
    """
    id = graphene.Int()
    success = graphene.String()

    class Arguments:
        id = graphene.Int()

    @login_required
    @user_permission('Manager')
    def mutate(self, info, id):
        user = info.context.user
        prompt = get_model_object(SalesPrompt, 'id', id)
        prompt.delete(user)
        return DeleteSalesPrompt(
            success="Sales Prompt was deleted successfully")


class Products(graphene.InputObjectType):
    """
    This class defines necessary fields of a product to be sold
    """
    product_id = graphene.Int()
    quantity = graphene.Int()
    discount = graphene.Float()
    price = graphene.Float()
    note = graphene.String()


class CreateSale(graphene.Mutation):
    """
    Create a sale
    """
    sale = graphene.Field(SaleType)
    message = graphene.String()
    error = graphene.String()

    class Arguments:
        customer_id = graphene.String()
        outlet_id = graphene.Int(required=True)
        products = graphene.List(Products, required=True)
        discount_total = graphene.Float(graphene.Float, required=True)
        sub_total = graphene.Float(graphene.Float, required=True)
        amount_to_pay = graphene.Float(graphene.Float, required=True)
        paid_amount = graphene.Float(graphene.Float, required=True)
        change_due = graphene.Float(graphene.Float, required=True)
        payment_method = graphene.String(graphene.String, required=True)
        notes = graphene.String()

    @login_required
    def mutate(self, info, **kwargs):
        new_sale = Sale()
        sale = new_sale.create_sale(info=info, **kwargs)
        return CreateSale(sale=sale,
                          message='Sale was created successfully')


class Mutation(graphene.ObjectType):
    create_salesprompts = CreateSalesPrompts.Field()
    delete_salesprompt = DeleteSalesPrompt.Field()
    update_salesprompt = UpdateSalesPrompt.Field()
    create_sale = CreateSale.Field()
