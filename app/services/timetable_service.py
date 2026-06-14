from app.models.timetable import Timetable
from app.repositories.timetable_repository import timetable_repo


class TimetableService:
    def __init__(self):
        self.repo = timetable_repo

    async def create_entry(
        self,
        db,
        class_id: str,
        subject_id: str,
        teacher_id: str,
        day_of_week: str,
        start_time,
        end_time,
        school_id: str,
    ):
        entry = Timetable(
            class_id=class_id,
            subject_id=subject_id,
            teacher_id=teacher_id,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            school_id=school_id,
        )

        return await self.repo.create(db, entry)

    async def get_class_timetable(self, db, class_id: str):
        entries = await self.repo.get_by_class(db, class_id)
        return {
            "entries": [
                {
                    "id": e.id,
                    "day_of_week": e.day_of_week,
                    "start_time": str(e.start_time),
                    "end_time": str(e.end_time),
                    "subject": e.subject.name if e.subject else None,
                    "teacher": (
                        f"{e.teacher.first_name} {e.teacher.last_name}"
                        if e.teacher
                        else None
                    ),
                }
                for e in entries
            ]
        }

    async def delete_entry(self, db, entry_id: str):
        return await self.repo.delete(db, entry_id)


timetable_service = TimetableService()
