from rest_framework import serializers
from . import models
from nomadgram.images import serializers as image_serializers
from nomadgram.users import serializers as user_serializers


class NotificationSerializer(serializers.ModelSerializer):
    
    image = image_serializers.SmallImageSerializer()
    creator = user_serializers.ListUserSerializer()
    
    class Meta:
        model = models.Notification
        fields = '__all__'

