metabase-kanban-dashboard
=========================

The goal of this project is to provide an open-source Kanban metrics dashboard for Metabase.

This still in early stage and that's how the dashboard currently looks like:

![Screen Shot 2020-09-07 at 22 19 59-fullpage](https://user-images.githubusercontent.com/33388/92423867-fbac2380-f158-11ea-9e07-7b5c5d83a9db.png)

Testing with the container and the test data:
---------------------------------------------

* Start the containers
```
$ docker-compose up
```

* Run the script to create a populate the test database:
```
$ ./scripts/run.sh populate_with_test_data.py
```

* Access the local Metabase instance on http://localhost:3000, create a user and password and connect to the testing database (db `kanban_metrics`, hostname `postgres`, username `postgres`, no password).

* Create an empty collection using the link: http://localhost:3000/collection/root/new_collection

* Run the script to import the Kanban dashboards to the new collection. Check that you set the proper user name and collection id (probably "2"):
```
./scripts/metabase-import-export.py --username <your-user-name> import --collection-id=<your-collection-id> --import-file=kanban-dashboards.json
```
