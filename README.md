View the html files in the `diagrams` folder

Every diagram is specified in the `architecture_views.yaml`, here we also define the repo we want to generate model views for (REPO_URL), where to clone the repo to (CODE_ROOT_FOLDER) and where to save the diagrams (save_location).

To install all dependecies run:
```shell
bash install_deps.sh
```

Each run of the following command, clones/pulls the target repo and remakes all the views specified in `architecture_views.yaml`:
```shell
python3 main.py
```