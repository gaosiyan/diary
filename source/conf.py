import sys
import os

sys.path.insert(0, os.path.abspath("."))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "diary"
copyright = "2025, gaosiyan"
author = "gaosiyan"
release = "0.0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "extensions.giscus",  # 添加 giscus 扩展
]

# https://giscus.app/zh-CN
# Giscus 配置
# 重要：你需要从 https://giscus.app 获取这些值
giscus_category = "Announcements"  # 你的分类名
giscus_category_id = "DIC_kwDOPbjS8s4CuAmL"  # 你的分类ID，需要替换为实际值

# 其他可选配置（使用默认值即可）
giscus_mapping = "pathname"  # 映射方式：pathname, title, url, og:title
giscus_reactions = "1"  # 是否启用反应：1 启用，0 禁用
giscus_metadata = "0"  # 是否发送元数据
giscus_position = "bottom"  # 输入框位置：bottom, top
giscus_theme = "light"  # 主题：light, dark, transparent_dark, preferred_color_scheme
giscus_lang = "zh_CN"  # 语言
giscus_loading = "lazy"  # 加载方式：lazy, eager

templates_path = ["_templates"]
exclude_patterns = []

language = "zh_CN"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static", "."]
