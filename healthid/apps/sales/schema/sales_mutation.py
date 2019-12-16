import graphene

from healthid.apps.sales.schema.mutations.sales_mutations\
    .create_sales_prompts import CreateSalesPrompts
from healthid.apps.sales.schema.mutations.sales_mutations\
    .update_sales_prompt import UpdateSalesPrompt
from healthid.apps.sales.schema.mutations.sales_mutations\
    .delete_sales_prompt import DeleteSalesPrompt
from healthid.apps.sales.schema.mutations.sales_mutations\
    .create_sale import CreateSale
from healthid.apps.sales.schema.mutations.sales_mutations\
    .consultation_payment import ConsultationPayment
from healthid.apps.sales.schema.mutations.sales_mutations\
    .initiate_sale_return import InitiateSaleReturn
from healthid.apps.sales.schema.mutations.sales_mutations\
    .approve_sale_return import ApproveSalesReturn


class Mutation(graphene.ObjectType):
    create_salesprompts = CreateSalesPrompts.Field()
    delete_salesprompt = DeleteSalesPrompt.Field()
    update_salesprompt = UpdateSalesPrompt.Field()
    create_sale = CreateSale.Field()
    consultation_payment = ConsultationPayment.Field()
    initiate_sales_return = InitiateSaleReturn.Field()
    approve_sales_return = ApproveSalesReturn.Field()
