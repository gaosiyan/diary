# -*- coding: utf-8 -*-

"""
文件名称: utils.py
文件作者: gaosiyan
创建时间: 20251213
功能说明: 工具函数
"""

import os
from typing import List
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha1


def check_files_exist_parallel(file_path_list: List[str]) -> List[bool]:
    """
    并行检查文件是否存在

    Args:
        file_path_list: 文件路径列表

    Returns:
        布尔值列表，对应每个文件是否存在

    file_path_list = ["/path/to/file1.txt", "/path/to/file2.txt", "/path/to/file3.txt"]
    exist_list = check_files_exist_parallel(file_path_list)

    for file_path, exist_flag in zip(file_path_list, exist_list):
        if exist_flag is False:
            print(f"{file_path}: 不存在")
    """

    def check_file(path: str) -> bool:
        return os.path.exists(path)

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(check_file, file_path_list))

    return results


def calc_sha1_code_parallel(file_path_list: List[str]) -> List[bool]:
    """
    并行计算文件的 sha1 码

    Args:
        file_path_list: 文件路径列表

    Returns:
        sha1 码列表，对应每个文件的 sha1 码,如果读取错误返回 None

    file_path_list = ["/path/to/file1.txt", "/path/to/file2.txt", "/path/to/file3.txt"]
    sha1_code_list = calc_sha1_code_parallel(file_path_list)

    for file_path, sha1_code in zip(file_path_list, sha1_code_list):
        if sha1_code is None:
            print(f"{file_path} Sha1 码计算失败")
        else:
            print(f"{file_path} Sha1 码为 {sha1_code}")
    """

    def calc_sha1_code(file_path: str):
        try:
            with open(file_path, mode="rb") as file:
                content = file.read()
                return sha1(content).hexdigest()
        except:
            return None

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(calc_sha1_code, file_path_list))

    return results


if __name__ == "__main__":

    file_path_list = ["1.png", "2.png", "3.png", "4.png", "55.png", "66.png", "77.png", "88.png", "99.png", "aa.png"]
    os.chdir(r"D:\projects\diary\source\_static")

    results = calc_sha1_code_parallel(file_path_list)
    print(results)
