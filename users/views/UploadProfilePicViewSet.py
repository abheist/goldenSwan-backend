import cloudinary
import cloudinary.api
import cloudinary.uploader
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView


class UploadProfilePicView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            result = cloudinary.uploader.upload(request.FILES['profile_pic'])
            request.user.profile_pic = result
            request.user.save()
            return Response({'pic_url': result.get('secure_url')}, status=status.HTTP_200_OK)
        else:
            return Response(status.HTTP_401_UNAUTHORIZED)
