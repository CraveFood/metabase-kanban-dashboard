
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

import settings

# SQLAlchemy
SQLALCHEMY_ENGINE = create_engine(settings.POSTGRES_DATABASE_URL, echo=False)

Base = declarative_base()
Session = sessionmaker(bind=SQLALCHEMY_ENGINE)


class KanbanTagType(Base):
    __tablename__ = "kanban_tag_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    tags = relationship("KanbanTag", back_populates="type")


class KanbanTag(Base):
    __tablename__ = "kanban_tag"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    type = relationship("KanbanTagType", back_populates="tags")
    type_id = Column(Integer, ForeignKey("kanban_tag_type.id"))


class KanbanCardTag(Base):
    __tablename__ = "kanban_card_tag_rel"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tag_id = Column(Integer, ForeignKey("kanban_tag.id"))
    card_id = Column(String, ForeignKey("kanban_card.id"))

    __table_args__ = (UniqueConstraint(tag_id, card_id),)


class KanbanCard(Base):
    __tablename__ = "kanban_card"

    id = Column(String, primary_key=True)
    tags = relationship("KanbanTag", secondary="kanban_card_tag_rel", backref="cards")
    times = relationship("KanbanCardTime", back_populates="card")

    waste = Column(Boolean, default=False)
    closed = Column(Boolean, default=False)


class KanbanCardTime(Base):
    __tablename__ = "kanban_card_time"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String)
    time = Column(Integer, default=-1)
    start_date = Column(Date)
    end_date = Column(Date)
    card_id = Column(String, ForeignKey("kanban_card.id"))
    card = relationship("KanbanCard", back_populates="times")

    __table_args__ = (UniqueConstraint(card_id, type),)


class KanbanColumn(Base):
    __tablename__ = "kanban_column"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    order = Column(Integer)


class KanbanDay(Base):
    __tablename__ = "kanban_day"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)
    column_id = Column(Integer, ForeignKey("kanban_column.id"))
    column = relationship("KanbanColumn")
    count = Column(Integer)

    __table_args__ = (UniqueConstraint(date, column_id),)
