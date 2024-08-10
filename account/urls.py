from django.urls import path
from .views import register_user,logout_user,login_user,edit_profile,members_profile,bio
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup',register_user,name='register'),
    path('logout',logout_user,name='logout'),
    path('login/',login_user,name='login'),
    path('edit',edit_profile,name='edit_profile'),
    path('members',members_profile,name='members'),
    path('signup/bio/<str:username>',bio,name='bio'),

    path('reset_password',auth_views.PasswordResetView.as_view(
        template_name='account/password_reset.html'),name='reset_password'),

    path('reset_password_sent',auth_views.PasswordResetDoneView.as_view(
        template_name='account/password_reset_sent.html'),name='password_reset_done'),

    path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(
        template_name='account/password_reset_done.html'),name='password_reset_confirm'),

    path('reset_password_complete',auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password_reset_complete.html'
    ),name='password_reset_complete')




]
