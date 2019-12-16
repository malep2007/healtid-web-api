import graphene
from graphql_jwt.decorators import login_required
from graphql import GraphQLError


from healthid.apps.sales.schema.types.sale import (
    SalesPromptType)
from healthid.utils.auth_utils.decorator import user_permission
from healthid.utils.messages.sales_responses import (SALES_ERROR_RESPONSES)
from healthid.apps.sales.models import (SalesPrompt)
from healthid.utils.app_utils.database import (SaveContextManager,
                                               get_model_object)
from healthid.apps.outlets.models import Outlet
from healthid.apps.products.models import Product
from healthid.utils.messages.common_responses import SUCCESS_RESPONSES


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
            raise GraphQLError(SALES_ERROR_RESPONSES["incomplete_list"])

        for title, description in zip(titles, prompt_descriptions):
            if title.strip() == "" or description.strip() == "":
                raise GraphQLError(SALES_ERROR_RESPONSES["title_error"])
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
            message=SUCCESS_RESPONSES[
                "creation_success"].format(
                "Sales prompt " + str(
                    sales_prompt_count)))
