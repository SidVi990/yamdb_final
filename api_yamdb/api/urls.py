from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet, get_token,
                    let_register)

v1_router = SimpleRouter()

v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
v1_router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
v1_router.register(r'users', UserViewSet)

registration_urls = [
    path('signup/', let_register, name='signup'),
    path('token/', get_token, name='token')
]

urlpatterns = [
    path('v1/auth/', include(registration_urls)),
    path('v1/', include(v1_router.urls)),
]
