from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blog.views import BookPostViewSet, CommentViewSet, LikeViewSet

router = DefaultRouter()
router.register(r'posts', BookPostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls)),
    
    path('posts/<int:post_id>/comments/', 
         CommentViewSet.as_view({'get': 'list', 'post': 'create'}), 
         name='post-comments'),
         
    path('posts/<int:post_id>/comments/<int:pk>/', 
         CommentViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}), 
         name='comment-detail'),
         
    path('posts/<int:post_id>/like/', 
         LikeViewSet.as_view({'post': 'create', 'delete': 'destroy'}), 
         name='post-like'),
]