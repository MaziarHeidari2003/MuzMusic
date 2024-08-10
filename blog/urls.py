from django.urls import path
from .views import BlogSingleView,BasePostListView,BlogAuthorView,BlogCategoryView,BlogHomeView,likeView,PostCreateView,follow_unfollow

app_name='blog'

urlpatterns = [
   # path('',BlogView.as_view(),name='blog_view'),
    path('single-view/<int:pk>',BlogSingleView.as_view(), name='single_view'),
    path('category/<str:cat_name>/', BlogCategoryView.as_view(), name='blog_category'),
    path('author/<str:author_name>/', BlogAuthorView.as_view(), name='blog_author'),
    path('', BlogHomeView.as_view(), name='blog_home'),
        # This will handle the default case with pagination
    path('like/<int:pk>',likeView, name='like_post'),
    path('post-create',PostCreateView.as_view(),name='post_create'),
    path('follow-unfollow',follow_unfollow,name='follow')
   ]
