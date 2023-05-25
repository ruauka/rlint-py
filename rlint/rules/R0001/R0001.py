import ast
from typing import Any, Dict

from rlint.tools.dirs_files import py_file_open
from rlint.tools.utils import get_threshold_R0001


# класс поиска констант
class ConstantVisitor(ast.NodeVisitor):
    def __init__(self):
        self.filename = str()
        self.cache = dict()

    # наполнение кэша
    def cache_fill(self, node, value) -> None:
        if self.cache.get(value):
            self.cache[value]["quantity"] += 1

            if not self.cache[value].get(self.filename):
                self.cache[value][self.filename] = {
                    "lines": [node.lineno],
                    "col_offset": [node.col_offset]
                }
                return

            self.cache[value][self.filename]["lines"].append(node.lineno)
            self.cache[value][self.filename]["col_offset"].append(node.col_offset)
        else:
            self.cache[value] = {
                # количество раз сколько встретилась переменная
                "quantity": 1,
                self.filename: {
                    "lines": [node.lineno],
                    "col_offset": [node.col_offset]
                },
            }

    # ast-метод фильтрации по ast.Constant. >=Python 3.8
    def visit_Constant(self, node: ast.Constant) -> Any:
        self.generic_visit(node)
        # проверка на bool, чтобы True или False не стали ключами в cache
        if type(node.value) is not bool:
            # наполнение кэша
            self.cache_fill(node, node.value)

    # ast-метод фильтрации по ast.Num. <=Python 3.6
    def visit_Num(self, node: ast.Num) -> Any:
        self.generic_visit(node)
        # наполнение кэша
        self.cache_fill(node, node.n)

    # ast-метод фильтрации по ast.Str. <=Python 3.6
    def visit_Str(self, node: ast.Str) -> Any:
        self.generic_visit(node)
        # наполнение кэша
        self.cache_fill(node, node.s)

    # старт проверки всех переданных py-файлов
    def check(self, py_files: list) -> None:
        for filepath in py_files:
            self.filename = filepath
            code = py_file_open(filepath)
            node = ast.parse(code)
            self.visit(node)

    # печать отчета в консоль
    def report(self, threshold: int) -> None:
        for var, var_info in self.cache.items():
            if var_info["quantity"] < threshold:
                continue
            for file_name, file_info in var_info.items():
                if file_name == "quantity":
                    continue
                for index, line in enumerate(file_info["lines"]):
                    print(f"{file_name}:{line}:{file_info['col_offset'][index]}"
                          f" {'R0001'} Hardcode on variable with value: {var}")


# функция старта проверки правила R0001
def R0001(py_files: list, cfg: Dict[str, Any]) -> None:
    # порог дублей
    threshold = get_threshold_R0001(cfg)
    # создание объекта класса
    visitor = ConstantVisitor()
    # запуск скрипта проверки
    visitor.check(py_files)
    # запуск отчета
    visitor.report(threshold)
