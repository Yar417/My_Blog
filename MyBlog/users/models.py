from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.ImageField('User Photo',
                            default='icon_user.png',
                            upload_to='user_img')
    choice = (
        ('male', 'Мужской пол'),
        ('female', 'Женский пол'),
        ('neutral', 'Гендерно-нейтральный'),
        ('other', 'Другой пол'),
    )
    gender = models.CharField(choices=choice, max_length=7, default='other')

    notifications = models.BooleanField(
        verbose_name=None,
        default=True,
    )

    def __str__(self):
        return f'User profile: {self.user.username}'

    def save(self, *args, **kwargs):
        super().save()

        image = Image.open(self.img.path)
        if image.height > 256 or image.width > 256:
            resize = (256, 256)
            image.thumbnail(resize)
            image.save(self.img.path)
