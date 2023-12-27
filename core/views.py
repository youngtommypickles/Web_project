from rest_framework import viewsets
from rest_framework.decorators import action
from .serializers import CommentSerializer, BlogPostListSerializer, BlogPostCreateUpdateSerialer, BlogPostDetailSerializer
from blog.models import Comment, Post

class ActionSerializedViewSet(viewsets.ModelViewSet):
	action_serializers = {}

	def get_serializer_class(self):
		if hasattr(self, 'action_serializers'):
			if self.action in self.action_serializers:
				return self.action_serializers[self.action]

		return self.serializers_class

class CommentViewSet(viewsets.ModelViewSet):
	serializer_class = CommentSerializer
	queryset = Comment.objects.all()

class BlogPostViewSet(viewsets.ModelViewSet):
	serializer_class = BlogPostListSerializer
	queryset = Post.objects.all()

	action_serializers = {
	  'list': BlogPostListSerializer,
	  'retrieve': BlogPostDetailSerializer,
	  'create': BlogPostCreateUpdateSerialer,
	  'update': BlogPostCreateUpdateSerialer
	}

	def get_queryset(self):
		queryset = self.queryset
		author = self.request.query_params.get('author', None)
		if author:
			queryset = queryset.filter(author__username=author)
		return queryset

	@action(detail=True, methods=['post'], permission_classes=['IsAuthenticated'])

	def publish(self, request, pk=None):
		post = self.get_object()
		if request.user == post.author:
			return Response({'message': 'blog post was published'}, status=status.HTTP_200_OK)
		else:
			return Response({'error': 'You don\'t have permissions'}, status=status.HTTP_403_FORBIDDEN)


	@action(detail=False)
	def published_posts(self, request):
		published_posts = Post.published.all()

		page = self.paginate_queryset(published_posts)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(published_posts, many=True)
		return Response(serializer.data)