import argparse
import inspect
import os
import pathlib

from alembic import command
from alembic.config import Config

from metabase_import_export import (
    export_collection,
    import_collection,
    metabase_login,
    set_metabase_url,
)

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
    engine = models.get_db_engine()
    models.Base.metadata.drop_all(engine, tables=tables)


def create_tables():
    tables = get_tables()
    engine = models.get_db_engine()
    models.Base.metadata.create_all(engine, tables=tables)
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


def manage_metabase(args):
    set_metabase_url(args.url)
    metabase_login(args.username)

    if args.export:
        print("Where to you want to store your Kanban definitions?")
        kanban_definitions_file = input(">> ")
        export_collection(kanban_definitions_file, args.collection_id)
    else:
        kanban_definitions_file = os.path.join(SCRIPT_DIR, "kanban-dashboards.json")
        import_collection(kanban_definitions_file, args.collection_id)


def get_argparser():
    parser = argparse.ArgumentParser(
        description="Metabase Kanban Dashboard manager",
    )
    subparsers = parser.add_subparsers()

    # metabase subparsers
    metabase = subparsers.add_parser("metabase")
    import_export_group = metabase.add_mutually_exclusive_group(required=True)
    import_export_group.add_argument(
        "--import",
        action="store_true",
        help=("Import the Kanban dashboard definitions to a Metabase instance."),
    )
    import_export_group.add_argument(
        "--export",
        action="store_true",
        help=("Export the Kanban dashboard definitions from a Metabase instance."),
    )
    metabase.add_argument(
        "--collection-id",
        type=int,
        help=(
            "The id of the collection where the data will be imported to or "
            "exported from."
        ),
        required=True,
    )
    metabase.add_argument(
        "--url",
        help="Metabase base URL",
        default="http://localhost:3000",
    )
    metabase.add_argument(
        "--username",
        help="Metabase admin user",
        required=True,
    )
    metabase.set_defaults(func=manage_metabase)

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
