import slugify
import cloudinary.uploader

from app.utils.reading_time import calculate_reading_time
from app.repositories.blog_repository import BlogRepository
from app.models.blog_post import BlogPost


class BlogService:
    def __init__(self):
        self.repo = BlogRepository()

    # =========================
    # CREATE BLOG
    # =========================
    async def create_blog(self, db, data, admin_id: str):
        blog = BlogPost(
            title=data["title"],
            slug=slugify.slugify(data["title"], lowercase=True, separator="-"),
            excerpt=data["excerpt"],
            content=data["content"],
            cover_image=data.get("coverImage"),
            cover_image_id=data.get("coverImageId"),
            published=data.get("published", False),
            featured=data.get("featured", False),
            seo_title=data.get("seoTitle"),
            seo_description=data.get("seoDescription"),
            reading_time=calculate_reading_time(data["content"]),
            author_id=admin_id,
        )

        return await self.repo.create(db, blog)

    # =========================
    # GET ALL
    # =========================
    async def get_blogs(self, db):
        return await self.repo.get_all(db)

    # =========================
    # GET FEATURED (MISSING BEFORE)
    # =========================
    async def get_featured_blogs(self, db):
        return await self.repo.get_featured(db)

    # =========================
    # GET ONE
    # =========================
    async def get_blog(self, db, blog_id: str):
        res = await self.repo.get_by_id(db, blog_id)
        print(res)
        return res

    # =========================
    # UPDATE BLOG
    # =========================
    async def update_blog(self, db, blog, data):
        if "title" in data:
            blog.title = data["title"]
            blog.slug = slugify.slugify(
                data["title"],
                lowercase=True,
                separator="-"
            )

        if "excerpt" in data:
            blog.excerpt = data["excerpt"]

        if "content" in data:
            blog.content = data["content"]
            blog.reading_time = calculate_reading_time(data["content"])

        if "coverImage" in data:
            blog.cover_image = data.get("coverImage")

        if "coverImageId" in data:
            blog.cover_image_id = data.get("coverImageId")

        if "published" in data:
            blog.published = data.get("published", False)

        if "featured" in data:
            blog.featured = data.get("featured", False)

        if "seoTitle" in data:
            blog.seo_title = data.get("seoTitle")

        if "seoDescription" in data:
            blog.seo_description = data.get("seoDescription")

        return await self.repo.update(db, blog)

    # =========================
    # DELETE BLOG
    # =========================
    async def delete_blog(self, db, blog):
        # ☁️ SAFE Cloudinary delete (non-blocking wrapper idea)
        if blog.cover_image_id:
            try:
                cloudinary.uploader.destroy(blog.cover_image_id)
            except Exception as e:
                print("Cloudinary delete failed:", e)

        await self.repo.delete(db, blog)