from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # Admin URL
    path('admin/', admin.site.urls),
    
    # Login URL
    path('', LoginView.as_view(
        template_name='login.html',
        next_page='/posts/',  # Redirect after successful login
        redirect_authenticated_user=True  # Prevent already logged-in users from accessing the login page
    ), name='login'),
    
    # Logout URL
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),  # Redirect to login page after logout
    
    # Blog URLs
    path('posts/', include('blog.urls')),  # Include URLs from the blog app
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
