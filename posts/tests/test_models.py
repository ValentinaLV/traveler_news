import datetime

from django.core import mail
from django.test import TestCase

from posts.models import Post, Comment
from user.models import CustomUser


class PostModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = CustomUser.objects.create_user(email='test_user@test.com',
                                                       username='test_user',
                                                       password='12345')
        cls.post = Post.objects.create(title='Test Post Title',
                                       author=cls.test_user,
                                       content='Test Content Description')
        cls.post.slug = 'test-post-title-2202856'

    def test_get_absolute_url(self):
        self.assertEquals(self.post.get_absolute_url(), '/posts/post/test-post-title-2202856/')

    def test_title_label(self):
        field_label = self.post._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_title_max_length(self):
        max_length = self.post._meta.get_field('title').max_length
        self.assertEquals(max_length, 100)

    def test_content_label(self):
        field_label = self.post._meta.get_field('content').verbose_name
        self.assertEquals(field_label, 'content')

    def test_content_max_length(self):
        max_length = self.post._meta.get_field('content').max_length
        self.assertEquals(max_length, None)

    def test_date_label(self):
        field_label = self.post._meta.get_field('created_date').verbose_name
        self.assertEquals(field_label, 'created date')

    def test_created_date(self):
        date = self.post.created_date.date().today()
        self.assertEquals(date, datetime.date.today())

    def test_object_title(self):
        expected_object_title = self.post.title
        self.assertEquals(expected_object_title, str(self.post))

    def test_title_data(self):
        self.assertEquals(self.post.title, 'Test Post Title')

    def test_content_data(self):
        self.assertEquals(self.post.content, 'Test Content Description')

    def test_author_data(self):
        self.assertEquals(self.post.author, self.test_user)


class CommentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user1 = CustomUser.objects.create_user(email='test_user1@test.com',
                                                        username='test_user1',
                                                        password='12345')
        cls.test_user2 = CustomUser.objects.create_user(email='test_user2@test.com',
                                                        username='test_user2',
                                                        password='54321')
        cls.post = Post.objects.create(title='Test Post Title',
                                       author=cls.test_user1,
                                       content='Test Content Description')
        cls.comment = Comment.objects.create(user=cls.test_user2,
                                             post=cls.post,
                                             content='Test Comment')

    def test_content_label(self):
        field_label = self.comment._meta.get_field('content').verbose_name
        self.assertEquals(field_label, 'content')

    def test_content_max_length(self):
        max_length = self.comment._meta.get_field('content').max_length
        self.assertEquals(max_length, None)

    def test_user_label(self):
        field_label = self.comment._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'user')

    def test_date_label(self):
        field_label = self.comment._meta.get_field('created_date').verbose_name
        self.assertEquals(field_label, 'created date')

    def test_created_date(self):
        date = self.comment.created_date.date().today()
        self.assertEquals(date, datetime.date.today())

    def test_comment_post(self):
        field_label = self.comment._meta.get_field('post').verbose_name
        self.assertEquals(field_label, 'post')

    def test_object_name(self):
        expected_object_name = f'{self.comment.user} {self.comment.content}'
        self.assertEquals(expected_object_name, str(self.comment))

    def test_content_data(self):
        self.assertEquals(self.comment.content, 'Test Comment')

    def test_comment_post_data(self):
        self.assertEquals(self.comment.post.content, 'Test Content Description')

    def test_user_data(self):
        self.assertEquals(self.comment.user, self.test_user2)
        self.assertNotEquals(self.comment.user, self.test_user1)

    def test_send_email_about_new_comment(self):
        mail.send_mail(f'Comment was added to your post {self.comment.post.title}',
                       f'Username: {self.comment.user.username}\n'
                       f'Email: {self.comment.user.email}\n'
                       f'Comment body: {self.comment.content}',
                       'traveller@gmail.com',
                       [self.comment.post.author.email],
                       fail_silently=False)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, f'Comment was added to your post {self.comment.post.title}')
