from django.db import models
from accounts.models import User

# Create your models here.
class ThriftGroup(models.Model):
   name = models.CharField(max_length=100)
   contribution_amount = models.DecimalField(max_digits=10, decimal_places=2)
   cycle = models.CharField(max_length=20, choices=[('weekly', 'Weekly'), ('monthly', 'Monthly')])
   admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin_groups")


class Membership(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   group = models.ForeignKey(ThriftGroup, on_delete=models.CASCADE)
   join_date = models.DateField(auto_now_add=True)


class Contribution(models.Model):
   member = models.ForeignKey(Membership, on_delete=models.CASCADE)
   amount = models.DecimalField(max_digits=10, decimal_places=2)
   date = models.DateField(auto_now_add=True)
   status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('paid', 'Paid')])


class Payout(models.Model):
   member = models.ForeignKey(Membership, on_delete=models.CASCADE)
   amount = models.DecimalField(max_digits=10, decimal_places=2)
   date = models.DateField(auto_now_add=True)
   order = models.IntegerField()  # payout order in the group
