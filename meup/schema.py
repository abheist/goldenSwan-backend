import graphene
from graphene_django import DjangoObjectType
from graphql_auth.decorators import login_required

from meup.models import Article


class ArticleType(DjangoObjectType):
    class Meta:
        model = Article


class Query(object):
    articles = graphene.List(ArticleType)
    article = graphene.Field(ArticleType, id=graphene.String())

    def resolve_articles(self, info, **kwargs):
        return Article.objects.all()

    def resolve_article(self, info, **kwargs):
        id = kwargs.get('id')
        return Article.objects.get(id=id)


class CreateArticleMutation(graphene.Mutation):
    article = graphene.Field(ArticleType)

    class Arguments:
        title = graphene.String()
        content = graphene.String()

    @classmethod
    @login_required
    def mutate(cls, root, info, title, content):
        if info.context.user:
            article = Article(title=title, content=content, author=info.context.user)
            article.save()
            return CreateArticleMutation(article=article)
        else:
            raise Exception


class UpdateArticleMutation(graphene.Mutation):
    article = graphene.Field(ArticleType)

    class Arguments:
        id = graphene.String(required=True)
        title = graphene.String()
        content = graphene.String()

    @classmethod
    @login_required
    def mutate(cls, root, info, title, content, id):
        article = Article.objects.get(pk=id)
        if article.author == info.context.user:
            article.title = title
            article.content = content
            article.save()
            return UpdateArticleMutation(article)
        else:
            raise Exception


class Mutation(graphene.ObjectType):
    create_article = CreateArticleMutation.Field()
    update_article = UpdateArticleMutation.Field()
