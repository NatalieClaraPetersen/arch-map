import yaml

from graph.models import ViewConfig


class Config:
    def __init__(self, repo_url, code_root_folder, save_location, views):
        self.REPO_URL = repo_url
        self.CODE_ROOT_FOLDER = code_root_folder
        self.save_location = save_location
        self.views = views

def load_views_config(path):
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    
    repo_url = data["REPO_URL"]  
    code_root_folder = data["CODE_ROOT_FOLDER"]
    save_location = data["save_location"]
    
    views = []
    for view_data in data["views"]:
        views.append(
            ViewConfig(
                name=view_data["name"],
                include=view_data.get("include", []),
                exclude=view_data.get("exclude", []),
                groups=view_data.get("groups", {}),
                allowed_edges_to=view_data.get("allowed_edges_to", {}),
                depth_config=view_data.get("depth_config", {}),
            )
        )

    return Config(repo_url, code_root_folder, save_location, views)
