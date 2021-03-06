from django.db import models
from django.core.validators import EmailValidator
import socket


class AccountType(models.Model):
    TYPES = {
        (1, 'basic'),
        (2, 'premium'),
        (3, 'enterprise')
    }
    types = models.IntegerField(default=0, choices=TYPES)

    def __str__(self):
        return f'{self.types}'


class User(models.Model):
    mail = models.CharField(unique=True, null=False, max_length=50, validators=[EmailValidator])
    account_type = models.OneToOneField(AccountType, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f'{self.mail} ({self.account_type})'


class Image(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images_links', null=False)
    photo = models.ImageField(null=False, blank=True)

    def __str__(self):
        return f'{self.photo} user: {self.user_id}'

    def link(self, type):
        image_link = f'http://{socket.gethostbyname("localhost")}:8000/imageuploader/users/{self.user_id.pk}/images/{self.pk}/{type}'
        return image_link

    def image_link(self):
        account_type = self.user_id.account_type.types
        small = 'small'
        medium = 'medium'
        original = 'original'
        if account_type == 1:
            return [self.link(small)]
        elif account_type == 2:
            return [self.link(small), self.link(medium)]
        else:
            return [self.link(small), self.link(medium), self.link(original)]


class Settings(models.Model):
    account_type = models.OneToOneField(AccountType, on_delete=models.CASCADE, null=False)
    resolution = models.IntegerField(null=False)

    def __str__(self):
        return f'{self.account_type} - {self.resolution}'





