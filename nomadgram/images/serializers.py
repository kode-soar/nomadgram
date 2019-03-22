from rest_framework import serializers
from . import models
from nomadgram.users import models as user_models
from taggit_serializer.serializers import (TagListSerializerField, TaggitSerializer)

class SmallImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = ('file', )


class FeedUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = user_models.User
        fields = (
            'username',
            'profile_image'
        )

class CommentSerializer(serializers.ModelSerializer):

    creator = FeedUserSerializer(read_only=True)

    class Meta:
        model = models.Comment
        fields = (
            'id',
            'message',
            'updated_at',
            'creator'            
        )

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Like
        fields = '__all__'


class ImageSerializer(TaggitSerializer, serializers.ModelSerializer):

    comments = CommentSerializer(many=True)
    creator = FeedUserSerializer()
    tags = TagListSerializerField()
	# Meta에서 fields로 불러온 필드 중, 시리얼라이저로 nested 하게 표현하고 싶은 필드를
    # 구체적으로 골라서 위에 작성함

    class Meta:
        model = models.Image
        fields = 'id', 'created_at', 'updated_at', 'file', 'location', 'caption', 'creator', 'comments', 'like_count', 'tags'

class CountImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = 'id', 'file', 'like_count', 'comment_count'

class InputImageSerializer(TaggitSerializer, serializers.ModelSerializer):

    # file = serializers.FileField(required=False)
    # 이 serializer를 이미지 업로드에도 사용할거라 시리얼라이저 자체에서 필수여부를 빼는건 좋지 않음
    # 따라서 view에서 부분 수정 가능하게 할 것임

    tags = TagListSerializerField(required=False)

    class Meta:
        model = models.Image
        fields = (
            'file',
            'location',
            'caption',
            'tags',
        )