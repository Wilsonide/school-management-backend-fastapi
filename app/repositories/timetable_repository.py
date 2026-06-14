from sqlalchemy import select

from app.models.timetable import Timetable


class TimetableRepository:
    async def create(self, db, entry):
        db.add(entry)
        await db.commit()
        await db.refresh(entry)
        return entry

    async def get_by_class(self, db, class_id: str):
        result = await db.execute(
            select(Timetable)
            .where(Timetable.class_id == class_id)
            .order_by(Timetable.day_of_week),
        )
        return result.scalars().all()

    async def delete(self, db, entry_id: str):
        result = await db.execute(select(Timetable).where(Timetable.id == entry_id))
        entry = result.scalar_one_or_none()

        if entry:
            await db.delete(entry)
            await db.commit()

        return entry


timetable_repo = TimetableRepository()
