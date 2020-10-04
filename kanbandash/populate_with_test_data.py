#!/usr/bin/python

import datetime
import math
import random
import uuid
import string

from collections import Counter
from itertools import chain

from .models import (
    KanbanBoard,
    KanbanCard,
    KanbanCardTime,
    KanbanClassOfService,
    KanbanColumn,
    KanbanDay,
    Session,
)

factories_session = Session()

START_DATE = datetime.date(2019, 1, 1)
TODAY = datetime.datetime.now().date()

# Distribuition of tasks in each class of service
CLASS_OF_SERVICES = {
    "expedite": 0.03,
    "fixed_date": 0.1,
    "bug": 0.3,
    "standard": 0.4,
    "intangible": 0.26,
}


def generate_boards(n):
    boards = []
    for letter in string.ascii_uppercase:
        name = "Board {}".format(letter)
        board = KanbanBoard(name=name)
        boards.append(board)
        generate_kanban_columns(board)
        factories_session.add(board)

        if len(boards) >= n:
            break

    factories_session.commit()
    return boards


def generate_kanban_columns(board):
    columns = [
        ("todo", 1),
        ("in_progress", 2),
        ("review", 3),
        ("qa", 4),
        ("done", 5),
    ]

    # shuffle columns to ensure queries don't rely on creation order
    random.shuffle(columns)

    for name, order in columns:
        column = KanbanColumn(name=name, order=order)
        board.columns.append(column)


def generate_kanban_days():
    class_of_services = get_object_ids(KanbanClassOfService)
    columns_query = factories_session.query(KanbanColumn)
    date = START_DATE
    done_count = dict.fromkeys(class_of_services, 0)

    while date <= TODAY:
        date += datetime.timedelta(days=1)

        for column in columns_query.all():
            if column.name == "done":
                upper_limit = 1
            else:
                upper_limit = 10

            tasks = random.choices(
                class_of_services,
                weights=CLASS_OF_SERVICES.values(),
                k=random.randint(0, upper_limit),
            )
            counts = Counter(tasks)

            for class_of_service_id in class_of_services:
                if column.name == "done":
                    # Add "done"
                    done_count[class_of_service_id] += counts[class_of_service_id]
                    count = done_count[class_of_service_id]
                else:
                    count = counts[class_of_service_id]

                day = KanbanDay(
                    date=date,
                    column=column,
                    count=count,
                    class_of_service_id=class_of_service_id,
                )
                factories_session.add(day)

    factories_session.commit()


def generate_class_of_services():
    class_of_services = CLASS_OF_SERVICES.keys()

    for name in class_of_services:
        cos = KanbanClassOfService(name=name)
        factories_session.add(cos)

    factories_session.commit()


def get_object_ids(Model):
    raw_query_data = factories_session.query(Model.id).all()
    return list(chain(*raw_query_data))


def generate_kanban_cards(n, m):
    date = START_DATE
    boards = get_object_ids(KanbanBoard)
    class_of_services = get_object_ids(KanbanClassOfService)

    while date <= TODAY:
        date += datetime.timedelta(days=1)
        for i in range(random.randint(n, m)):
            id = uuid.uuid4()
            waste = True if random.randint(0, 9) == 0 else False
            closed = False
            board_id = random.choice(boards)

            # Class of Services distribution
            cos_id = random.choices(
                class_of_services, weights=CLASS_OF_SERVICES.values()
            )[0]

            card = KanbanCard(
                id=id,
                waste=waste,
                closed=closed,
                board_id=board_id,
                class_of_service_id=cos_id,
            )
            for type in ["lead", "cycle", "touch"]:
                start_date = date
                time = math.ceil(random.weibullvariate(10, 1))
                end_date = start_date + datetime.timedelta(days=time)
                card_time = KanbanCardTime(
                    type=type,
                    time=time,
                    start_date=start_date,
                    end_date=end_date,
                    card_id=id,
                )
                factories_session.add(card_time)
            factories_session.add(card)
    factories_session.commit()


def generate_data(args=None):
    generate_class_of_services()
    generate_boards(4)
    generate_kanban_days()
    generate_kanban_cards(3, 10)
