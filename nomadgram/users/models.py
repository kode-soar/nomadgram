from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
# from django.utils.encoding import python_2_unicode_compatible

class User(AbstractUser):

    """ User Model """

    GENDER_CHOICES = ( # 기본 폼 위젯이 select box가 됨
        ('male', 'Male'), #(저장될 값, 어드민에서 표시할 이름)
        ('female', 'Female'),
        ('not-spectified', 'Not specified')
    )

    # First Name and Last Name do not cover name patterns
    # around the globe.
    profile_image = models.ImageField(null=True)
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    website = models.URLField(null=True, blank=True) # null=True 시 컬럼 생성이전의 데이터는 null이 됨
    bio = models.TextField(null=True)
    phone = models.CharField(max_length=140, null=True)
    gender = models.CharField(max_length=80, choices = GENDER_CHOICES, null=True)
    followers = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="followers_set")
    following = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="following_set")

    def __str__(self):
        return self.username #Admin에서 표시될 Like 객체의 표현 방법 정의

    @property
    def post_count(self):
        return self.images.all().count()

    @property
    def followers_count(self):
        return self.followers.all().count()

    @property
    def following_count(self):
        return self.following.all().count()
