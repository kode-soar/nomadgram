from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers

class Notifications(APIView):
    def get(self, request, format = None):
        
        notifications = models.Notification.objects.filter(to=request.user)
        
        #if len(notifications) == 0:
        if notifications.count() == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.NotificationSerializer(notifications, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

def create_notification(creator, to, type, image = None, comment = None):

    notification = models.Notification.objects.create(
        creator = creator,
        to = to,
        notification_type = type,
        image = image,
        comment = comment,
    )

    notification.save()