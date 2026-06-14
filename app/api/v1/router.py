from fastapi import APIRouter

from . import admin, auth, invite, profile, school, school_admin, user,blog

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(user.router)
api_router.include_router(school.router)
api_router.include_router(profile.router)
api_router.include_router(invite.router)
api_router.include_router(admin.router)
api_router.include_router(school_admin.router)
api_router.include_router(blog.router)
