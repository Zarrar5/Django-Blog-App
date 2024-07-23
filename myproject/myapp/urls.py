from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("blog/", views.blog_posts, name="blog_posts"),
    path("blog/create", views.create_post, name="create_post"),
    path("blog/update/<int:post_id>/", views.update_post, name="update_post"),
    path("blog/delete/<int:post_id>/", views.delete_post, name="delete_post"),
    path("blog/<int:post_id>/", views.post_detail, name="post_detail"),
    path("blog/like/<int:post_id>/", views.like_post, name="like_post"),
]