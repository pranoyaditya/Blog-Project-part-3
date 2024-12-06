from django.urls import path
from . import views

urlpatterns = [
    path('add_post/', views.AddPostCreateView.as_view(), name='add_post'),
    path('edit_post/<int:id>', views.EditPostView.as_view(), name='edit_post'),
    path('delete_post/<int:id>', views.DeletePostView.as_view(), name='delete_post'),
]