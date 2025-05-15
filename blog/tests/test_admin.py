from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from blog.models import BookPost, Comment, Like
from blog.admin import BookPostAdmin, CommentAdmin, LikeAdmin

class AdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.user = get_user_model().objects.create_superuser(
            username='admin',
            password='admin'
        )
        self.client.login(username='admin', password='admin')

    def test_bookpost_admin(self):
        admin = BookPostAdmin(BookPost, self.site)
        self.assertIn('title', admin.list_display)
        self.assertIn('author', admin.list_filter)
        self.assertIn('search_fields', dir(admin))

    def test_comment_admin(self):
        admin = CommentAdmin(Comment, self.site)
        self.assertIn('text', admin.list_display)
        self.assertIn('user', admin.list_filter)

    def test_like_admin(self):
        admin = LikeAdmin(Like, self.site)
        self.assertIn('user', admin.list_display)
        self.assertIn('content_type', admin.list_filter)