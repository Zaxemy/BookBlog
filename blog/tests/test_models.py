from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError, IntegrityError
from django.contrib.contenttypes.models import ContentType

from blog.models import BookPost, Comment, Like

User = get_user_model()

class BookPostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = BookPost.objects.create(
            title="Test Book",
            author="Author Name",
            content="Book review",
            user=self.user,
            rating=4.5
        )

    def test_create_book_post(self):
        """Проверка создания поста"""
        self.assertEqual(self.post.title, "Test Book")
        self.assertEqual(self.post.author, "Author Name")
        self.assertEqual(self.post.content, "Book review")
        self.assertEqual(self.post.user, self.user)
        self.assertEqual(self.post.rating, 4.5)

    def test_default_rating(self):
        """Проверка значения рейтинга по умолчанию"""
        post = BookPost.objects.create(
            title="Another Book",
            author="Another Author",
            content="Another review",
            user=self.user
        )
        self.assertEqual(post.rating, 0)

    def test_timestamps(self):
        """Проверка автоматических дат"""
        self.assertIsNotNone(self.post.created_at)
        self.assertIsNotNone(self.post.updated_at)
        old_updated_at = self.post.updated_at
        self.post.title = "Updated Title"
        self.post.save()
        self.assertNotEqual(self.post.updated_at, old_updated_at)

    def test_generic_relations(self):
        """Проверка полиморфных связей"""
        comment = Comment.objects.create(
            user=self.user,
            content_object=self.post,
            text="Great post!"
        )
        like = Like.objects.create(
            user=self.user,
            content_object=self.post
        )
        self.assertIn(comment, self.post.comments.all())
        self.assertIn(like, self.post.likes.all())

class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = BookPost.objects.create(
            title="Test Book",
            author="Author Name",
            content="Book review",
            user=self.user
        )
        self.comment = Comment.objects.create(
            user=self.user,
            content_object=self.post,
            text="Great post!"
        )

    def test_comment_creation(self):
        """Проверка создания комментария"""
        self.assertEqual(self.comment.text, "Great post!")
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.content_object, self.post)

    def test_ordering(self):
        """Проверка порядка сортировки"""
        later_comment = Comment.objects.create(
            user=self.user,
            content_object=self.post,
            text="Another comment"
        )
        comments = list(self.post.comments.all())
        self.assertEqual(comments[0], later_comment)
        self.assertEqual(comments[1], self.comment)

class LikeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = BookPost.objects.create(
            title="Test Book",
            author="Author Name",
            content="Book review",
            user=self.user
        )

    def test_unique_like(self):
        """Проверка уникальности лайка"""
        Like.objects.create(
            user=self.user,
            content_object=self.post
        )
        with self.assertRaises(IntegrityError):
            Like.objects.create(
                user=self.user,
                content_object=self.post
            )

    def test_content_type_resolution(self):
        """Проверка работы GenericForeignKey"""
        like = Like.objects.create(
            user=self.user,
            content_object=self.post
        )
        content_type = ContentType.objects.get_for_model(BookPost)
        self.assertEqual(like.content_type, content_type)
        self.assertEqual(like.object_id, self.post.id)
        self.assertEqual(like.content_object, self.post)