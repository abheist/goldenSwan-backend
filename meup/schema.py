import graphene
from graphene_django import DjangoObjectType
from graphql_auth.decorators import login_required

from meup.models import Article


class ArticleType(DjangoObjectType):
    class Meta:
        model = Article


class Query(object):
    articles = graphene.List(ArticleType)
    article = graphene.Field(ArticleType, slug=graphene.String())

    def resolve_articles(self, info, **kwargs):
        return Article.objects.all()

    def resolve_article(self, info, **kwargs):
        slug = kwargs.get('slug')
        return Article.objects.get(slug=slug)


class CreateArticleMutation(graphene.Mutation):
    article = graphene.Field(ArticleType)

    class Arguments:
        title = graphene.String()
        subtitle = graphene.String()
        content = graphene.String()

    @classmethod
    @login_required
    def mutate(cls, root, info, title, subtitle, content):
        if info.context.user:
            article = Article(title=title, subtitle=subtitle, content=content, author=info.context.user)
            article.save()
            return CreateArticleMutation(article=article)
        else:
            raise Exception


class UpdateArticleMutation(graphene.Mutation):
    article = graphene.Field(ArticleType)

    class Arguments:
        slug = graphene.String(required=True)
        title = graphene.String()
        subtitle = graphene.String()
        content = graphene.String()
        published = graphene.Boolean(required=False)

    @classmethod
    @login_required
    def mutate(cls, root, info, slug, title, subtitle, content, published):
        try:
            article = Article.objects.get(slug=slug)
            if article.author == info.context.user:
                article.title = title
                article.subtitle = subtitle
                article.content = content
                article.published = published

                article.save()
                return UpdateArticleMutation(article=article)
            else:
                raise Exception
        except Exception as e:
            print(e)


class Mutation(graphene.ObjectType):
    create_article = CreateArticleMutation.Field()
    update_article = UpdateArticleMutation.Field()
