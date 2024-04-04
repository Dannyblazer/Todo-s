import graphene
from graphene_django import DjangoObjectType
from blog.models import BlogPost

class BlogPostType(DjangoObjectType):
    class Meta:
        model = BlogPost
        fields = ("id", "title", "subTitle", "dateCreated")


class Query(graphene.ObjectType):
    """all_blogposts = graphene.List(BlogPostType)
    blogpost_by_title = graphene.Field()"""
    blogs = graphene.String()

    def resolve_blogs():
        return "This is a test blog"


schema = graphene.Schema(query=Query)
