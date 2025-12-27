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

from utils import calculate_files_sha1_code_parallel


def sphinx_format():
    """
    格式化 sphinx 文档项目
    """
    # 切换工作目录为 Sphinx 项目的 source 目录
    os.chdir(Path(__file__).resolve().parent)

    # 删除之前的编译产出
    build_path = "../build"
    if os.path.isdir(build_path):
        try:
            shutil.rmtree(build_path)
        except:
            print(f"目录 {build_path} 删除失败!")
            sys.exit(0)

    app = Sphinx(
        srcdir=".",   # source 目录
        confdir=".",  # conf.py 的目录
        outdir="../build/html", # 输出目录
        doctreedir="../build/doctrees",
        buildername="html",
        # status=None,           # 打印输出
        # warning=None,
        warningiserror=True,  # 严格模式
    )

    app.build()  # 编译

    if app.statuscode != 0:
        print("编译失败,请检查输出信息!")
        sys.exit(0)

    '''
    app.builder.env.images (app.builder.env.images)是一个字典,描述了项目中的所有图片,结构如下:
    {'_static/34281dec3876fd628d692bc704d541380eb68139.png': ({'sphinx/基础教程', 'sphinx/项目部署'}, '34281dec3876fd628d692bc704d541380eb68139.png'), 
    '_static/cb415eae31351d256f8214b271c8b43266150368.png': ({'sphinx/项目部署'}, 'cb415eae31351d256f8214b271c8b43266150368.png')}

    app.builder.env.all_docs (app.env.all_docs)是一个字典,描述了项目中的所有文档,结构如下:
    {'index': 1766833110783521, 'sphinx/基础教程': 1766833110786802, 'sphinx/最佳实践': 1766833110789712, 'sphinx/项目部署': 1766833110803779, 'sphinx/高阶功能': 1766833110807224}
    '''

    sha1_codes = calculate_files_sha1_code_parallel(list(app.builder.env.images))

    print(sha1_codes)





if __name__ == "__main__":
    sphinx_format()
