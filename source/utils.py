# -*- coding: utf-8 -*-

"""
文件名称: utils.py
文件作者: gaosiyan
创建时间: 20251213
功能说明: 工具函数
"""

import os
import multiprocessing
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
        函数返回值列表
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


if __name__ == "__main__":

    image_file_path_list = ["1.png", "2.png", "3.png", "4.png", "55.png", "66.png", "77.png", "88.png", "99.png", "aa.png"]
    os.chdir(r"D:\projects\diary\source\_static")

    result_list = calculate_files_sha1_code_parallel(image_file_path_list)
    print(result_list)
