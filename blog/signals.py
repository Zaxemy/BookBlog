from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BookPost, Comment
from .tasks import send_new_post_notification, send_new_comment_notification

@receiver(post_save, sender=BookPost)
def post_post_save(sender, instance, created, **kwargs):
    if created:
        send_new_post_notification.delay(instance.id)

@receiver(post_save, sender=Comment)
def comment_post_save(sender, instance, created, **kwargs):
    if created and instance.content_object.user != instance.user:
        send_new_comment_notification.delay(instance.id)