# -*- coding: utf-8 -*-

"""
文件名称: RstDocBatchProcessor.py
文件作者: gaosiyan
创建时间: 20251213
功能说明: RST 文档批处理类
"""

import os
from RstDocParser import RstDocParser
from utils import rename_files_by_sha1


class RstDocBatchProcessor:
    """RST 文档批处理类封装"""

    def __init__(self, root_dir: str, image_dir: str) -> None:
        """
        root_dir: 文档根目录
        image_dir: 图像根目录
        """
        if os.path.isdir(root_dir) is False:
            raise RstDocBatchProcessorError(f"错误! {root_dir} 目录不存在.")

        if os.path.isdir(image_dir) is False:
            raise RstDocBatchProcessorError(f"错误! {image_dir} 目录不存在.")

        self.root_dir = root_dir
        self.image_dir = image_dir

        self.rst_file_paths = []

        for root, _, files in os.walk(root_dir):
            for file in files:
                if file.endswith(".rst"):
                    self.rst_file_paths.append(os.path.join(root, file))

    def format(self):
        """
        遍历处理所有文档
        """
        rename_dicts = rename_files_by_sha1(self.image_dir)

        for rst_file_path in self.rst_file_paths:
            parse = RstDocParser(rst_file_path)
            # image_file_paths 是当前文档的所有图片,例如[/_static/1.png,/_static/2.png]
            image_file_paths = parse.get_image_file_paths()

            replace_dicts = []

            for image_file in image_file_paths:
                # base_file_name 只是文件名,例如 1.png
                base_file_name = os.path.basename(image_file)
                if base_file_name in rename_dicts:
                    old_str = image_file
                    new_str = image_file.replace(base_file_name, rename_dicts[base_file_name])
                    print(old_str, new_str)


class RstDocBatchProcessorError(Exception):
    """自定义异常类
    在异常处直接用:
        raise RstDocBatchProcessorError("错误信息") 抛出异常

    try:
        ...
    except RstDocBatchProcessorError as exc:
        print(exc)
    """
