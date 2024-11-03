from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import CommentCreateRequest
from app.api.pins.services import PinService
from app.api.users.services import UserService
from app.database.models import Comment
from sqlmodel import select
from app.database.models import Comment

pin_service = PinService()
user_service = UserService()


class CommentService:
    async def create_comment(self, user_uid: str,
                              pin_uid: str, 
                              comment_data: CommentCreateRequest, 
                              session: AsyncSession
    ):
        pin = await pin_service.get_pin_by_uid(pin_uid, session)
        user = await user_service.get_user_by_uid(user_uid, session)

        comment_data_dict = comment_data.model_dump()
        new_comment = Comment(**comment_data_dict)

        new_comment.user = user
        new_comment.pin = pin

        session.add(new_comment)

        await session.commit()

        return new_comment
    
    async def create_reply(self, comment_uid: str, user_uid: str, comment_data: CommentCreateRequest, session: AsyncSession):
        comment = await self.get_comment_by_uid(comment_uid, session)
        user = await user_service.get_user_by_uid(user_uid, session)

        comment_data_dict = comment_data.model_dump()
        new_comment = Comment(**comment_data_dict)
        new_comment.user = user
        new_comment.parent_uid = comment.uid

        session.add(new_comment)

        await session.commit()

        return new_comment
    

    async def get_comment_by_uid(self, comment_uid: str, session: AsyncSession):
        statement = select(Comment).where(Comment.uid == comment_uid)

        result = await session.exec(statement)

        comment = result.first()

        return comment
    

    async def get_all_replies(self, comment_uid: str, session: AsyncSession):
        statement = select(Comment).where(Comment.parent_uid == comment_uid)

        result = await session.exec(statement)

        return result.all()
    

    async def update_comment(self, comment: Comment , comment_data: dict, session: AsyncSession):

        for k, v in comment_data.items():
            setattr(comment, k, v)

        await session.commit()

        return comment