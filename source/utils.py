# -*- coding: utf-8 -*-

"""
文件名称: utils.py
文件作者: gaosiyan
创建时间: 20251213
功能说明: 工具函数
"""

import os
import multiprocessing
import re
from typing import List, Callable, Any
from concurrent.futures import ProcessPoolExecutor
from hashlib import sha1


def execute_in_parallel(func: Callable[[str], Any], arguments: List[str]) -> List[Any] | None:
    """
    使用进程池并行执行函数

    Args:
        func: 要执行的函数, 接受一个参数
        arguments: 参数列表, 每次执行 func 函数时传入的参数

    Returns:
        函数返回值列表, 或 None 表示没有执行成功
    """
    # 最大进程数为CPU核数
    with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        results = list(executor.map(func, arguments))
        return results

    return None


def check_files_exist_parallel(file_paths: List[str]) -> List[bool]:
    """
    并行检查文件是否存在

    Args:
        file_paths: 文件路径列表

    Returns:
        布尔值列表，对应每个文件是否存在

    Example:
        >>> file_paths = ["/path/to/file1.txt", "/path/to/file2.txt", "/path/to/file3.txt"]
        >>> exist_flags = check_files_exist_parallel(file_paths)
        >>> for file_path, exists in zip(file_paths, exist_flags):
        >>>     if not exists:
        >>>         print(f"{file_path}: 不存在")
    """
    return execute_in_parallel(os.path.exists, file_paths)


def calculate_file_sha1_code(file_path: str):
    """
    计算文件的 SHA1 码

    Args:
        file_path: 文件路径

    Returns:
        文件的 SHA1 码, 如果读取错误则返回 None
    """
    try:
        with open(file_path, mode="rb") as file:
            content = file.read()
            return sha1(content).hexdigest()
    except (IOError, OSError, FileNotFoundError):
        return None


def calculate_files_sha1_code_parallel(file_paths: List[str]):
    """
    并行计算文件的SHA1码

    Args:
        file_paths: 文件路径列表

    Returns:
        SHA1码列表, 对应每个文件的SHA1码, 如果读取错误则返回None

    Example:
        >>> file_paths = ["/path/to/file1.txt", "/path/to/file2.txt", "/path/to/file3.txt"]
        >>> sha1_codes = calculate_files_sha1_code_parallel(file_paths)
        >>> for file_path, sha1_code in zip(file_paths, sha1_codes):
        >>>     if sha1_code is None:
        >>>         print(f"{file_path}: SHA1码计算失败")
        >>>     else:
        >>>         print(f"{file_path}: SHA1码为 {sha1_code}")
    """
    return execute_in_parallel(calculate_file_sha1_code, file_paths)


def rename_files_by_sha1(root: str):
    """
    重命名文件,并返回已经重命名文件字典 {old_name:new_name}
    """
    cwd = os.getcwd()
    os.chdir(root)

    file_names = os.listdir()

    sha1_codes = calculate_files_sha1_code_parallel(file_names)

    if sha1_codes is None or None in sha1_codes:
        return None

    rename_dict = {}

    for file_name, sha1_code in zip(file_names, sha1_codes):
        file_name_without_ext = os.path.splitext(os.path.basename(file_name))[0]
        if file_name_without_ext != sha1_code:
            old_name = file_name
            new_name = file_name.replace(file_name_without_ext, sha1_code)
            rename_dict[old_name] = new_name
            os.rename(old_name, new_name)

    os.chdir(cwd)
    return rename_dict


def replace_file(file_path: str, old: str, new: str):
    """替换更新文件"""
    content = ""
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read().replace(old, new)

    if content != "":
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content.strip() + os.linesep)


def format(file_path) -> None:
    """
    格式化
    """
    content = ""
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    if content != "":
        # 替换中文标点
        content = (
            content.replace("。", ".")
            .replace("，", ",")
            .replace("（", "(")
            .replace("）", ")")
            .replace("、", ",")
            .replace("！", "!")
            .replace("：", ":")
            .replace("“", '"')
            .replace("”", '"')
            .replace("；", ";")
            .replace("？", "?")
        )

        # 去除中文之间的多余空格
        content = re.sub(r"([\u4e00-\u9fa5]) +([\u4e00-\u9fa5])", r"\1\2", content)
        # 去除英文之间的多余空格
        content = re.sub(r"\b([a-zA-Z]) +([a-zA-Z])\b", r"\1 \2", content)
        # 中英文之间添加一个空格
        content = re.sub(r"([\u4e00-\u9fa5]) *([a-zA-Z])", r"\1 \2", content)
        content = re.sub(r"([a-zA-Z]) *([\u4e00-\u9fa5])", r"\1 \2", content)
        # 中文数字之间添加一个空格
        content = re.sub(r"([\u4e00-\u9fa5]) *(\d+)", r"\1 \2", content)
        content = re.sub(r"(\d+) *([\u4e00-\u9fa5])", r"\1 \2", content)
        # 删除多余的换行
        content = re.sub(r"\n\n+", r"\n\n", content)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content.strip() + os.linesep)


if __name__ == "__main__":

    # image_file_path_list = ["1.png", "2.png", "3.png", "4.png", "55.png", "66.png", "77.png", "88.png", "99.png", "aa.png"]
    # os.chdir(r"D:\projects\diary\source\_static")

    # result_list = calculate_files_sha1_code_parallel(image_file_path_list)
    # print(result_list)

    rename_files_by_sha1(r"D:\projects\diary\source\_static")
