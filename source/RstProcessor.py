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

from utils import check_files_exist_parallel, calculate_files_sha1_code_parallel


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
            raise RstProcessorError(f"错误! 切换到 {working_dir} 目录失败,错误信息 {exc}.")

        try:
            parser = Parser()
            settings = get_default_settings(Parser)
            document = new_document(file_path, settings=settings)
            parser.parse(file_content, document)
        except Exception as exc:
            raise RstProcessorError(f"错误! 文档 {file_path} 解析错误,错误信息 {exc}.")

        self.file_path = file_path
        self.document = document

    def is_image_files_exist(self) -> bool:
        """
        检查当前文档图片是否都存在
        """

        image_file_paths = self._get_image_file_paths()
        exists = check_files_exist_parallel(["." + s for s in image_file_paths])

        if exists is None:
            print("警告! check_files_exist_parallel 调用失败.")
            return False

        for file_path, exist_flag in zip(image_file_paths, exists):
            if exist_flag is False:
                print(f"警告! {self.file_path} 文件中 {file_path} 不存在.")
                return False

        return True

    def get_rename_image_dict_list(self):
        """
        返回需要重命名的文件列表
        """
        image_file_paths = self._get_image_file_paths()
        image_files_sha1_code = calculate_files_sha1_code_parallel(["." + s for s in image_file_paths])
        rename_image_dict_list = []

        if image_files_sha1_code is None or None in image_files_sha1_code:
            raise RstProcessorError(f"错误! sha1 计算错误")

        for file_path, sha1_code in zip(image_file_paths, image_files_sha1_code):
            file_name_without_ext = os.path.splitext(os.path.basename(file_path))[0]

            if file_name_without_ext != sha1_code:
                rename_image_dict_list.append({file_path: file_path.replace(file_name_without_ext, sha1_code)})
        return rename_image_dict_list

    def _calc_image_files_sha1_code(self):
        """
        批量计算 sha1
        """
        image_file_paths = self._get_image_file_paths()
        image_files_sha1_code = calculate_files_sha1_code_parallel(["." + s for s in image_file_paths])

        image_files_sha1_code_dict_list = []

        if image_files_sha1_code is None or None in image_files_sha1_code:
            raise RstProcessorError(f"错误! sha1 计算错误")

        for file_path, sha1_code in zip(image_file_paths, image_files_sha1_code):
            image_files_sha1_code_dict_list.append({file_path, sha1_code})

        return image_files_sha1_code_dict_list

    def _get_image_file_paths(self) -> List[str]:
        """
        返回当前文档的图片列表
        """

        image_file_paths = []
        for node in self.document.findall(nodes.image):
            if "uri" in node.attributes:
                image_file_paths.append(node["uri"])

        return image_file_paths


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
