import graphene
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql import GraphQLError
from .models import BlogPost
from .forms import BlogPostForm
from users.models import Account as User

# Define GraphQL types for User and BlogPost models

class UserType(DjangoObjectType):
    """GraphQL type for the User model."""
    class Meta:
        model = User
        fields = ('id', 'username')

class BlogPostType(DjangoObjectType):
    """GraphQL type for the BlogPost model."""
    class Meta:
        model = BlogPost
        fields = ('id', 'title', 'subTitle', 'body', 'dateCreated', 'author')
        # Add prefetch_related to prefetch author's data to avoid N+1 queries
        prefetch_related = ('author',)

# Define queries

class Query(graphene.ObjectType):
    """Root query for retrieving data."""
    all_blog_posts = graphene.List(BlogPostType, description="Retrieve all blog posts.")

    def resolve_all_blog_posts(self, info):
        """Resolver function for retrieving all blog posts."""
        # Add select_related to fetch author data in one query
        return BlogPost.objects.select_related('author').all()

# Define mutations

class CreateBlogPost(graphene.Mutation):
    """Mutations for creating a new blog post."""
    class Arguments:
        title = graphene.String()
        subtitle = graphene.String()
        body = graphene.String()

    blog_post = graphene.Field(BlogPostType)

    def mutate(self, info, title, subtitle, body):
        """Mutate function for creating a new blog post."""
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError('You must be logged in to create a blog post.')
        blog_post = BlogPost(title=title, subTitle=subtitle, body=body, author=user)
        blog_post.save()
        return CreateBlogPost(blog_post=blog_post)

class UpdateBlogPost(DjangoModelFormMutation):
    """Mutation for updating an existing blog post."""
    class Meta:
        form_class = BlogPostForm
        input_field_name = 'input'  # Specify the input field name

    blog_post = graphene.Field(BlogPostType)

    @classmethod
    def perform_mutate(cls, form, info):
        """Perform mutation function for updating an existing blog post."""
        blog_post = form.save(commit=False)
        user = info.context.user
        if blog_post.author != user:
            raise GraphQLError('You are not authorized to edit this blog post.')
        blog_post.save()
        return cls(blog_post=blog_post)

# Deleting a BlogPost
class DeleteBlogPost(graphene.Mutation):
    """Mutation for deleting the blog post."""
    class Arguments:
        id = graphene.ID()

    blog_post_id = graphene.ID()

    def mutate(self, info, id):
        """Mutate function for deleting a blog post."""
        user = info.context.user
        blog_post = BlogPost.objects.filter(id=id).first()
        if not blog_post:
            raise GraphQLError('Blog post not found.')
        if blog_post.author != user:
            raise GraphQLError('You are not authorized to delete this blog post.')
        blog_post.delete()
        return DeleteBlogPost(blog_post_id=id)


# Define mutation field
class Mutation(graphene.ObjectType):
    """Root mutation for performing data mutations."""
    create_blog_post = CreateBlogPost.Field(description="Create a new blog post.")
    update_blog_post = UpdateBlogPost.Field(description="Update an existing blog post.")
    delete_blog_post = DeleteBlogPost.Field(description="Delete a blog post.")

# Define GraphQL schema
schema = graphene.Schema(query=Query, mutation=Mutation)

