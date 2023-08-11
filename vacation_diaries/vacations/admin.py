from django.contrib import admin

from vacation_diaries.vacations.models import Vacation


class VacationAdmin(admin.ModelAdmin):
    list_display = ("destination", "start_date", "end_date", "rating", "budget", "user")
    list_filter = ("destination", "rating", "budget", "user")
    search_fields = ("destination",)
    ordering = ["destination"]


admin.site.register(Vacation, VacationAdmin)
