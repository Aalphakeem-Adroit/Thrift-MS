from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import ThriftGroup, Membership, Contribution, Payout
from .serializers import ThriftGroupSerializer, MembershipSerializer, ContributionSerializer, PayoutSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum

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


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {}

        # If user is an admin of any group(s)
        admin_groups = ThriftGroup.objects.filter(admin=user)
        if admin_groups.exists():
            groups_data = []
            for group in admin_groups:
                total_contributions = Contribution.objects.filter(
                    member__group=group, status='paid'
                ).aggregate(total=Sum('amount'))['total'] or 0

                total_payouts = Payout.objects.filter(
                    member__group=group
                ).aggregate(total=Sum('amount'))['total'] or 0

                balance = total_contributions - total_payouts

                groups_data.append({
                    'group_name': group.name,
                    'cycle': group.cycle,
                    'contribution_amount': float(group.contribution_amount),
                    'total_contributions': float(total_contributions),
                    'total_payouts': float(total_payouts),
                    'group_balance': float(balance),
                })

            data['admin_dashboard'] = {
                'admin': user.username,
                'groups_managed': groups_data,
            }

        # If user is a member in any group(s)
        memberships = Membership.objects.filter(user=user)
        if memberships.exists():
            membership_data = []
            for membership in memberships:
                contributions = Contribution.objects.filter(member=membership)
                payouts = Payout.objects.filter(member=membership)

                total_contributed = contributions.filter(status='paid').aggregate(total=Sum('amount'))['total'] or 0
                last_payout = payouts.order_by('-date').first()

                membership_data.append({
                    'group_name': membership.group.name,
                    'joined_on': membership.join_date,
                    'total_contributed': float(total_contributed),
                    'contributions': ContributionSerializer(contributions, many=True).data,
                    'payouts': PayoutSerializer(payouts, many=True).data,
                    'last_payout_status': 'Received' if last_payout else 'Not Yet Paid'
                })

            data['member_dashboard'] = {
                'member': user.username,
                'groups_joined': membership_data
            }

        return Response(data)