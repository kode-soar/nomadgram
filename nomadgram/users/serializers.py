from rest_framework import serializers
from . import models
from nomadgram.images import serializers as images_serialzers

class ListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = (
            'id',
            'profile_image',
            'username',
            'name'
        )

class UserProfileSerializer(serializers.ModelSerializer):

    images = images_serialzers.CountImageSerializer(many=True, read_only=True)
    post_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    # ReadOnlyField는 Serializer 통해서 수정 불가능하게 해줌, 하지만 위의
    # *_count는 함수로 계산된 결과라서 이 속성 없어도 수정이 안되는 것 같아 보임

    class Meta:
        model = models.User
        fields = (
            'profile_image',
            'username',
            'name',
            'bio',
            'website',
            'post_count',
            'followers_count',
            'following_count',
            'images'
        )

