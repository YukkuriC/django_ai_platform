from django.db import models
from django.contrib.auth.hashers import make_password, check_password, hashlib
from django.conf import settings
from main.helpers import set_autodelete


### models
class User(models.Model):
    username = models.CharField('用户名', max_length=20, unique=True)
    pw_hash = models.CharField('密码hash', max_length=128)
    stu_code = models.CharField('学号', max_length=10)
    real_name = models.CharField('真实姓名', max_length=32)
    register_datetime = models.DateTimeField('注册时间')
    login_datetime = models.DateTimeField('上次登录时间', null=True)
    email_validated = models.BooleanField('已验证电子邮箱', default=False)

    def __str__(self):
        return '%s (%s, %s)' % (self.username, self.real_name, self.stu_code)

    def match_passwd(self, pw):
        return check_password(pw, self.pw_hash)

    def set_passwd(self, pw):
        self.pw_hash = make_password(pw)
        self.save()

    class Meta:
        ordering = ["stu_code"]
        verbose_name = "用户"
        verbose_name_plural = "用户"


class UserMailCheck(models.Model):
    user = models.OneToOneField(User, models.CASCADE, verbose_name='用户')
    send_time = models.DateTimeField('请求时间')
    check_hash = models.CharField('校验hash', max_length=256)

    def activate(self):
        hasher = hashlib.sha256()
        hash_str = self.user.stu_code
        hash_str += self.user.register_datetime.strftime("%Y%m%d%H%I%S")
        hash_str += self.send_time.strftime("%Y%m%d%H%I%S")
        hasher.update(hash_str.encode())
        self.check_hash = hasher.hexdigest()
        self.save()