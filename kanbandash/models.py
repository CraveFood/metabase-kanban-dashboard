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

from . import settings

SQLALCHEMY_CACHE = {}

Base = declarative_base()


def get_db_engine():
    if "engine" in SQLALCHEMY_CACHE:
        return SQLALCHEMY_CACHE["engine"]

    engine = create_engine(settings.POSTGRES_DATABASE_URL, echo=False)
    SQLALCHEMY_CACHE["engine"] = engine
    return engine


def get_db_session_class():
    if "session" in SQLALCHEMY_CACHE:
        return SQLALCHEMY_CACHE["session"]

    engine = get_db_engine()
    Session = sessionmaker(bind=engine)
    SQLALCHEMY_CACHE["session"] = Session

    return Session


class KanbanClassOfService(Base):
    __tablename__ = "kanban_class_of_service"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    cards = relationship("KanbanCard", back_populates="class_of_service")


class KanbanCard(Base):
    __tablename__ = "kanban_card"

    id = Column(String, primary_key=True)

    board_id = Column(Integer, ForeignKey("kanban_board.id"))
    board = relationship("KanbanBoard", back_populates="cards")

    class_of_service_id = Column(Integer, ForeignKey("kanban_class_of_service.id"))
    class_of_service = relationship("KanbanClassOfService", back_populates="cards")

    times = relationship("KanbanCardTime", back_populates="card")

    rework = Column(Boolean, default=False)
    waste = Column(Boolean, default=False)
    closed = Column(Boolean, default=False)


class KanbanBoard(Base):
    __tablename__ = "kanban_board"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    cards = relationship("KanbanCard", back_populates="board")
    columns = relationship("KanbanColumn", back_populates="board")


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

    board_id = Column(Integer, ForeignKey("kanban_board.id"))
    board = relationship("KanbanBoard", back_populates="columns")


class KanbanDay(Base):
    __tablename__ = "kanban_day"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)

    column_id = Column(Integer, ForeignKey("kanban_column.id"))
    column = relationship("KanbanColumn")

    count = Column(Integer)

    class_of_service_id = Column(Integer, ForeignKey("kanban_class_of_service.id"))
    class_of_service = relationship("KanbanClassOfService")

    __table_args__ = (UniqueConstraint(date, column_id, class_of_service_id),)
