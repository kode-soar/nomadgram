from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers
from nomadgram.notifications import views as notification_views
from nomadgram.users import serializers as user_serializers
from nomadgram.users import models as user_models

class Images(APIView):

    def get(self, request, format = None):

        user = request.user
        following_users = user.following.all()

        image_list = []

        for following_user in following_users:
            user_images = following_user.images.all()[:2]
            for image in user_images:
                image_list.append(image)

        my_images = user.images.all()[:2]

        for image in my_images:
            image_list.append(image)

        # sorted_list = sorted(image_list, key=get_key, reverse=True) # 일반 함수 사용 외부에 함수 정의 필요
        sorted_list = sorted(image_list, key = lambda image: image.created_at, reverse = True) # 람다함수 사용
        serializer = serializers.ImageSerializer(sorted_list, many = True)

        return Response(serializer.data, status = status.HTTP_200_OK)

    # def get_key(image):
    #     return image.created_at

    def post(self, request, format = None):
        
        user = request.user

        serializer = serializers.InputImageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(creator=user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikeImage(APIView):

    def get(self, request, image_id, format = None):

        user = request.user

        likes = models.Like.objects.filter(image__id = image_id)
        creator_ids = likes.values('creator_id')
        creators = user_models.User.objects.filter(id__in=creator_ids)

        if likes.count() == 0:
            return Response(status = status.HTTP_404_NOT_FOUND)

        serializer = user_serializers.ListUserSerializer(creators, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request, image_id, format = None):

        user = request.user

        try:
            found_image = models.Image.objects.get(id = image_id) # obejcts.get()은 1개의 값만 조회할 때 사용
            
        except models.Image.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

        try:
            preexisting_like = models.Like.objects.get(
                creator = user,
                image = found_image
            )

            return Response(status = status.HTTP_304_NOT_MODIFIED)

        except models.Like.DoesNotExist:
            new_like = models.Like.objects.create(
                creator = user,
                image = found_image
            )
            new_like.save()

            notification_views.create_notification(user, found_image.creator, 'like', found_image)

            return Response(status = status.HTTP_201_CREATED)

class UnLikeImage(APIView):

    def delete(self, request, image_id, format = None):

        user = request.user

        try:
            found_image = models.Image.objects.get(id = image_id) # obejcts.get()은 1개의 값만 조회할 때 사용
        except models.Image.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

        try:
            preexisting_like = models.Like.objects.get(
                creator = user,
                image = found_image
            )

            preexisting_like.delete()

            return Response(status = status.HTTP_204_NO_CONTENT)

        except models.Like.DoesNotExist:

            return Response(status = status.HTTP_304_NOT_MODIFIED)



class CommentOnImage(APIView):

    def post(self, request, image_id, format = None):

        user = request.user
        serializer = serializers.CommentSerializer(data = request.data)

        try:
            found_image = models.Image.objects.get(id = image_id) # obejcts.get()은 1개의 값만 조회할 때 사용

        except models.Image.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():

            serializer.save(creator = user, image = found_image)

            notification_views.create_notification(user, found_image.creator, 'comment', found_image, serializer.data['message'] )
            # request시, body에 {"message" : 메세지} 형식으로 요청
            return Response(data = serializer.data, status = status.HTTP_201_CREATED)

        else:
            return Response(data = serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class Comment(APIView):

    def delete(self, request, comment_id, format=None):
        
        user = request.user
        
        try:
            comment = models.Comment.objects.get(id=comment_id, creator=user)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class Search(APIView):

    def get(self, request, format = None):

        hashtags = request.query_params.get('hashtags', None)
        # http://127.0.0.1:8000/images/search/?hashtags=aaa 처럼 get 방식으로 주소에 검색어 키, 값 넘기면
        # 아래와 같이 request.query_paramas 통해서 url의 get 키, 값 받아옴
        # request.query_params.get('hashtags', None)
        # 이 경우 print(hashtags) -> aaa

        if hashtags != None:
            hashtags = hashtags.split(",") # , 기준으로 구분하여 array에 담아서 반환
            images = models.Image.objects.filter(tags__name__in=hashtags).distinct()
            serializer = serializers.CountImageSerializer(images, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ModerateComments(APIView):

    def delete(self, request, image_id, comment_id, format=None):
        
        user = request.user

        try:
            comment = models.Comment.objects.get(id=comment_id, image__id=image_id, image__creator=user)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except models.Comment.DoesNotExist :
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class ImageDetail(APIView):

    def find_own_image(self, image_id, user):
        try:
            image = models.Image.objects.get(id=image_id, creator=user)
            return image
        except models.Image.DoesNotExist:
            return None

    def get(self, request, image_id, format=None):
        
        try:
            image = models.Image.objects.get(id=image_id)
            serializer = serializers.ImageSerializer(image)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        except models.Image.DoesNotExist :
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, image_id, format=None):
        
        user = request.user
        image = self.find_own_image(image_id, user)

        if image is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
            
        serializer = serializers.InputImageSerializer(image, data=request.data, partial=True)
        # partial=True 사용하면, 필수 값이더라도 제외하고 부분적으로 입력가능

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, image_id, format=None):
        
        user = request.user
        image = self.find_own_image(image_id, user)

        if image is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        image.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
