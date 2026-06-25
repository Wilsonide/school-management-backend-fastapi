from pydantic import BaseModel


class LessonCreate(BaseModel):
    class_id: str
    subject_id: str
    session_id: str
    term_id: str

    title: str
    topic: str

    objectives: str | None = None

    file_url: str | None = None

    is_published: bool = True

class LessonUpdate(BaseModel):
    title: str | None = None

    topic: str | None = None

    objectives: str | None = None

    file_url: str | None = None

    is_published: bool | None = None



class LessonFilter(BaseModel):
    class_id: str | None = None
    subject_id: str | None = None
    session_id: str | None = None
    term_id: str | None = None