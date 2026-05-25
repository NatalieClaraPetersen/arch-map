View the html files in the ./diagrams folder

Every diagram is specified in the ./architecture_views.yaml

To remove any unused imports in the cloned repo, we use autoflake, so make sure to install it:
```bash
pip install autoflake
# You can also try autoflake out manually:
autoflake --remove-all-unused-imports --in-place --recursive content/  --ignore-init-module-imports
```

Each run of the following command, clones/pulls the target repo, removes all unused imports from the target repo and remakes all the views specified in architecture_views.yaml:
```shell
python3 main.py
```