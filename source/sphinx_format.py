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


def sphinx_format():
    """
    格式化 sphinx 文档项目
    """
    # 切换到 Sphinx 项目根目录,即 diary 目录
    os.chdir(Path(__file__).resolve().parent.parent)

    # 删除之前的编译产出
    build_path = "build"
    if os.path.isdir(build_path):
        try:
            shutil.rmtree(build_path)
        except:
            print(f"目录 {build_path} 删除失败!")
            sys.exit(0)

    app = Sphinx(
        srcdir="source",
        confdir="source",
        outdir="build/html",
        doctreedir="build/doctrees",
        buildername="html",
        # status=None,           # 打印输出
        # warning=None,
        warningiserror=True,  # 严格模式
    )

    app.build()  # 编译

    if app.statuscode != 0:
        print("编译失败,请检查输出信息!")
        sys.exit(0)

    print(app.builder.env.images)  # 所有图片,或者用 app.env.images
    print(app.builder.env.all_docs)  # 所有文档,或者用 app.env.all_docs


if __name__ == "__main__":
    sphinx_format()
