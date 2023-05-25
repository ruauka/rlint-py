import click

from rlint.rules.R0001.R0001 import R0001
from rlint.tools.utils import get_config
from rlint.tools.dirs_files import get_py_files


# запуск скрипта проверки
def execute(paths: tuple, cfg: str) -> None:
    # парсинг конфигурации
    cfg = get_config(config_path=cfg)
    # получение списка путей всех py-файлов
    py_files = get_py_files(paths, cfg)
    # запуск проверки R0001
    R0001(py_files, cfg)


# CLI обертка
@click.command()
@click.argument('paths', type=click.Path(exists=True), nargs=-1)
@click.option("--config", default="pyproject.toml", help="Путь к файлу конфигурации линтера.")
def main(paths: tuple, config: str):
    execute(paths, config)


if __name__ == '__main__':
    main()

    # paths_ = (".",)
    # cfg_ = "testdata/pyproject.toml"
    # execute(paths_, cfg_)

# PYTHONPATH=. python rlint/main.py . --config=rlint/testdata/pyproject.toml
# pip install -e /Users/ushakov-as1-mobile/Python/tools/rlint
