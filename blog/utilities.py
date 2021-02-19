from django.conf import settings
from django.core.mail import send_mail


def email_subscriber(email, blog_title, post_url):
    subject = 'Новый пост от %s' % blog_title
    message = f'''
        В вашей ленте новый пост. 
        Ссылка на пост - {post_url} .
    '''
    email_from = settings.EMAIL_HOST_USER
    email_to = [email]
    send_mail(subject, message, email_from, email_to)
