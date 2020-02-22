from django.test import TestCase
from django.urls import reverse

from posts.models import Post
from user.models import CustomUser


class PostViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = CustomUser.objects.create_user(email='test_user@test.com',
                                                       username='test_user',
                                                       password='12345')
        cls.post = Post.objects.create(title='Test Post Title',
                                       author=cls.test_user,
                                       content='Test Content Description')
        cls.post.slug = 'test-post-title-2202822'

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get('/posts/post/test-post-title-2202822')
        self.assertEqual(resp.status_code, 301)

    def test_view_uses_correct_template_posts(self):
        resp = self.client.get(reverse('home-page'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'index.html')

    def test_view_uses_correct_template_post_details(self):
        resp = self.client.get('/posts/post/test-post-title-2202822')
        self.assertTemplateNotUsed(resp, 'post_details.html')

    def test_view_uses_correct_template_post_create(self):
        resp = self.client.get(reverse('posts:post-create'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'post_create.html')
