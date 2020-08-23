
import datetime

import factory
from factory import fuzzy

from models import KanbanDay, KanbanColumn
from . import factories_session


class KanbanColumnFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = KanbanColumn
        sqlalchemy_session = factories_session
        #sqlalchemy_session_persistence = 'commit'

    name = factory.Iterator(["todo", "in_progress", "review", "qa"])
    order = fuzzy.FuzzyInteger(0, 10)


class KanbanDayFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = KanbanDay
        sqlalchemy_session = factories_session
        #sqlalchemy_session_persistence = 'commit'

    date = factory.Faker(
        'date_between_dates',
        date_start=datetime.date(2020, 1, 1),
        date_end=datetime.date(2020, 5, 31),
    )
    column = factory.SubFactory(KanbanColumnFactory)
    count = fuzzy.FuzzyInteger(0, 10)
