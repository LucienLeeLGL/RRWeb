from django.core.mail import send_mail

from rrsite.models import EmailVerifyRecord
from rrsite.util.string import random_str
from RRWeb.settings import EMAIL_FROM


def send_register_email(email, send_type="register"):
    try:
        email_title = "RRWeb网站注册"
        code = random_str(16)
        email_body = "点击下面链接激活RRWeb账号：http://58.87.109.246/email/verify/{0}?email={1}".format(code, email)
        result = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if result == 1:
            email_record = EmailVerifyRecord()
            email_record.code = code
            email_record.email = email
            email_record.send_type = send_type
            email_record.save()
            return 1
        else:
            return 0
    except Exception as e:
        print(e)
        return -1


def send_forgot_email(email, send_type='forget'):
    try:
        email_title = "RRWeb验证码"
        code = random_str(4)
        email_body = "您的验证码为：  {0}".format(code)
        result = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if result == 1:
            email_record = EmailVerifyRecord()
            email_record.code = code
            email_record.email = email
            email_record.send_type = send_type
            email_record.save()
            return 1
        else:
            return 0
    except Exception as e:
        print(e)
        return -1
