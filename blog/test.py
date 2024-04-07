from django.test import RequestFactory, TestCase
from graphene.test import Client
import json
from users.models import Account as User
from .models import BlogPost
from .schema import schema

def execute_test_client_api_query(api_query, user=None, variable_values=None, **kwargs):
    """
    Returns the results of executing a graphQL query using the graphene test client.  This is just a helper method for our tests
    """
    request_factory = RequestFactory()
    context_value = request_factory.get('/api/')  # or use reverse() on the API endpoint
    context_value.user = user
    client = Client(schema)  
    executed = client.execute(api_query, context_value=context_value, variable_values=variable_values, **kwargs)
    return executed

class BlogPostTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user', email='test@example.com')
        self.blog_post = BlogPost.objects.create(title='Test Title', subTitle='Test Subtitle', body='Test Body', author=self.user)

    def execute_query(self, api_query, user=None, variable_values=None, **kwargs):
        executed = execute_test_client_api_query(api_query, user=user, variable_values=variable_values, **kwargs)
        return executed

    def test_create_blog_post_mutation(self):
        query = '''
        mutation {
            createBlogPost(title: "New Title", subtitle: "New Subtitle", body: "New Body") {
                blogPost {
                    id
                    title
                    subTitle
                    body
                    dateCreated
                    author {
                        id
                        username
                    }
                }
            }
        }
        '''
        response = self.execute_query(query, user=self.user)
        self.assertIsNone(response.get('errors'))
        self.assertEqual(response['data']['createBlogPost']['blogPost']['title'], 'New Title')
        self.assertEqual(response['data']['createBlogPost']['blogPost']['subTitle'], 'New Subtitle')
        self.assertEqual(response['data']['createBlogPost']['blogPost']['body'], 'New Body')
        self.assertEqual(response['data']['createBlogPost']['blogPost']['author']['username'], 'test_user')

    def test_update_blog_post_mutation(self):
        query = '''
        mutation {
            updateBlogPost(input: {id: %d, title: "Updated Title", subTitle: "Updated Subtitle", body: "Updated Body"}) {
                blogPost {
                    id
                    subTitle
                    body
                }
            }
        }
        ''' % self.blog_post.id
        response = self.execute_query(query, user=self.user)
        self.assertIsNone(response.get('errors'))
        self.assertEqual(response['data']['updateBlogPost']['blogPost']['subTitle'], 'Updated Subtitle')
        self.assertEqual(response['data']['updateBlogPost']['blogPost']['body'], 'Updated Body')

    def test_delete_blog_post_mutation(self):
        query = '''
        mutation {
            deleteBlogPost(id: %d) {
                blogPostId
            }
        }
        ''' % self.blog_post.id
        response = self.execute_query(query, user=self.user)
        self.assertIsNone(response.get('errors'))
        self.assertEqual(response['data']['deleteBlogPost']['blogPostId'], str(self.blog_post.id))
