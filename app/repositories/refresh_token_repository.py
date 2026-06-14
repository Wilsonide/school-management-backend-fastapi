from sqlalchemy import select

from app.models.refresh_token import RefreshToken


class RefreshTokenRepository:

    async def create(self, db, token):
        db.add(token)
        await db.commit()
        await db.refresh(token)
        return token

    async def get_by_hash(self, db, token_hash: str):
        result = await db.execute(
            select(RefreshToken).where(
                RefreshToken.token_hash == token_hash
            )
        )

        return result.scalar_one_or_none()

    async def revoke(self, db, token):

        token.revoked = True

        await db.commit()

        return token
    
refresh_token_repo = RefreshTokenRepository()