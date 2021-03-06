from .serializers import UserSerializer, ImageTypeSerializer
from rest_framework import viewsets
from .models import User, Image, Settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from .validators import check_account_type, check_image_type, check_image_owner
from rest_framework.response import Response
from PIL import Image as pil_image
import io


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        user = User.objects.all()
        return user

    def list(self, request, *args, **kwargs):
        return Response('This method is not allowed')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserSerializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return Response('This method is not allowed')

    def update(self, request, *args, **kwargs):
        return Response('This method is not allowed')

    def destroy(self, request, *args, **kwargs):
        return Response('This method is not allowed')


def scale_image(image, resolution):
    img = pil_image.open(image)
    hpercent = (resolution / float(img.size[1]))
    wsize = int((float(img.size[0]) * float(hpercent)))
    img = img.resize((wsize, resolution), pil_image.ANTIALIAS)
    to_return = io.BytesIO()
    img.save(to_return, 'png')
    return to_return.getvalue()


def resize_image(image, type):
    if type == 'original':
        return image
    elif type == 'small':
        settings = Settings.objects.get(account_type__types=1)
        resolution = settings.resolution
        return scale_image(image, resolution)
    elif type == 'medium':
        settings = Settings.objects.get(account_type__types=2)
        resolution = settings.resolution
        return scale_image(image, resolution)
    else:
        raise ValueError('Wrong scale type')


@api_view(['POST'])
def create_image(request, user_id):
    user = get_object_or_404(User, id=user_id)
    request_image = request.data['image']
    check_image_type(request_image.name)
    image = Image.objects.create(
            user_id=user,
            photo=request_image
        )
    return HttpResponse(f'Image added: {image.pk}')


@api_view(['GET'])
def get_image(request, user_id, image_id, type):
    user = get_object_or_404(User, id=user_id)
    image = get_object_or_404(Image, id=image_id)
    check_image_owner(user_id, image)
    check_account_type(type, user.account_type.types)
    return HttpResponse(resize_image(image.photo, type), content_type='image/png')


@api_view(['GET'])
def select_image(request, user_id, image_id):
    image = get_object_or_404(Image, id=image_id)
    check_image_owner(user_id, image)
    serializer = ImageTypeSerializer(image)
    return Response(serializer.data)
