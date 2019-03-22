from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers
from rest_framework.decorators import api_view
from nomadgram.notifications import views as notification_views
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView


class ExploreUsers(APIView):

    def get(self, request, format = None):

        last_five = models.User.objects.all().order_by('-date_joined')[:5]
        serializer = serializers.ListUserSerializer(last_five, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

class FollowUsers(APIView):

    def post(self, request, user_id, format = None):

        user = request.user

        try:
            user_to_follow = models.User.objects.get(id=user_id)

        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.following.add(user_to_follow)
        user.save()

        user_to_follow.followers.add(user)
        user_to_follow.save()

        notification_views.create_notification(user, user_to_follow, 'follow')

        return Response(status=status.HTTP_200_OK)

class UnFollowUsers(APIView):

    def delete(self, request, user_id, format = None):

        user = request.user

        try:
            user_to_follow = models.User.objects.get(id=user_id)

        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.following.remove(user_to_follow)
        user.save()

        user_to_follow.followers.remove(user)
        user_to_follow.save()

        return Response(status=status.HTTP_200_OK)

class UserProfile(APIView):

    def get_user(self, username):

        try:
            found_user = models.User.objects.get(username=username)
            return found_user

        except models.User.DoesNotExist:
            return None

    def get(self, request, username, format = None):

        found_user = self.get_user(username)

        if found_user is None:

            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.UserProfileSerializer(found_user)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, username, format = None):

        user = request.user
        found_user = self.get_user(username)

        if found_user is None:

            return Response(status=status.HTTP_404_NOT_FOUND)

        elif found_user != user:
        # elif found_user.username != user.username:

            return Response(status=status.HTTP_401_UNAUTHORIZED)

        else:
            serializer = serializers.UserProfileSerializer(found_user, data=request.data, partial=True)
        
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)

            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserFollowers(APIView):

    def get(self, request, username, format = None):

        try:
            found_user = models.User.objects.get(username=username)

        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.ListUserSerializer(found_user.followers.all(), many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

class UserFollowing(APIView):
    
    def get(self, request, username, format = None):

        try:
            found_user = models.User.objects.get(username=username)

        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.ListUserSerializer(found_user.following.all(), many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def UserFollowingFBV(request, username):
    if request.method == 'GET':

        try:
            found_user = models.User.objects.get(username=username)

        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.ListUserSerializer(found_user.following.all(), many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':

        try:
            found_user = models.User.objects.get(username=username)

        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.ListUserSerializer(found_user.following.all(), many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class Search(APIView):

    def get(self, request, format = None):

        username = request.query_params.get('username', None)
        # http://127.0.0.1:8000/users/search/?username=aaa 처럼 get 방식으로 주소에 검색어 키, 값 넘기면
        # 아래와 같이 request.query_paramas 통해서 url의 get 키, 값 받아옴
        # request.query_params.get('username', None)
        # 이 경우 print(username) -> aaa

        if username != None:
            users = models.User.objects.filter(username__istartswith=username)
            serializer = serializers.ListUserSerializer(users, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class ChangePassword(APIView):
    
   def put(self, request, format = None):

        user = request.user
        current_password = request.data.get('current_password', None)

        if current_password is not None:

            passwords_match = user.check_password(current_password) 
            # True, False 로 결과 나옴

            if passwords_match:

                new_password = request.data.get('new_password', None)

                if new_password is not None:

                    user.set_password(new_password)
                    user.save()
                    return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter