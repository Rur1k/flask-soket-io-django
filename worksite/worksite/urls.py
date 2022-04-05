from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('main.urls')),
    path('api-auth', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
   ]

# curl \
#   -X POST \
#   -H "Content-Type: application/json" \
#   -d '{"email": "admin@admin.com", "password": "admin"}' \
#   http://127.0.0.1:8000/auth/jwt/create/

# curl \
#   -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ4ODEzNjk1LCJpYXQiOjE2NDg4MTMzOTUsImp0aSI6IjRhOGRiZmZkNDI2NTRiNzk5YzUyYWYyYWQ2MWVlMDAxIiwidXNlcl9pZCI6MX0.CXKK78Y4xCope6LuaDaJQUKIQiaTT7zMNfvuWMARr8Y" \
#   http://127.0.0.1:8000/api/some-protected-view/