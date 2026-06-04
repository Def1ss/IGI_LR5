from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('content.urls')),
    path('users/', include('users.urls')),
    path('workouts/', include('workouts.urls')),
    path('enrollments/', include('enrollments.urls')),
    path('promocodes/', include('promocodes.urls')),
    path('reviews/', include('reviews.urls')),
]
