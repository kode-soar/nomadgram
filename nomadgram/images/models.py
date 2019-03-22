from django.db import models
from nomadgram.users import models as user_models
# from django.utils.encoding import python_2_unicode_compatible
from taggit.managers import TaggableManager

#@python_2_unicode_compatible
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        # abstract base class 설정 -> 다른 class model 정의 시 사용
        # abstract base 클래스는 DB와 연결 X
        # model metadata is "anything that's not a field"
        # ex) ordering options, database table name, other information...

#@python_2_unicode_compatible
class Image(TimeStampedModel):

    """ Image Model """
    file = models.ImageField()
    location = models.CharField(max_length=140)
    caption = models.TextField()
    creator = models.ForeignKey(user_models.User, on_delete=models.PROTECT, null=True, related_name='images')
    tags = TaggableManager()

    @property
    def like_count(self):
        return self.likes.all().count()

    @property
    def comment_count(self):
        return self.comments.all().count()

    def __str__(self): #Image에서 반환할(Admin에서 표시될 Image 객체의) 표현 방법 정의
        return '{} - {}'.format(self.location, self.caption)

    class Meta:
        ordering = ['-created_at']

#@python_2_unicode_compatible
class Comment(TimeStampedModel):

    """ Comment Model """

    message = models.TextField()
    creator = models.ForeignKey(user_models.User, on_delete=models.PROTECT, null=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, related_name='comments')

    def __str__(self): #Admin에서 표시될 Comment 객체의 표현 방법 정의
        return self.message

#@python_2_unicode_compatible
class Like(TimeStampedModel):

    """ Like Model """

    creator = models.ForeignKey(user_models.User, on_delete=models.PROTECT, null=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, related_name='likes')
    
    def __str__(self): #Admin에서 표시될 Like 객체의 표현 방법 정의
        return 'User: {} - Image Caption: {}'.format(self.creator.username, self.image.caption)