import graphene
from django.contrib.auth import get_user_model
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        exclude = ('password', 'email')


class Query(object):
    users = graphene.List(UserType)
    user = graphene.Field(UserType, user_id=graphene.ID())
    me = graphene.Field(UserType)

    @login_required
    def resolve_users(self, info, **kwargs):
        return get_user_model().objects.all()

    @login_required
    def resolve_user(self, info, user_id, **kwargs):
        return get_user_model().objects.get(pk=user_id)

    @login_required
    def resolve_me(self, info, **kwargs):
        user = info.context.user
        return user
