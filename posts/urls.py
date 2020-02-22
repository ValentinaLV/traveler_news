from django.urls import path

from .views import posts_list, post_details, create_post


urlpatterns = [
    path('', posts_list, name='posts'),
    path('post/<str:slug>/', post_details, name='post-details'),
    path('create-post/', create_post, name='post-create'),

]
