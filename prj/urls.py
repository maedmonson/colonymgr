"""projects URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from colonymgr import views as colonymgr_views
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('signup/', accounts_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('colonies/<int:home_pk>/', colonymgr_views.colonies, name='colonies'),
    path('queens/<int:pk>/', colonymgr_views.queens, name='queens'),
    path('colony_logs/<int:pk>/', colonymgr_views.colony_logs, name='colony_logs'),
    path('display_colony_log/<int:pk>/', colonymgr_views.display_colony_log, name='display_colony_log'),

    path('queen_logs/<int:pk>/', colonymgr_views.queen_logs, name='queen_logs'),

    path('', colonymgr_views.home, name='home'),
    path('yards/new/', colonymgr_views.new_yard, name='new_yard'),
    path('yards/<int:yard_pk>/delete/', colonymgr_views.YardDeleteView.as_view(), name='delete_yard'),

    path('colonies/new/<int:yard_pk>/', colonymgr_views.new_colony, name='new_colony'),
    path('colony_logs/new/<int:pk>/', colonymgr_views.new_colony_log, name='new_colony_log'),
    path('queens/new/<int:colony_pk>/', colonymgr_views.new_queen, name='new_queen'),
    path('admin/', admin.site.urls),

    path('yards/<int:yard_pk>/edit/',colonymgr_views.YardUpdateView.as_view(), name='edit_yard'),
    path('colonies/<int:colony_pk>/edit/', colonymgr_views.ColonyUpdateView.as_view(), name='edit_colony'),
    path('colony_logs/<int:colony_log_pk>/edit/', colonymgr_views.Colony_logUpdateView.as_view(), name='edit_colony_log'),
    path('queens/<int:queen_pk>/edit/', colonymgr_views.QueenUpdateView.as_view(), name='edit_queen'),
    path('queens/<int:queen_pk>/delete/', colonymgr_views.QueenDeleteView.as_view(), name='delete_queen'),
    path('ajax/load-colonies/', colonymgr_views.load_colonies, name='ajax_load_colonies'),

    path('reset/',auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt'
    ),name='password_reset'),

    path('reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),

    path('reset/complete', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),

    path('settings/password/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
        name='password_change'),

    path('settings/password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
        name='password_change_done'),



]
