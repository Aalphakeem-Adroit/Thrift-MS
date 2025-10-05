from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import ThriftGroup, Membership, Contribution, Payout
from .serializers import ThriftGroupSerializer, MembershipSerializer, ContributionSerializer, PayoutSerializer

# Create your views here.
class ThriftGroupViewSet(viewsets.ModelViewSet):
    queryset = ThriftGroup.objects.all()
    serializer_class = ThriftGroupSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

class ContributionViewSet(viewsets.ModelViewSet):
    queryset = Contribution.objects.all()
    serializer_class = ContributionSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

class PayoutViewSet(viewsets.ModelViewSet):
    queryset = Payout.objects.all()
    serializer_class = PayoutSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]