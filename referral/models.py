import random
import string
from django.db import models
from django.utils import timezone


class User(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    invite_code = models.CharField(max_length=6, unique=True, blank=True)
    activated_invite = models.CharField(max_length=6, blank=True, null=True)
    referred_users = models.ManyToManyField('self', symmetrical=False, blank=True)

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        super().save(*args, **kwargs)

class VerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verification_codes')
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = now() + timedelta(minutes=5)
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        from django.utils import timezone
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(minutes=5)
        super().save(*args, **kwargs)

    def is_valid(self):
        return timezone.now() <= self.expires_at and not self.is_used