# from django.urls import path
# from . import views

# app_name = 'blog'

# urlpatterns = [
#     path('ram/', views.index, name="index"),
#     path('form/<str:post_id>/', views.data1, name="data"),
#     path('details/', views.details, name="details"),
#     path('contact/', views.contact, name="contact"),
# ]
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
app_name = 'blog'



urlpatterns = [
    path('custom_404/', custom, name="custom_404"),
    path('index/', index, name="index"),
    path('contact/', contact_view, name='contact'),
    path('ListOut/', ListOut, name='ListOut'),
    path('success/', success_view, name='success'),
    path('profile/', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('update/<int:id>/', update_view, name='update'),
    path('delete/<int:id>/', delete_view, name='delete'),
    path('update_user/<int:id>/', update_user_data, name='update_user_data'),
    path('delete_user/<int:id>/', delet_user_data, name='delet_user_data'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
     path('logout/', logout_view, name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)