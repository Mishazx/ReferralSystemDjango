from django.contrib import admin
from .models import User, VerificationCode


class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'invite_code', 'activated_invite')


class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at', 'expires_at', 'is_used')


admin.site.register(User, UserAdmin)
admin.site.register(VerificationCode, VerificationCodeAdmin)