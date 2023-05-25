import platform
import toml
import os
from typing import Any, Dict


# парсинг конфигурации линтера
def get_config(config_path: str) -> Dict[str, Any]:
    try:
        cfg = toml.load(config_path)
    except FileNotFoundError:
        return {}

    return cfg


# парсинг трешхолда для правила R0001.
def get_threshold_R0001(cfg: Dict[str, Any]) -> int:
    # дефолтное значение = 2
    threshold = 2

    # проверка наличия настройки в pyproject.toml [tool.rlint.R0001]
    if cfg_check(cfg):
        if cfg["tool"]["rlint"].get("R0001"):
            if cfg["tool"]["rlint"]["R0001"].get("threshold"):
                return cfg["tool"]["rlint"]["R0001"]["threshold"]

    return threshold


# проверка директории на исключение из проверок
def exclude_dirs(directory: str, cfg: Dict[str, Any]) -> bool:
    if cfg_check(cfg):
        if cfg["tool"]["rlint"].get("exclude"):
            return directory in cfg["tool"]["rlint"]["exclude"]

    return False


# проверка файлов на исключение из проверок
def exclude_files(all_files: list, cfg: Dict[str, Any]) -> list:
    if cfg_check(cfg):
        if cfg["tool"]["rlint"].get("exclude"):
            return [file for file in all_files if file not in cfg["tool"]["rlint"]["exclude"]]

    return all_files


# добавление py-файлов из корня проекта к списку директорий py-файлов из всех подпапок
def add_root_py_files(without_root_files: list) -> list:
    return without_root_files + list(filter(lambda x: x.endswith('.py'), os.listdir("./")))


# удаление ./ из пути py-файла (./file.py -> file.py)
def remove_root_slash(with_root_files: list) -> list:
    return [file[2:] if file[:2] == "./" else file for file in with_root_files]


# исключение виртуального окружения
def exclude_venv(directory: str):
    venv = os.getenv("VIRTUAL_ENV")

    # путь unix
    if platform.system() == "Darwin" or platform.system() == "Linux":
        return directory == venv.split("/")[-1].strip()

    # путь windows
    if platform.system() == "Windows":
        return directory == venv.split("\\")[-1].strip()


def cfg_check(cfg: Dict[str, Any]):
    if cfg.get("tool"):
        if cfg["tool"].get("rlint"):
            return True

    return False
