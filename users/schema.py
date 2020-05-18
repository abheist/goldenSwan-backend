import json

import graphene
from django.contrib.auth import get_user_model
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from meup.models import Article
from meup.schema import ArticleType


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        exclude = ('password', 'article_set')

    articles = graphene.List(ArticleType)

    def resolve_articles(self, info):
        if info.context.user.is_anonymous or self != info.context.user:
            return Article.objects.filter(author=self, published=True)
        if self == info.context.user:
            return Article.objects.filter(author=self)


class Query(object):
    users = graphene.List(UserType)
    user = graphene.Field(UserType, username=graphene.String())
    me = graphene.Field(UserType)

    def resolve_users(self, info, **kwargs):
        return get_user_model().objects.all()

    def resolve_user(self, info, username, **kwargs):
        try:
            user = get_user_model().objects.get(username=username)
            if user.profile_pic:
                profile_pic = json.loads(user.profile_pic)
                public_id = profile_pic.get('public_id')
                user.profile_pic = public_id
            return user
        except Exception as e:
            print(e)
            return None

    @login_required
    def resolve_me(self, info, **kwargs):
        user = info.context.user
        return user


class UpdateUserMutation(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        pk = graphene.ID(required=True)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)
        username = graphene.String(required=False)
        email = graphene.String(required=False)
        dob = graphene.String(required=False)
        bio = graphene.String(required=False)
        facebook = graphene.String(required=False)
        twitter = graphene.String(required=False)
        instagram = graphene.String(required=False)
        linkedin = graphene.String(required=False)

    @classmethod
    @login_required
    def mutate(cls, root, info, **kwargs):
        try:
            user = get_user_model().objects.get(pk=kwargs['pk'])
            if user == info.context.user:
                user.first_name = kwargs['first_name']
                user.last_name = kwargs['last_name']
                user.username = kwargs['username']
                user.email = kwargs['email']
                user.bio = kwargs['bio']
                user.facebook = kwargs['facebook']
                user.instagram = kwargs['instagram']
                user.twitter = kwargs['twitter']
                user.linkedin = kwargs['linkedin']
                user.save()
                return UpdateUserMutation(user=user)
            else:
                raise Exception
        except Exception as e:
            print(e)


class Mutation(graphene.ObjectType):
    update_user = UpdateUserMutation.Field()
