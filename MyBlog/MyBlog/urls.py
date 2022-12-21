from django.contrib import admin
from django.urls import path, include, reverse_lazy
from users import views as userViews
from django.contrib.auth import views as authViews
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('reg/', userViews.register, name='reg'),
    path('profile/', userViews.profile, name='profile'),
    path('user/', authViews.LoginView.as_view(template_name='users/user.html'), name='user'),
    path('exit/', authViews.LogoutView.as_view(template_name='users/exit.html'), name='exit'),
    path(
        'pass-reset/',
        authViews.PasswordResetView.as_view(template_name='users/pass_reset.html'),
        name='pass-reset',
    ),
    path(
        'password_reset_confirm/<uidb64>/<token>/',
        authViews.PasswordResetConfirmView.as_view(template_name='users/password-reset-confirm.html'),
        name='password_reset_confirm'
    ),
    path(
        'password_reset_done',
        authViews.PasswordResetDoneView.as_view(template_name='users/password-reset-done.html'),
        name='password_reset_done'
    ),
    path(
        'password_reset_complete',
        authViews.PasswordResetCompleteView.as_view(template_name='users/password-reset-complete.html'),
        name='password_reset_complete'
    ),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
