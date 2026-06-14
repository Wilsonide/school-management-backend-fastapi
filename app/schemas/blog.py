from pydantic import BaseModel
from typing import Optional


class BlogCreate(BaseModel):
    title: str
    excerpt: str
    content: str
    coverImage: Optional[str] = None
    coverImageId: Optional[str] = None
    published: bool = False
    featured: bool = False
    seoTitle: Optional[str] = None
    seoDescription: Optional[str] = None


class BlogUpdate(BaseModel):
    title: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    coverImage: Optional[str] = None
    coverImageId: Optional[str] = None
    published: Optional[bool] = None
    featured: Optional[bool] = None
    seoTitle: Optional[str] = None
    seoDescription: Optional[str] = None