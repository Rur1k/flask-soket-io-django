from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('main.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   ]

# curl \
#   -X POST \
#   -H "Content-Type: application/json" \
#   -d '{"email": "admin@admin.com", "password": "admin"}' \
#   http://127.0.0.1:8000/api/token/
#
# curl \
#   -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ5MjU2MDY4LCJqdGkiOiJjNzRmNTQ3YzhiZjU0Yjc3YWIyN2E2OWZmODYzN2NiNiIsInVzZXJfaWQiOjF9.VutCAFwy82Ty69cc_Ywn9RKEDAOyNCRhwCsiBgR3lD0" \
#   http://localhost:8000/api/some-protected-view/