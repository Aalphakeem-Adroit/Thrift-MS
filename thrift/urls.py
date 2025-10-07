from rest_framework.routers import DefaultRouter
from .views import ThriftGroupViewSet, MembershipViewSet, ContributionViewSet, PayoutViewSet

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from django.urls import path, include
from .views import DashboardView

router = DefaultRouter()
router.register(r'thrift-groups', ThriftGroupViewSet)
router.register(r'memberships', MembershipViewSet)
router.register(r'contributions', ContributionViewSet)
router.register(r'payouts', PayoutViewSet)

urlpatterns = router.urls

# urlpatterns += [
#     path('dashboard/', DashboardView.as_view(), name='dashboard'),
# ]

# Custom API root view to include dashboard link
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'thrift-groups': reverse('thriftgroup-list', request=request, format=format),
        'memberships': reverse('membership-list', request=request, format=format),
        'contributions': reverse('contribution-list', request=request, format=format),
        'payouts': reverse('payout-list', request=request, format=format),
        'dashboard': request.build_absolute_uri('/api/dashboard/')
    })

urlpatterns = [
    path('', api_root, name='api-root'),  # custom root replaces router.urls' root
    path('', include(router.urls)),        # include ViewSets
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]