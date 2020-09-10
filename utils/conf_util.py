import os
import yaml

from utils.common import get_project_root


def read_app_yaml() -> dict:
    p = get_project_root()
    p = p.joinpath("conf.yaml")
    with p.open() as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return data


def conf_to_env():
    data = read_app_yaml()
    for k, v in data["env_variables"].items():
        os.environ[k] = str(v)


if __name__ == "__main__":
    conf_to_env()
    print(os.environ)
