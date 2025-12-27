# -*- coding: utf-8 -*-

"""
文件名称: sphinx_format.py
文件作者: gaosiyan
创建时间: 20251226
功能说明: 当前项目格式化
"""

import os
import sys
import shutil
from pathlib import Path
from sphinx.application import Sphinx

from utils import rename_files_by_sha1, replace_file


def sphinx_format():
    """
    格式化 sphinx 文档项目
    """

    ROOT_DIR = Path(__file__).resolve().parent.parent  # Sphinx 根目录
    SRC_DIR = os.path.join(ROOT_DIR, "source")  # 源码目录
    CONFIG_DIR = SRC_DIR  # conf.py 的目录
    BUILD_DIR = os.path.join(ROOT_DIR, "build")  # 编译输出根目录
    IMAGE_DIR = os.path.join(SRC_DIR, "_static")  # 图片目录
    HTML_DIR = os.path.join(BUILD_DIR, "html")  # HTML 输出根目录
    DOC_TREE_DIR = os.path.join(BUILD_DIR, "doctrees")  # doctrees 目录

    # 删除之前的编译产出
    if os.path.isdir(BUILD_DIR):
        try:
            shutil.rmtree(BUILD_DIR)
        except:
            print(f"目录 {BUILD_DIR} 删除失败!")
            sys.exit(0)

    app = Sphinx(
        srcdir=SRC_DIR,  # source 目录
        confdir=CONFIG_DIR,  # conf.py 的目录
        outdir=HTML_DIR,  # html 输出目录
        doctreedir=DOC_TREE_DIR,  # doctrees 目录
        buildername="html",  # 编译输出格式
        # status=None,      # 打印输出
        # warning=None,     # 告警输出
        warningiserror=True,  # 严格模式
    )

    app.build()  # 编译

    if app.statuscode != 0:
        print("编译失败,请检查输出信息!")
        sys.exit(0)

    """
    app.builder.env.images (app.builder.env.images)是一个字典,描述了项目中的所有图片,结构如下:
    {'_static/34281dec3876fd628d692bc704d541380eb68139.png': ({'sphinx/基础教程', 'sphinx/项目部署'}, '34281dec3876fd628d692bc704d541380eb68139.png'), 
    '_static/cb415eae31351d256f8214b271c8b43266150368.png': ({'sphinx/项目部署'}, 'cb415eae31351d256f8214b271c8b43266150368.png')}

    app.builder.env.all_docs (app.env.all_docs)是一个字典,描述了项目中的所有文档,结构如下:
    {'index': 1766833110783521, 'sphinx/基础教程': 1766833110786802, 'sphinx/最佳实践': 1766833110789712, 'sphinx/项目部署': 1766833110803779, 'sphinx/高阶功能': 1766833110807224}
    """

    rename_dict = rename_files_by_sha1(IMAGE_DIR)  #  {old_name:new_name}

    image_dir_name = Path(IMAGE_DIR).name

    # 更新图片
    for old_name in rename_dict:
        new_name = rename_dict[old_name]
        if old_name != new_name:
            old_path = image_dir_name + "/" + old_name
            new_path = old_path.replace(old_name, new_name)
            for rst_file_path in app.builder.env.images[old_path][0]:
                replace_file(os.path.join(SRC_DIR, rst_file_path), old_path, new_path)


if __name__ == "__main__":
    sphinx_format()
