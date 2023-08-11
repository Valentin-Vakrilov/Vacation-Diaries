from django.contrib import admin
from vacation_diaries.photos.models import Photo, Comment


class PhotoAdmin(admin.ModelAdmin):
    list_display = ("user", "upload_date_and_time", "total_likes",
                    "photo_main", "photo_second", "photo_third")
    list_filter = ("user",)
    search_fields = ("user",)
    ordering = ["-upload_date_and_time"]


class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "publication_date_and_time")
    list_filter = ("user",)
    ordering = ["-publication_date_and_time"]


admin.site.register(Photo, PhotoAdmin)
admin.site.register(Comment, CommentAdmin)
