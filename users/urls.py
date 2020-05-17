from django.urls import path

from users.views.UploadProfilePicViewSet import UploadProfilePicView

urlpatterns = [
    path('upload-profile-pic', UploadProfilePicView.as_view())
]
