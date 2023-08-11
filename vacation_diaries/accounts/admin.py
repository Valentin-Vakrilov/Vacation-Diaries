from django.contrib import admin

from vacation_diaries.accounts.models import AppUser, Profile


class AppUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_staff")
    ordering = ["username"]
    list_filter = ("is_staff",)
    search_fields = ("username", "email")


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "age", "gender", "user")
    ordering = ["first_name", "last_name"]
    list_filter = ("gender",)
    search_fields = ("first_name", "last_name")


admin.site.register(AppUser, AppUserAdmin)
admin.site.register(Profile, ProfileAdmin)
