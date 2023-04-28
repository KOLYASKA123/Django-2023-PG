from django.urls import path, re_path
from . import views

urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    #path('', views.PostListView.as_view(), name='post_list'),
    path('create_post/', views.create_post, name='create_post'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    #path('edit/<int:post_id>/', views.EditPostView.as_view(), name='edit_post'),
    re_path(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list, name='post_list_by_tag'),
    re_path(r'^(?P<post_id>\d+)/share/$', views.post_share, name='post_share'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('my_blogs/', views.BlogListView.as_view(), name='my_blogs'),
    path('posts_of_blog/<int:blog_id>/', views.posts_of_blog, name='posts_of_blog'),
]