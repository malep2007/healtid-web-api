import graphene
from graphql_jwt.decorators import login_required

from healthid.apps.sales.models import (SalesPrompt)
from healthid.utils.auth_utils.decorator import user_permission
from healthid.utils.app_utils.database import (get_model_object)
from healthid.utils.messages.common_responses import SUCCESS_RESPONSES


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
            success=SUCCESS_RESPONSES[
                "deletion_success"].format("Sales prompt"))
