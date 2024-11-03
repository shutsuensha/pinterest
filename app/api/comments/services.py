from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import CommentCreateRequest
from app.api.pins.services import PinService
from app.api.users.services import UserService
from app.database.models import Comment

pin_service = PinService()
user_service = UserService()


class CommentService:
    async def create_comment(user_uid: str,
                              pin_uid: str, 
                              comment_data: CommentCreateRequest, 
                              session: AsyncSession
    ):
        pin = await pin_service.get_pin_by_uid(pin_uid, session)
        user = await user_service.get_user_by_uid(user_uid)

        comment_data_dict = comment_data.model_dump()
        new_comment = Comment(**comment_data_dict)

        new_comment.user = user
        new_comment.pin = pin

        await session.commit()

        return new_comment