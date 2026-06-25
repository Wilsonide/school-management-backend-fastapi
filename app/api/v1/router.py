from fastapi import APIRouter

from . import admin, auth, blog, profile,students,teacher, school_admin, user, academic

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(user.router)
api_router.include_router(students.router)
api_router.include_router(teacher.router)
api_router.include_router(profile.router)
api_router.include_router(admin.router)
api_router.include_router(school_admin.router)
api_router.include_router(blog.router)
api_router.include_router(academic.router)
