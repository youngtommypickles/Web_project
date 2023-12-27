from rest_framework import serializers, viewsets
from blog.models import Comment, Post

class CommentSerializer(serializers.ModelSerializer):
	text = serializers.CharField(max_length=200)
	created_data = serializers.DateTimeField()

	class Meta:
		model = Comment
		fields = ('text', 'created_data')

class BlogPostListSerializer(serializers.ModelSerializer):
	preview_text =serializers.SerializerMethodField()

	def get_preview_text(self, post):
		return post.get_text_preview()

	class Meta:
		model = Post
		fields = ('title', 'author', 'created_data', 'preview_text')

class BlogPostCreateUpdateSerialer(serializers.ModelSerializer):
	class Meta:
		model = Post
		exclude = ()

class BlogPostDetailSerializer(serializers.ModelSerializer):
	comments = CommentSerializer(many=True, read_only=True)
	comments_count = serializers.SerializerMethodField()

	def get_comments_count(self, obj):
		#return Comment.objects.filter(post=obj)
		return obj.comments.count()

	class Meta:
		model = Post
		fields = ('title', 'author', 'created_data', 'preview_text', 'comments', 'comments_count')