#!/usr/bin/python

import datetime
import random

import sqlalchemy

from .kanban_day import KanbanDayFactory, KanbanColumnFactory
from . import factories_session


def generate_kanban_columns():
    columns = []
    columns.append(KanbanColumnFactory(name="todo", order=1))
    columns.append(KanbanColumnFactory(name="qa", order=4))
    columns.append(KanbanColumnFactory(name="in_progress", order=2))
    columns.append(KanbanColumnFactory(name="done", order=5))
    columns.append(KanbanColumnFactory(name="review", order=3))
    return columns


def generate_kanban_days(columns, n):
    date = datetime.date(2016, 1, 1)
    done_count = 0

    for i in range(n):
        random.shuffle(columns)
        date += datetime.timedelta(days=1)

        for column in columns:
            factory_args = {
                "column": column,
                "date": date,
            }
            if column.name == "done":
                # Add "done"
                done_count += random.randint(0, 3)
                factory_args["count"] = done_count
            try:
                KanbanDayFactory(**factory_args)
            except sqlalchemy.exc.IntegrityError:
                factories_session.rollback()

    factories_session.commit()


def generate_data():
    columns = generate_kanban_columns()
    generate_kanban_days(columns, 2000)
