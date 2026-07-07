from pydantic import BaseModel


class StorySchema(BaseModel):
    author: str
    title: str
    story: str


class StoryDB(StorySchema):
    id: int


class StoryPublic(BaseModel):
    id: int
    title: str
    email: str
