from rest_framework import viewsets, permissions
from django.contrib.contenttypes.models import ContentType
from blog.models import BookPost, Comment, Like
from blog.serializers import BookPostSerializer, CommentSerializer, LikeSerializer
from blog.permissions import IsOwnerOrReadOnly, IsCommentOwner
from rest_framework import filters


class BookPostViewSet(viewsets.ModelViewSet):
    queryset = BookPost.objects.select_related("user").prefetch_related(
        "comments", "likes"
    )
    serializer_class = BookPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filterset_fields = ["author", "user__username"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsCommentOwner]

    def get_queryset(self):
        return Comment.objects.filter(
            content_type=ContentType.objects.get_for_model(BookPost),
            object_id=self.kwargs["post_id"],
        ).select_related("user")

    def perform_create(self, serializer):
        content_type = ContentType.objects.get_for_model(BookPost)
        serializer.save(
            user=self.request.user,
            content_type=content_type,
            object_id=self.kwargs["post_id"],
        )


class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Like.objects.filter(
            content_type=ContentType.objects.get_for_model(BookPost),
            object_id=self.kwargs["post_id"],
        )

    def perform_create(self, serializer):
        content_type = ContentType.objects.get_for_model(BookPost)
        serializer.save(
            user=self.request.user,
            content_type=content_type,
            object_id=self.kwargs["post_id"],
        )
