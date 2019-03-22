from django.contrib import admin
from . import models # . means same folder
# Register your models here.

#모델들이 admin에서 어떻게 보일지 서술

@admin.register(models.Image) # decorator(함수, 클래스에 함수를 장식(호출시마다 먼저작동)해주는 기능) 작성 후 한줄 띄우면 에러 발생, 바로 앞에 붙여서 기술해야함
class ImageAdmin(admin.ModelAdmin):
    list_display_links = (
        # 클릭 했을 때, 수정 화면으로 가는 링크를 입힐 항목 기술
        'location',
        'caption',
    )

    search_fields = (
        # 검색 폼이 추가되며, 검색 시 검색할 항목 기술
        'location',
        'caption',
        'creator__username',
        # creator은 user_models.User 클래스 객체를 바라보고 있기 때문에(필드가 아닌)
        # User 클래스에서  def __str__에 username이 지정되어 있어 검색 가능할 것 처럼 보이지만
        # 직접 검색 대상이 될 수 없어, User 클래스 하위의 필드를 직접 지정
    )

    list_filter = (
        # 화면 우측에 필터를 추가하며, 필터링 할 항목 기술
        'location',
        'creator',
    )

    list_display = (
        # 페이지 테이블에 출력할 항목 기술
        'id',
        'file',
        'location',
        'caption',
        'creator',
        'created_at',
        'updated_at',
        'tag_list',
    )

    def get_queryset(self, request):
        return super(ImageAdmin, self).get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

@admin.register(models.Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'creator',
        'image',
        'created_at',
        'updated_at',
    )

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display_links = (
        # 클릭 했을 때, 수정 화면으로 가는 링크를 입힐 항목 기술
        'id',
        'message',
    )
    list_display = (
        'id',
        'message',
        'creator',
        'image',
        'created_at',
        'updated_at',
    )