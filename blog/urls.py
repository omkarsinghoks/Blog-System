
from django.urls import path
from .views import HomeView, AboutView, AddPostView, EditPostView, DeletePostView,HomeOnlyView,AboutViewWithoutLogin

urlpatterns = [
    
    path('', HomeView.as_view(), name='blog-home'),
    # path('about1/',AboutViewWithoutLogin.as_view(),name='blog-about-page'),
    path('about/', AboutView.as_view(), name='blog-about'),
    
    path('add_post/', AddPostView.as_view(), name='add-post'),
    path('edit/<int:pk>/', EditPostView.as_view(), name='edit_post'),  # Edit post route
    path('delete/<int:pk>/', DeletePostView.as_view(), name='delete_post'),  # Delete post route
]

