from django.db import models
from django.contrib.auth.models import User


class UserText(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)


def user_directory_path(instance, filename):
    # 文件将被上传到 MEDIA_ROOT/user_<username>/<filename>
    return 'userFiles/user_{0}/{1}'.format(instance.user.username, filename)


class UserFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)
