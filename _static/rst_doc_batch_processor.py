# -*- coding: utf-8 -*-

"""
文件名称: rst_doc_batch_processor.py
文件作者: gaosiyan
创建时间: 20251213
功能说明: RST 文档批处理类
"""

import os
from rst_doc_parser import RstDocParser
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
        rename_dict = rename_files_by_sha1(self.image_dir)

        for rst_file_path in self.rst_file_paths:
            parser = RstDocParser(rst_file_path)

            if rst_file_path.endswith("index.rst") is False:
                # image_file_paths 是当前文档的所有图片,例如[/_static/1.png,/_static/2.png]
                image_file_paths = parser.get_image_file_paths()

                replace_dict = {}

                for image_file in image_file_paths:
                    # base_file_name 只是文件名,例如 1.png
                    base_file_name = os.path.basename(image_file)
                    if base_file_name in rename_dict:
                        old_str = image_file
                        new_str = image_file.replace(base_file_name, rename_dict[base_file_name])
                        replace_dict[old_str] = new_str

                if replace_dict:
                    parser.replace_image_path(replace_dict)

            parser.format()


class RstDocBatchProcessorError(Exception):
    """自定义异常类
    在异常处直接用:
        raise RstDocBatchProcessorError("错误信息") 抛出异常

    try:
        ...
    except RstDocBatchProcessorError as exc:
        print(exc)
    """


if __name__ == "__main__":
    processor = RstDocBatchProcessor(r"D:\projects\diary\source", r"D:\projects\diary\source\_static")
    processor.format()
