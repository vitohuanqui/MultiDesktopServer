from django.urls import path
from rest_framework.routers import DefaultRouter

from accounts.views import DocumentViewSet, CreateUserView, CreateLeapUserView, \
    ShareDocumentViewSet, ShareListDocumentViewSet, UpdateDocumentView

app_name = 'accounts'

router = DefaultRouter()
router.register(r'register', CreateLeapUserView, base_name='register')
router.register(r'me', CreateUserView, base_name='me')
router.register(r'documents', DocumentViewSet, base_name='documents')
router.register(r'update_document', UpdateDocumentView, base_name='documents')
router.register(r'share_document', ShareDocumentViewSet, base_name='set_shared')
router.register(r'get_share_document', ShareListDocumentViewSet, base_name='share_documents')
urlpatterns = router.urls
