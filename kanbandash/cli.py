import argparse
import inspect
import os
import pathlib

from alembic import command
from alembic.config import Config

from . import models

from .populate_with_test_data import generate_data

SCRIPT_DIR = pathlib.Path(__file__).parent.absolute()

os.chdir(SCRIPT_DIR)

ALEMBIC_CFG = Config(pathlib.Path(SCRIPT_DIR, "alembic.ini"))


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
    migrate_schema()


def recreate_tables():
    drop_tables()
    create_tables()


def migrate_schema():
    command.upgrade(ALEMBIC_CFG, "head")


def manage_models(args):
    if args.create:
        create_tables()

    elif args.reset:
        recreate_tables()

    elif args.upgrade:
        migrate_schema()


def get_argparser():
    parser = argparse.ArgumentParser(
        description="Metabase Kanban Dashboard manager",
    )
    subparsers = parser.add_subparsers()

    # models subparsers
    models = subparsers.add_parser("models")
    models_group = models.add_mutually_exclusive_group(required=True)
    models_group.add_argument(
        "--create", action="store_true", help=("Create the database schema.")
    )
    models_group.add_argument(
        "--upgrade",
        action="store_true",
        help=("Update the database schema to the latest version."),
    )
    models_group.add_argument(
        "--reset",
        action="store_true",
        help="Destroy and recreate all tables. Note that ALL DATA WILL BE ERASED.",
    )
    models.set_defaults(func=manage_models)

    # test-data subparser
    test_data = subparsers.add_parser("generate-test-data")
    test_data.set_defaults(func=generate_data)

    return parser


def main():
    parser = get_argparser()
    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_usage()


if __name__ == "__main__":
    main()
