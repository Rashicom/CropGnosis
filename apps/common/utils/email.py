from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class Email:
    def __init__(self):
        pass

    def send_email(
            self,
            subject:str=None,
            to:list=[],
            html_template:str=None,
            data:dict={},
            attachment_path:str=None,
            from_email:str=settings.EMAIL_HOST_USER
            ):

        if subject is None or len(to)==0 or html_template is None:
            raise Exception("Insufficient arguments for send_email")

        msg = EmailMultiAlternatives(
            subject,
            "CropGnosis",
            from_email,
            to,
        )

        # TODO:attach attachment path

        # render is there any variable
        # TODO: render variables like otp
        html_content = render_to_string(html_template, data)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
