from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import BookPost, Comment

@shared_task
def send_new_post_notification(post_id):
    post = BookPost.objects.get(id=post_id)
    subject = f'New post published: {post.title}'
    message = f'Check out the new post: {post.content[:100]}...'
    recipient_list = [post.user.email]
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )

@shared_task
def send_new_comment_notification(comment_id):
    comment = Comment.objects.get(id=comment_id)
    subject = f'New comment on your post: {comment.content_object.title}'
    message = f'User {comment.user.username} commented: {comment.text[:50]}...'
    recipient = comment.content_object.user.email
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [recipient],
        fail_silently=True,
    )