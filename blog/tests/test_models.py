from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from ..models import Post

User = get_user_model()


class PostTest(TestCase):
	def setUp(self):
		author1 = User.objects.create(username='author #1')
		author2 = User.objects.create(username='author #2')
		Post.objects.create(title='Test Post #1', text='Dummy text #1', author=author1)
		Post.objects.create(title='Test Post #2', text='Dummy text #2', author=author2)
		Post.objects.create(title='Test Post #3', text='Dummy text #3', is_published=True,  author=author2)
		
	def test_published_method_for_post(self):
		post = Post.objects.get(title='Test Post #1')
		post.publish()
		self.assertEqual(post.is_published, True)

	def test_published_post_filtering(self):
		post = Post.objects.get(title='Test Post #1')
		post.publish()
		posts = Post.published.all()
		self.assertEqual(posts.count(), 1)