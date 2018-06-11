from django.urls import path
from rest_framework.routers import DefaultRouter

from accounts.views import DocumentViewSet, CreateUserView

app_name = 'accounts'

router = DefaultRouter()
router.register(r'documents', DocumentViewSet, base_name='documents')
router.register(r'register', CreateUserView, base_name='register')
urlpatterns = router.urls
