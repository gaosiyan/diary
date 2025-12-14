# -*- coding: utf-8 -*-

"""
文件名称: RstDocParser.py
文件作者: gaosiyan
创建时间: 20251213
功能说明: 单个 RST 文档解析处理类
"""

import os
import re
from typing import List
from pathlib import Path
from docutils.parsers.rst import Parser
from docutils.utils import new_document
from docutils.frontend import get_default_settings
from docutils import nodes

from utils import check_files_exist_parallel


class RstDocParser:
    """处理单个 RST 文档的相关功能封装"""

    def __init__(self, file_path: str) -> None:
        """
        初始化方法只传入文档路径
        """

        if os.path.isfile(file_path) is False:
            raise RstDocParserError(f"错误! 文档 {file_path} 不存在.")

        if file_path.endswith(".rst") is False:
            raise RstDocParserError(f"错误! 文档 {file_path} 非 rst 文档.")

        working_dir = Path(__file__).resolve().parent
        try:
            os.chdir(working_dir)
        except:
            raise RstDocParserError(f"错误! 切换到 {working_dir} 目录失败.")

        self.file_path = file_path

    def get_image_file_paths(self) -> List[str]:
        """
        返回当前文档的图片列表,实际路径需要转换成 ["." + file_path for file_path in image_file_paths]
        """
        file_path = self.file_path
        file_content = ""
        with open(file_path, "r", encoding="utf-8") as file:
            file_content = file.read()

        if file_content == "":
            raise RstDocParserError(f"错误! 文档 {file_path} 读取错误,请检查文件是否非 UTF-8 编码.")

        try:
            parser = Parser()
            settings = get_default_settings(Parser)
            document = new_document(file_path, settings=settings)
            parser.parse(file_content, document)
        except Exception as exc:
            raise RstDocParserError(f"错误! 文档 {file_path} 解析错误,错误信息 {exc}.")

        image_file_paths = []
        for node in self.document.findall(nodes.image):
            if "uri" in node.attributes:
                image_file_paths.append(node["uri"])

        return image_file_paths

    def is_images_complete(self) -> bool:
        """
        判断是否有文件丢失,有丢失返回 False,否则返回 True
        """
        image_file_paths = self.get_image_file_paths()
        exists = check_files_exist_parallel(["." + file_path for file_path in image_file_paths])

        if exists is None:
            print("警告! check_files_exist_parallel 调用失败.")
            return False

        for file_path, exist_flag in zip(image_file_paths, exists):
            if exist_flag is False:
                print(f"警告! {self.file_path} 文件中 {file_path} 不存在.")
                return False

        return True

    def format(self) -> None:
        """
        格式化
        """
        file_path = self.file_path
        file_content = ""
        with open(file_path, "r", encoding="utf-8") as file:
            file_content = file.read()

        if file_content == "":
            raise RstDocParserError(f"错误! 文档 {file_path} 读取错误,请检查文件是否非 UTF-8 编码.")

        # 替换中文标点
        file_content = (
            file_content.replace("。", ".")
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
        file_content = re.sub(r"([\u4e00-\u9fa5]) +([\u4e00-\u9fa5])", r"\1\2", file_content)
        # 去除英文之间的多余空格
        file_content = re.sub(r"\b([a-zA-Z]) +([a-zA-Z])\b", r"\1 \2", file_content)
        # 中英文之间添加一个空格
        file_content = re.sub(r"([\u4e00-\u9fa5]) *([a-zA-Z])", r"\1 \2", file_content)
        file_content = re.sub(r"([a-zA-Z]) *([\u4e00-\u9fa5])", r"\1 \2", file_content)
        # 中文数字之间添加一个空格
        file_content = re.sub(r"([\u4e00-\u9fa5]) *(\d+)", r"\1 \2", file_content)
        file_content = re.sub(r"(\d+) *([\u4e00-\u9fa5])", r"\1 \2", file_content)
        # 删除多余的换行
        file_content = re.sub(r"\n\n+", r"\n\n", file_content)

        # 回写文件
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(file_content.strip() + os.linesep)


class RstDocParserError(Exception):
    """自定义异常类
    在异常处直接用:
        raise RstDocParserError("错误信息") 抛出异常

    try:
        ...
    except RstDocParserError as exc:
        print(exc)
    """


if __name__ == "__main__":
    #processor = RstProcessor(r"D:\projects\diary\source\sphinx\项目部署.rst")
    #print(processor.get_image_file_path_list())
