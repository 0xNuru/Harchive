#!/usr/bin/python3


from utils.logger import logger
from utils.oauth1 import AuthJWT
from utils import auth
from typing import List
from starlette import status
from sqlalchemy.orm import Session
from schema import user as userSchema
from models import user as userModel
from models import patient as patientModel
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi import APIRouter, Depends, HTTPException, Response, Request
from engine.loadb import load
from dependencies.depends import get_current_user
import sys
from utils.email import Email, generateToken, verifyToken
from jinja2 import Environment, select_autoescape, PackageLoader
from utils.auth import oauth, OAuthError
from utils import acl, utime
from utils.email import verifyEmail
from utils.cache import json_cache

sys.path.insert(0, '..')


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

env = Environment(
    loader=PackageLoader('app', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

@router.get('/verifyemail/{token}')
def verify_token(token: str, db: Session = Depends(load)):
    """_summary_

    Args:
        token (str): _description_
        db (Session, optional): _description_. Defaults to Depends(load).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    result = verifyToken(token)

    if not result:

        # to do remove user details if existing

        cached_data = json_cache.get(token)

        if cached_data :
            user = db.query_eng(userModel.Users).filter(
                userModel.Users.email == cached_data.lower()).first()
            print(user)
            db.delete(user)
            db.save()
            
            # remove user cached details
            json_cache.delete(token)
        print("CachedData: ", cached_data)


        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=[{"message":"Token for Email Verification has expired."}])
    else:
        email = result['email']
        user_model = db.query_eng(userModel.Users).filter(
            userModel.Users.email == email).first()
        if user_model is None:
            return {
                "status": "Failed",
                "message": "Error in Verifying Account!"
            }
        user_model.is_verified = True
        db.update(user_model)
        db.save()

        # remove user cached details
        json_cache.delete(token)
        
    return  {
        "status": "success",
        "message": "Account verified successfully"
    }


@router.post('/forgot_password', status_code=status.HTTP_200_OK)
async def forgot_password(request: userSchema.forgotPassword,
                    req: Request,
                    db: Session = Depends(load))-> None:
    email = request.email

    user_check = db.query_eng(userModel.Users).filter(
        userModel.Users.email == email).first()

    if not user_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=[{"msg":f"user with email: {email} does not exists"}])
    try:
        token = generateToken(email)
        token_url =  f"{req.url.scheme}://{req.client.host}:{req.url.port}/user/reset_password/{token}"
        await Email(user_check.name, token_url, [email]).sendResetPassword()

    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=[{'msg':'There was an error sending email, please check your email address!'}])
    return {
        "status": "success",
        "message": "Recovery Email sent successfully"
    }
    

@router.get('/reset_password/{token}')
def reset_password(token: str, req: Request, db: Session = Depends(load)):

    result = verifyToken(token)

    if not result:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=[{"msg":"Token for Email Verification has expired."}])

    template = env.get_template(f'reset_password_markup.html')

    token_url =  f"{req.url.scheme}://{req.client.host}:{req.url.port}/user/reset_password/{token}"
    
    html = template.render(
        token_link=token_url
        )
        
    return  HTMLResponse(html)

@router.post('/reset_password/{token}')
def reset_password(request: userSchema.resetPassword, token: str, db: Session = Depends(load)):

    result = verifyToken(token)

    if not result:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=[{"msg":"Token for Email Verification has expired."}])
    else:
        email = result['email']
        user_model = db.query_eng(userModel.Users).filter(
            userModel.Users.email == email).first()
        
        del request.rPassword1
        passwd_hash = auth.get_password_hash(request.rPassword2.get_secret_value())

        user_model.password_hash = passwd_hash
        db.update(user_model)
        db.save()
        
    return  {
        "status": "success",
        "message": "Password reset successfully"
    }

# login endpoint
@router.post('/login', status_code=status.HTTP_200_OK)
async def login(response: Response, request: userSchema.UserLogin = Depends(),
          Authorize: AuthJWT = Depends(), db: Session = Depends(load)):
    duration = 3 # current timeout duration is 3 minutes
    tryalls = 3 # current maximum retry is 3 times
    email = request.email.lower()
    password = request.password._secret_value

    check = db.query_eng(userModel.Users).filter(
        userModel.Users.email == email).first()

    if not check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=[{"msg":f"Incorrect Username or Password"}])
    
    # check if user is currently suspended 
    # current timeout value: 3 minutes
    
    if check.is_suspended and not utime.compare_time(check.suspended_at, duration):
        # get the remaining time left
        minute, secs = utime.getRemain_time(check.suspended_at, duration)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=[{"msg":f"Maximum login limit reached, try again in {minute} min {secs} secs"}])

    # check if user is currently suspended 
    # And compare the duration of suspension

    if check.is_suspended and utime.compare_time(check.suspended_at, duration):
        acl.reset_user_state(email) # reset user state if timeout is reached

    patient = db.query_eng(patientModel.Patient).filter(
        patientModel.Patient.id == check.id).first()

    if not auth.verify_password(password, check.password_hash):
        # initiate jail login 
        acl.update_max_trys(email, tryalls)
        remain_tryalls = tryalls - check.failed_login_attempts
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=[{'msg':f'Incorrect Username or Password, {remain_tryalls} trys remainning'}])

    # reset max login retry after succesfull login
    if  check.failed_login_attempts is not None or check.failed_login_attempts > 0 :
        acl.reset_user_state(email)
    
    if not check.is_verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=[{'msg':'User not verified, please verify your email to continue'}])

    data = {
        'username': check.name,
        'email': check.email,
        'user_id': check.id,
        'role': check.role
    }

    if patient:
        data['nin'] = patient.nin
    else:
        data['nin'] = None

    # generate user cookies
    access_token = auth.access_token(data)
    refresh_token = auth.refresh_token(data)

    # # save tokens in the cookies
    auth.set_access_cookies(access_token, response)
    auth.set_refresh_cookies(refresh_token, response)

    
    return {
        "status": "success",
        "message": "user logged in successfully",
        "tokens": {
            "access_token": access_token,
            "refresh_token": refresh_token
            }
        }

@router.get('/refresh')
async def refresh(request: Request,
                  response: Response,
                  Authorize: AuthJWT = Depends(),
                  db: Session = Depends(load)):

    try:

        Authorize.jwt_refresh_token_required()

        user_email = Authorize.get_jwt_subject()

        if not user_email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=[{'msg':'Could not refresh access token'}])

        check = db.query_eng(userModel.Users).filter(
            userModel.Users.email == user_email).first()

        if not check:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=[{'msg':'The user belonging to this token no logger exist'}])
    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            redirect_url = request.url_for('login')
            
            return JSONResponse(content={
                "redirect_url": redirect_url,
                "redirect": True
                }, status_code=307)
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    data = {
        'username': check.name,
        'email': check.email,
        'user_id': check.id

    }

    # generate user cookies
    access_token = auth.access_token(data)

    # save tokens in the cookies
    auth.set_access_cookies(access_token, response)

    return {
            "status": "success",
            "message": "refreshed successfully!!",
            "tokens": {
                "access_token": access_token,
                }
            }

# login with google endpoint
@router.route('/auth/login_with_google')
async def login(request: Request):
    """_summary_: 
                 Endpoint used to login a user using google account credentials
                 To use this endpoint, copy the request link to your browser; this 
                 is because it does not work directly from fastapi swagger!

    Args:
        request (Request): _description_

    Returns:
        _type_: _description_
    """
    redirect_url = request.url_for('auth_google_login')
    return await oauth.google.authorize_redirect(request, redirect_url)


@router.get('/auth_google_login')
async def auth_google_login(request: Request,
                            db: Session = Depends(load)):
    """_summary_:
                  Endpoint where google redirects the user to after authentication
                  from google ends, input parameters are token used to get userinfo.
                  Won't work from fastapi swagger openai.json interface
    Args:
        request (Request): _description_
        db (Session, optional): _description_. Defaults to Depends(load).
        
    Returns:
        _type_: json object
    """

    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        return RedirectResponse(request.url_for('login'))
    
    access_token_decoded =  dict(access_token)
    user_data = access_token_decoded['userinfo']

    email = user_data['email']

    check = db.query_eng(userModel.Users).filter(
        userModel.Users.email == email).first()

    if not check:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=[{"msg":f"User not registered, please create an account"}])
        
    patient = db.query_eng(patientModel.Patient).filter(
        patientModel.Patient.id == check.id).first()
    
    data = {
        'username': check.name,
        'email': check.email,
        'user_id': check.id,
        'role': check.role
    }

    if patient:
        data['nin'] = patient.nin
    else:
        data['nin'] = None

    # generate user cookies
    access_token = auth.access_token(data)
    refresh_token = auth.refresh_token(data)

    # save tokens in the cookies
    logger.info(f" {check.name} logged in !!")

    return {
        "status": "success",
        "message": "user logged in successfully",
        "tokens": {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        }

@router.get('/logout', status_code=status.HTTP_200_OK)
def logout(response: Response, Authorize: AuthJWT = Depends()):
    Authorize.unset_jwt_cookies()
    response.set_cookie("logged_in", '', -1)
    return RedirectResponse(url = '/auth/login')  #  remember to use frontend url for login in here (error otherwise)
