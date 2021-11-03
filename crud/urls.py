from django.urls import path
from . import views

app_name = 'crud'
urlpatterns = [
    # Create
    path('create/', views.create, name='create'),

    # Read
    path('', views.index, name='index'),
    path('<int:article_pk>/', views.detail, name='detail'),

    # Update
    path('<int:article_pk>/update/', views.update, name='update'),

    # Delete
    path('<int:article_pk>/delete/', views.delete, name='delete'),
    
    # Comment
    path('<int:article_pk>/comments/', views.comment_create, name='comment_create'),
    path('<int:article_pk>/comments/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),

    # Like
    path('<int:article_pk>/likes/', views.article_likes, name='article_likes'),
    path('<int:article_pk>/comments/<int:comment_pk>/likes/', views.comment_likes, name='comment_likes'),
    path('<int:article_pk>/comments/<int:comment_pk>/dislikes/', views.comment_dislikes, name='comment_dislikes'),
]
