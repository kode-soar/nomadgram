from django.conf.urls import url
from . import views
app_name = "images" # 1-29강 추가 팁에서 보고 추가됨(없으면 오류)

urlpatterns = [
    url(
        regex=r'^$',
        view=views.Images.as_view(),
        name='images'
    ),
    url(
        regex=r'^(?P<image_id>[0-9]+)/$',
        view=views.ImageDetail.as_view(),
        name='image_detail'
    ),
    url(
        regex=r'^(?P<image_id>[0-9]+)/likes/$',
        view=views.LikeImage.as_view(),
        name='like_image'
    ),
    url(
        regex=r'^(?P<image_id>[0-9]+)/unlikes/$',
        view=views.UnLikeImage.as_view(),
        name='unlike_image'
    ),
    url(
        regex=r'^(?P<image_id>[0-9]+)/comments/$',
        view=views.CommentOnImage.as_view(),
        name='comment_image'
    ),
    url(
        regex=r'^comments/(?P<comment_id>[0-9]+)/$',
        view=views.Comment.as_view(),
        name='comment'
    ),
    url(
        regex=r'^(?P<image_id>[0-9]+)/comments/(?P<comment_id>[0-9]+)/$',
        view=views.ModerateComments.as_view(),
        name='moderrate_comments'
    ),
    url(
        regex=r'^search/$',
        view=views.Search.as_view(),
        name='search'
    ),    


    # 아래와 같이 url 대신, path를 이용해서도 라우팅 가능함
    # 아래와 같이 할 경우 정규식 사용하지 않을 수 있음(장고 2.0)
    # https://docs.djangoproject.com/en/2.1/topics/http/urls/
    # from django.urls import path    
    # path("comments/", view=views.ListAllComments.as_view(), name="all_comments"),
]