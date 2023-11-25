#!/usr/bin/env python3
#  module for email configurations
#  written by Hamza <-cyberguru->
#  Team Harchive

from fastapi import HTTPException
from starlette import status
from config.config import settings
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from itsdangerous import URLSafeTimedSerializer, BadTimeSignature, SignatureExpired
from jinja2 import Environment, select_autoescape, PackageLoader
from pydantic import EmailStr, BaseModel
from typing import List


env = Environment(
    loader=PackageLoader('app', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

token_algo= URLSafeTimedSerializer(settings.jwt_secret_key,
                                   salt='Email_Verification_&_Forgot_password')

class EmailSchema(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    email: List[EmailStr]

class Email:
    def __init__(self, name: str, token: str, email: List[EmailStr]):
        self.name = name
        self.sender = 'Harchvie <admin@harchive.com>'
        self.email = email
        self.token = token
        pass

    async def sendMail(self, subject_feild, template):
        """_summary_

        Args:
            subject (_type_): subject details
            template (_type_): jinja2 template
        """
        conf = ConnectionConfig(
            MAIL_USERNAME=settings.EMAIL_USERNAME,
            MAIL_PASSWORD=settings.EMAIL_PASSWORD,
            MAIL_FROM=settings.EMAIL_FROM,
            MAIL_PORT=settings.EMAIL_PORT,
            MAIL_SERVER=settings.EMAIL_HOST,
            MAIL_STARTTLS=False,
            MAIL_SSL_TLS=True,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True
        )
        #  Generate the HTML template

        template = env.get_template(f'{template}.html')

        html = template.render(
            token_url=self.token,
            first_name=self.name,
            subject=subject_feild
        )

        # define the message options

        message = MessageSchema(
            subject=subject_feild,
            recipients=self.email,
            body=html,
            subtype="html"
        )

        # Send mail

        fm = FastMail(conf)
        await fm.send_message(message)

    async def sendVerificationCode(self):
        await self.sendMail("Your Verification code (Valid for 10min)", 'verification')

    async def sendResetPassword(self):
        await self.sendMail("Your Password Reset Link (Valid for 10min)", 'reset_password')

def generateToken(email: List[EmailStr]):
    """_summary_

    Args:
        email (List[EmailStr]): user email
    """
    _token = token_algo.dumps(email)

    return _token

def verifyToken(token: str):
    """_summary_

    Args:
        token (str): token to be verified
    """
    try:
        email = token_algo.loads(token, max_age=600)

    except BadTimeSignature:
        return None
    
    except SignatureExpired:
        return None

    return {'email':email, 'verified': True}

async def verifyEmail(email, http_request, request):
    try:
        token = generateToken(email)
        token_url =  f"{http_request.url.scheme}://{http_request.client.host}:{http_request.url.port}/auth/verifyemail/{token}"
        await Email(request.name, token_url, [email]).sendVerificationCode()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=[{
                                'msg':'There was an error sending email, please check your email address!',
                                "error": f"{e}"
                                }])
    
    return "Verification email sent successfully"
