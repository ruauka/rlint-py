import glob
from rlint.tools.utils import *


# открытие проверяемого py-файла
def py_file_open(filepath: str) -> str:
    with open(os.path.join(filepath), "r") as f:
        return f.read()


# создание списка подпапок для последующего поиска в них py-файлов
def get_all_dir_paths(path: str, cfg: Dict[str, Any]) -> list:
    sub_folders = []

    for instance in os.scandir(path):
        # идем только по папкам
        if not instance.is_dir():
            continue
        # исключение виртуального окружения
        if exclude_venv(instance.path[2:]):
            continue
        # исключение из проверки; f.path[2:] - очистка от ./
        if exclude_dirs(instance.path[2:], cfg):
            continue

        sub_folders.append(instance.path)

    # рекурсивный обход подпапок
    for dir_name in list(sub_folders):
        sub_folders.extend(get_all_dir_paths(dir_name, cfg))

    return sub_folders


# создание списка путей всех py-файлов во всех переданых директориях
def get_all_py_files_paths(all_dirs: list) -> list:
    # список py-файлов из всех подпапок без корневых py-файлов
    py_files = list()

    for directory in all_dirs:
        for filename in glob.iglob(directory + '**/*py', recursive=True):
            py_files.append(filename)

    # добавление корневых py-файлов если идем от корня проекта
    if "." in all_dirs:
        py_files = add_root_py_files(py_files)

    # очистка от ./ py-файлов
    py_files = remove_root_slash(py_files)

    return py_files


# получение всех py-файлов (без исключенных)
def get_py_files(paths: tuple, cfg: Dict[str, Any]) -> list:
    py_files = []

    for path in paths:
        # фикс корневого пути
        if path == "./":
            path = "."

        # проверка файл ли это
        if os.path.isfile(path):
            py_files.append(path)

        # проверка директория ли это
        if os.path.isdir(path):
            # получение всех подпапок переданной директории
            all_dirs = get_all_dir_paths(path, cfg)
            # массив из полученных подпапок + текущая директория
            dirs = [path] + all_dirs
            # получение всех py-файлов из актуальных подпапок
            all_files = get_all_py_files_paths(dirs)
            # распаковка путей py-файлов в общий список
            for file in all_files:
                py_files.append(file)

    # исключение из проверки py-файлов по инструкции exclude
    py_files = exclude_files(py_files, cfg)

    return py_files
