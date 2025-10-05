from rest_framework.routers import DefaultRouter
from .views import ThriftGroupViewSet, MembershipViewSet, ContributionViewSet, PayoutViewSet

router = DefaultRouter()
router.register(r'thrift-groups', ThriftGroupViewSet)
router.register(r'memberships', MembershipViewSet)
router.register(r'contributions', ContributionViewSet)
router.register(r'payouts', PayoutViewSet)

urlpatterns = router.urls