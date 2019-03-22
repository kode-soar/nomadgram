from django.db import models
from nomadgram.users import models as user_models
from nomadgram.images import models as images_models

class Notification(images_models.TimeStampedModel):

    TYPE_CHOICES = ( # 기본 폼 위젯이 select box가 됨
        ('like', 'Like'), #(저장될 값, 어드민에서 표시할 이름)
        ('comment', 'Comment'),
        ('follow', 'Follow')
    )

    creator = models.ForeignKey(user_models.User, on_delete=models.PROTECT, null=True, related_name='creator')
    to = models.ForeignKey(user_models.User, on_delete=models.PROTECT, null=True, related_name='to')
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    image = models.ForeignKey(images_models.Image, on_delete=models.PROTECT, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return 'From: {} - To: {}'.format(self.creator, self.to)