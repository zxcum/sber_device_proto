from sqlalchemy.orm import declarative_base, mapped_column, Mapped, relationship 
from sqlalchemy import MetaData, CheckConstraint, PrimaryKeyConstraint, ForeignKeyConstraint
from pydantic import BaseModel
from sqlalchemy import ForeignKey, JSON, text
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy import String
import uuid
import pytz


MOSCOW_TZ = pytz.timezone('Europe/Moscow')
Base = declarative_base()
Base.metadata = MetaData()


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(nullable=False, primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False, primary_key=True)
    year_of_birth: Mapped[int] = mapped_column(nullable=True)
    user_sessions: Mapped[list["UserSession"]] = relationship(  # Связь 1 - M | /User/ - Answer
        "UserSession",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    __table_args__ = (
        PrimaryKeyConstraint('id', 'first_name'),
    )

class UserSession(Base):
    __tablename__ = 'user_sessions'

    id: Mapped[str] = mapped_column(
        unique=True, default=lambda: str(uuid.uuid4()), nullable=False, primary_key=True)
    user_id: Mapped[str] = mapped_column(nullable=False)
    user_first_name: Mapped[str] = mapped_column(nullable=False)
    theme_id = mapped_column(ForeignKey(
        'themes.id', ondelete="CASCADE"), nullable=True)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=lambda: datetime.now(MOSCOW_TZ)
    )
    score: Mapped[int] = mapped_column(nullable=True)

    __table_args__ = (
        ForeignKeyConstraint(['user_id', 'user_first_name'], ['users.id', 'users.first_name'], ondelete="CASCADE"),
    )


    user: Mapped["User"] = relationship(  # Связь M - 1 | /Answer/ - User
        "User",
        back_populates="user_sessions"
    )
    answers: Mapped[list["Answer"]] = relationship(  # Связь 1 - M | /User/ - Answer
        "Answer",
        back_populates="session",
        cascade="all, delete-orphan"
    )


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=lambda: datetime.now(MOSCOW_TZ)
    )
    text: Mapped[str] = mapped_column(nullable=True)
    question_id = mapped_column(ForeignKey(
        'questions.id', ondelete="CASCADE"), nullable=True)
    session_id = mapped_column(ForeignKey(
        'user_sessions.id', ondelete="CASCADE"))

    # Связи
    session: Mapped["UserSession"] = relationship(  # Связь M - 1 | /Answer/ - User
        "UserSession",
        back_populates="answers"
    )
    question: Mapped["Question"] = relationship(  # Связь M - 1 | Answer - /Question/
        "Question",
        back_populates="answers",
    )



class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    text: Mapped[str] = mapped_column(nullable=False)
    theme_id = mapped_column(ForeignKey("themes.id", ondelete="CASCADE"))
    age_group_id = mapped_column(ForeignKey("age_groups.id", ondelete="CASCADE"))

    right_answer: Mapped[str] = mapped_column(nullable=False)
    fact: Mapped[str] = mapped_column(nullable=False)
    hint: Mapped[str] = mapped_column(nullable=False)

    answers: Mapped[list["Answer"]] = relationship(
        "Answer",
        back_populates="question",
        cascade="all, delete-orphan"  # Связь 1 - M | /Question/ - Answer
    )

    theme: Mapped["Theme"] = relationship(  # Связь M - 1 | /Question/ - Theme
        "Theme",
        back_populates="questions",
    )

    age_group: Mapped["AgeGroup"] = relationship(  # Связь M - 1 | /Question/ - Theme
        "AgeGroup",
        back_populates="questions",
    )



class Theme(Base):
    __tablename__ = "themes"

    id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    questions: Mapped[list["Question"]] = relationship(
        "Question",
        back_populates="theme",
        cascade="all, delete-orphan"  # Связь 1 - M | /Theme/ - MainQuestion
    )

class AgeGroup(Base):
    __tablename__ = "age_groups"

    id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    age_from: Mapped[int] = mapped_column(nullable=False)
    age_to: Mapped[int] = mapped_column(nullable=False)

    questions: Mapped[list["Question"]] = relationship(
        "Question",
        back_populates="age_group",
        cascade="all, delete-orphan"  # Связь 1 - M | /Theme/ - MainQuestion
    )