import yaml

from pathlib import Path


def config():
    root_dir = Path(__file__).parent
    with open(f"{root_dir}/config/project.yml", 'r', encoding='utf-8') as file:
        return yaml.load(file.read(), Loader=yaml.BaseLoader)['environment']['prod']

        # применимо при запуске venv окружения. в pytest.ini указать "env= STAGE=prod"
        # return yaml.load(file.read(), Loader=yaml.BaseLoader)['environment'][getenv('STAGE')]
