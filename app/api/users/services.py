from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.database.models import User
from .schemas import UserCreateModel
from .utils import get_password_hash, create_url_safe_token, decode_url_safe_token, verify_password
from app.config import settings
from app.celery_tasks.celery import send_email
from fastapi import HTTPException, status


class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)

        result = await session.exec(statement)

        user = result.first()

        return user
    

    async def get_user_by_uid(self, user_uid: str, session: AsyncSession):
        statement = select(User).where(User.uid == user_uid)

        result = await session.exec(statement)

        user = result.first()

        return user
    

    async def get_user_by_username(self, username: str, session: AsyncSession):
        statement = select(User).where(User.username == username)

        result = await session.exec(statement)

        user = result.first()

        return user


    async def user_exists(self, email: str, session: AsyncSession):
        user = await self.get_user_by_email(email, session)

        return user is not None
    

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()

        new_user = User(**user_data_dict)

        new_user.password_hash = get_password_hash(user_data_dict["password"])

        session.add(new_user)

        await session.commit()

        return new_user
    

    async def update_user(self, user: User , user_data: dict, session: AsyncSession):

        for k, v in user_data.items():
            setattr(user, k, v)

        await session.commit()

        return user


    def send_verification(self, email: str):
        token = create_url_safe_token({"email": email})

        link = f"http://{settings.DOMAIN}/api/v1/users/verify/{token}"

        html_message = f"""
        <h1>Verify your Email</h1>
        <p>Please click this <a href="{link}">link</a> to verify your email</p>
        """

        emails = [email]

        subject = "Verify Your email"

        send_email.delay(emails, subject, html_message)

    def send_password_reset(self, email: str, password: str):
        token = create_url_safe_token({"email": email, "password": password})

        link = f"http://{settings.DOMAIN}/api/v1/users/password-reset-confirm/{token}"

        html_message = f"""
        <h1>Reset Your Password</h1>
        <p>Please click this <a href="{link}">link</a> to Reset Your Password</p>
        """
        subject = "Reset Your Password"

        send_email.delay([email], subject, html_message)


    async def verify_user(self, token: str, session: AsyncSession):
        token_data = decode_url_safe_token(token)

        user_email = token_data['email']

        user = await self.get_user_by_email(user_email, session)

        updated_user = await self.update_user(user, {"is_verified": True}, session)

        return updated_user
    

    async def confirm_password_reset(self, token: str, session: AsyncSession):
        token_data = decode_url_safe_token(token)

        user_email = token_data['email']
        password = token_data['password']

        user = await self.get_user_by_email(user_email, session)

        passwd_hash = get_password_hash(password)

        updated_user = await self.update_user(user, {"password_hash": passwd_hash}, session)

        return updated_user
    
    

    async def authenticate_user(self, session: AsyncSession, email: str, password: str):
        user = await self.get_user_by_email(email, session)
        
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        # Verify the password
        if not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password doesn't match")
        
        # Check if the user is verified
        if not user.is_verified:
            self.send_verification(email)
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not verified, Verification link is send")
        
        return user
    

    async def simple_authenticate_user(self, session: AsyncSession, username: str, password: str):
        user = await self.get_user_by_username(username, session)
        
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        # Verify the password
        if not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password doesn't match")
        
        return user
    


