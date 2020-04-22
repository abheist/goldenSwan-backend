import graphene
from django.contrib.auth import get_user_model
from graphene_django.types import DjangoObjectType
from graphene_file_upload.scalars import Upload
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


class UpdateUserMutation(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        pk = graphene.ID(required=True)
        # username = graphene.String(required=False)
        first_name = graphene.String(required=False)
        # last_name = graphene.String(required=False)
        # email = graphene.String(required=False)
        # dob = graphene.String(required=False)
        # bio = graphene.String(required=False)
        profile_pic = Upload()

    @classmethod
    @login_required
    def mutate(cls, root, info, pk, first_name, profile_pic):
        try:
            user = get_user_model().objects.get(pk=pk)
            if user.username == info.context.user.username:
                # todo: change user models fields
                user.first_name = first_name
                user.profile_pic = profile_pic
                user.save()
                return UpdateUserMutation(user=user)
            else:
                raise Exception
        except Exception as e:
            print(e)


class Mutation(graphene.ObjectType):
    update_user = UpdateUserMutation.Field()
