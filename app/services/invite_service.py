import uuid

from app.models.invite import Invite
from app.repositories.invite_repository import InviteRepository
from app.services.email_service import EmailService


class InviteService:
    def __init__(self):
        self.repo = InviteRepository()
        self.email_service = EmailService()

    def generate_code(self):
        return f"LERNA-{uuid.uuid4().hex[:8].upper()}"

    async def create_auto_invite(self, db, email: str, role: str, school_id: str):
        invite = Invite(
            email=email,
            role=role,
            school_id=school_id,
            code=self.generate_code(),
            is_used=False,
        )

        invite = await self.repo.create(db, invite)

        # send email automatically
        self.email_service.send_invite(email, invite.code)

        return invite

    async def get_by_code(self, db, code: str):
        return await self.repo.get_by_code(db, code)

    async def mark_used(self, db, invite):
        invite.is_used = True
        await db.commit()
        return invite


inviteservice = InviteService()
