from viajei_api.schemas.user import UserSchema


class Story:
    name: str
    title: str
    email = UserSchema.email
    body: str
