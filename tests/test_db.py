from dataclasses import asdict

from sqlalchemy import select

from viajei_api.models import Story, User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(email="jorge@example.test", password="SenhaForte123")

        session.add(new_user)
        session.commit()

    user = session.scalar(
        select(User).where(User.email == "jorge@example.test")
    )

    assert asdict(user) == {
        "id": 1,
        "password": "SenhaForte123",
        "email": "jorge@example.test",
        "created_at": time,
    }


def test_create_story(session, mock_db_time, user):
    with mock_db_time(model=Story) as time:
        new_story = Story(
            author="Fulaninho",
            title="Pensando ilimitado",
            story="Que baita história",
        )

        new_story.email = user.email

        session.add(new_story)
        session.commit()

    story = session.scalar(select(Story).where(Story.author == "Fulaninho"))

    assert asdict(story) == {
        "id": 1,
        "author": "Fulaninho",
        "title": "Pensando ilimitado",
        "email": "jorge@example.com",
        "story": "Que baita história",
        "created_at": time,
    }
