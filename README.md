# metabase-kanban-dashboard

The goal of this project is to provide an open-source Kanban metrics dashboard for Metabase.

This still in early stage and that's how the dashboard currently looks like:

![Screen Shot 2020-09-07 at 22 19 59-fullpage](https://user-images.githubusercontent.com/33388/92423867-fbac2380-f158-11ea-9e07-7b5c5d83a9db.png)

## Getting started

Before getting started you will need to have a PostgreSQL server and a Metabase instance configured and running.

The tools included in this repository will create the questions and the dashboards in your metabase instance as well as the database schema you will need.

It's not in the scope of this project to connect to any project management tool to extract your information (at least not for now).

Long story short, here is what you will need in order to get your Kanban dashboard up and running:

1. Create the tables required to store your Kanban data
1. Import the Metabase questions and dashboards
1. Process the data from your project management tool and insert in the database

In the next sections we'll guide you over each of the next steps.

If you want to play around with the test docker environment before getting your hands dirty, take a look in the section "[Testing with the container and the test data](#testing-with-the-container-and-the-test-data)".


### Installing

You can install the library by cloning this repository and running `pip install .` inside the repository directory.

Another option is to just download our docker container using `docker pull cravefood/kanban-dash`.

In either case you will always have to set the the env var `KANBANDASH_DATABASE_URL`. This is how the tool will know in which database it should connect. The variable should look like this `KANBANDASH_DATABASE_URL=postgresql://<db_user>:<db_password>@<db_host>:<db_port>/<db_name>`.


### Creating the models

To create the models you will need to run the command:

```
KANBANDASH_DATABASE_URL=postgresql://<db_user>:<db_password>@<db_host>:<db_port>/<db_name> kanban-dash models --create
```

Or using the docker container:

```
docker run -e KANBANDASH_DATABASE_URL=postgresql://<db_user>:<db_password>@<db_host>:<db_port>/<db_name> cravefood/kanban-dash kanban-dash models --create
```


### Creating the questions and dashboards in Metabase

Before creating the data in Metabase you will need to configure your Metabase instance to access your Kanban database. You can do that by accessing Settings -> Admin -> Databases (top menu) -> Add database.

With your database configured you will need to create a new collection: Browse all items -> New collection.
After creating the collection you will have to access it in order to get the collection id (available in the collection URL).

Now we are ready to run the collection import script:

```
kanban-dash metabase --import \
    --username=<your-user-name> \
    --collection-id=<your-collection-id> \
    --url=<your-metabase-url>
```

or using our docker container:

```
docker run -it cravefood/kanban-dash kanban-dash metabase --import \
    --username=<your-user-name> \
    --collection-id=<your-collection-id> \
    --url=<your-metabase-url>
```


After running the script you should be able to access the collection and see the imported reports. Select "Kanban" in the dashboards tab to see the dashboard without any data.

If you want to insert some test data you can that by running:

```
KANBANDASH_DATABASE_URL=postgresql://<db_user>:<db_password>@<db_host>:<db_port>/<db_name> kanban-dash generate-test-data
```

Or using the docker container:

```
docker run -e KANBANDASH_DATABASE_URL=postgresql://<db_user>:<db_password>@<db_host>:<db_port>/<db_name> cravefood/kanban-dash kanban-dash generate-test-data
```


Once you are done playing with the test data you can clean it up using the command:

```
KANBANDASH_DATABASE_URL=postgresql://<db_user>:<db_password>@<db_host>:<db_port>/<db_name> models --reset
```

Or using the docker container:

```
docker run -e KANBANDASH_DATABASE_URL=postgresql://<db_user>:<db_password>@<db_host>:<db_port>/<db_name> cravefood/kanban-dash kanban-dash models --reset
```

### Inserting real data

TODO


## Testing with the container and the test data

* Start the containers
```
$ docker-compose up
```

* Run the scripts to create the database schema:
```
docker-compose run kanban-dash kanban-dash models --create
```

* Run the script to populate the database with test data:
```
docker-compose run kanban-dash kanban-dash generate-test-data
```

* Access the local Metabase instance on http://localhost:3000, create a user and password and connect to the testing database (db `kanban_metrics`, hostname `postgres`, username `postgres`, no password).

* Create an empty collection using the link: http://localhost:3000/collection/root/new_collection. Check the ID of the newly created collection in the URL (probably 2).

* Run the script to import the Kanban dashboard to the new collection. Make sure to use the proper username and collection-id:
```
metabase-import-export \
    --username=<your-user-name> \
    import \
    --collection-id=<your-collection-id> \
    --import-file=kanbandash/kanban-dashboards.json
```

or using our docker container:

```
docker run cravefood/kanban-dash metabase-import-export \
    --username=<your-user-name> \
    import \
    --collection-id=<your-collection-id> \
    --import-file=kanbandash/kanban-dashboards.json
```


## Developing / Contributing

### Creating a schema migration

The database migrations are using alembic. If perform a change in the models.py file you will need to create a new database migration to reflect those changes. Usign the docker-compose environment you can do that using the following command:

```
docker-compose run kanban-dash alembic revision --autogenerate -m "<Your message here>"
```
