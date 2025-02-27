import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    referral_code = models.CharField(max_length=20, unique=True, blank=True)
    referred_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    # Override the groups field to avoid reverse accessor clash
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='user'
    )

    # Override the user_permissions field to avoid reverse accessor clash
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user'
    )

    def save(self, *args, **kwargs):
        if not self.referral_code:
            # Generate a unique referral code (first 8 characters of a UUID)
            self.referral_code = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

class Referral(models.Model):
    referrer = models.ForeignKey(User, related_name="referrals", on_delete=models.CASCADE)
    referred_user = models.ForeignKey(User, related_name="referred_users", on_delete=models.CASCADE)
    date_referred = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('successful', 'Successful')],
        default='pending'
    )

    def __str__(self):
        return f"{self.referrer.username} referred {self.referred_user.username}"

# Optional rewards model to track rewards or incentives earned by referrers.
class Reward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    description = models.CharField(max_length=255, blank=True)
    awarded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.points} points"
