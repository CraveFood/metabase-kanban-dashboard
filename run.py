import inspect

import models

from populate_with_test_data import generate_data


def is_base_subclass(obj):
    if obj is not models.Base and inspect.isclass(obj) and issubclass(obj, models.Base):
        return True


def get_tables():
    obj_names = dir(models)

    objs = [
        getattr(models, obj_name)
        for obj_name in obj_names
        if not obj_name.startswith("__")
    ]
    objs = [obj.__table__ for obj in objs if is_base_subclass(obj)]

    return objs


def drop_tables():
    tables = get_tables()
    models.Base.metadata.drop_all(models.SQLALCHEMY_ENGINE, tables=tables)


def create_tables():
    tables = get_tables()
    models.Base.metadata.create_all(models.SQLALCHEMY_ENGINE, tables=tables)


def recreate_table():
    drop_tables()
    create_tables()


if __name__ == "__main__":
    recreate_table()
    generate_data()
