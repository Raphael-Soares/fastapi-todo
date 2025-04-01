from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username='Raphael',
        email='raphael@email.com',
        password='passwd',
    )
    session.add(user)
    session.commit()
    result = session.scalar(
        select(User).where(User.email == 'raphael@email.com')
    )

    assert result.username == 'Raphael'
