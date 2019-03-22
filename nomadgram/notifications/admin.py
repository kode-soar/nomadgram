from django.contrib import admin

from . import models

@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display_links = (
        'notification_type',
    )
 
    list_display = (
        # 페이지 테이블에 출력할 항목 기술
        'creator',
        'to',
        'notification_type',
        'image',
    )