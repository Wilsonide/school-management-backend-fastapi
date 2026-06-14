from app.models.classes import Class
from app.repositories.school_class_repository import SchoolClassRepository


class SchoolClassService:
    def __init__(self):
        self.repo = SchoolClassRepository()

    async def create_class(self, db, data, school_id: str):
        cls = Class(
            name=data["name"],
            level=data.get("level"),
            school_id=school_id,
        )

        return await self.repo.create(db, cls)

    async def get_classes(self, db, school_id: str):
        return await self.repo.get_by_school(db, school_id)

    async def delete_class(self, db, class_id: str):
        return await self.repo.delete(db, class_id)

    async def get_class_dashboard(
        self,
        db,
        class_id,
    ):
        return await self.repo.get_class_dashboard(
            db,
            class_id,
        )


school_class_service = SchoolClassService()
