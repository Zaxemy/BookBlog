from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


User = get_user_model()


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ActivityModel(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class BookPost(TimeStampedModel):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=100)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)
    likes = GenericRelation("Like", related_query_name="book_post_like")
    comments = GenericRelation("Comment",  related_query_name="book_post_comment")

    def __str__(self):
        return self.title


class Comment(ActivityModel):
    text = models.TextField(max_length=1000)

    class Meta:
        ordering = ["-created_at"]


class Like(ActivityModel):
    class Meta:
        unique_together = ["user", "content_type", "object_id"]
