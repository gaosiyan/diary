# -*- coding: utf-8 -*-

"""
文件名称: RstProcessor.py
文件作者: gaosiyan
创建时间: 20251213
功能说明: RST 文档解析处理类
"""

import os
from typing import List
from pathlib import Path
from docutils.parsers.rst import Parser
from docutils.utils import new_document
from docutils.frontend import get_default_settings
from docutils import nodes

from utils import check_files_exist_parallel


class RstProcessor:
    """处理 RST 文档的完整功能"""

    def __init__(self, file_path: str) -> None:

        if os.path.isfile(file_path) is False:
            raise RstProcessorError(f"错误! 文档 {file_path} 不存在.")

        if file_path.endswith(".rst") is False:
            raise RstProcessorError(f"错误! 文档 {file_path} 非 rst 文档.")

        file_content = ""
        with open(file_path, "r", encoding="utf-8") as file:
            file_content = file.read()

        if file_content == "":
            raise RstProcessorError(f"错误! 文档 {file_path} 为空,或者编码错误.")

        working_dir = Path(__file__).resolve().parent
        try:
            os.chdir(working_dir)
        except Exception as exc:
            raise RstProcessorError(f"错误! 切换到 {working_dir} 目录失败")

        try:
            parser = Parser()
            settings = get_default_settings(Parser)
            document = new_document(file_path, settings=settings)
            parser.parse(file_content, document)
        except Exception as exc:
            raise RstProcessorError(f"错误! 文档 {file_path} 解析错误,错误信息 {exc}.")

        self.file_path = file_path
        self.document = document

    def get_image_file_path_list(self) -> List[str]:
        """
        返回当前文档的图片列表
        """

        file_path_list = []
        for node in self.document.findall(nodes.image):
            if "uri" in node.attributes:
                file_path_list.append(node["uri"])

        exist_list = check_files_exist_parallel(["." + s for s in file_path_list])

        for file_path, exist_flag in zip(file_path_list, exist_list):
            if exist_flag is False:
                raise RstProcessorError(f"错误! 文档 {self.file_path} 中 {file_path} 丢失.")

        return file_path_list


class RstProcessorError(Exception):
    """自定义异常类
    在异常处直接用:
        raise RstProcessorError("错误信息") 抛出异常

    try:
        ...
    except RstProcessorError as exc:
        print(exc)
    """


if __name__ == "__main__":
    processor = RstProcessor(r"D:\projects\diary\source\sphinx\项目部署.rst")
    print(processor.get_image_file_path_list())
