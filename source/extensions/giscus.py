# extensions/giscus.py
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx.application import Sphinx

class GiscusComments(Directive):
    """添加 giscus 评论的指令
    
    用法:
    .. giscus::
    
    或自定义主题:
    .. giscus::
       :theme: dark
       
    或自定义语言:
    .. giscus::
       :lang: en
       
    或禁用反应:
    .. giscus::
       :reactions: 0
    """
    
    option_spec = {
        'mapping': directives.unchanged,
        'reactions': directives.unchanged,
        'metadata': directives.unchanged,
        'position': directives.unchanged,
        'theme': directives.unchanged,
        'lang': directives.unchanged,
        'loading': directives.unchanged,
    }
    
    def run(self):
        # 获取 Sphinx 应用配置
        app = self.state.document.settings.env.app
        config = app.config
        
        # 使用配置或选项中的值（选项优先）
        mapping = self.options.get('mapping', getattr(config, 'giscus_mapping', 'pathname'))
        reactions = self.options.get('reactions', getattr(config, 'giscus_reactions', '1'))
        metadata = self.options.get('metadata', getattr(config, 'giscus_metadata', '0'))
        position = self.options.get('position', getattr(config, 'giscus_position', 'bottom'))
        theme = self.options.get('theme', getattr(config, 'giscus_theme', 'light'))
        lang = self.options.get('lang', getattr(config, 'giscus_lang', 'zh-CN'))
        loading = self.options.get('loading', getattr(config, 'giscus_loading', 'lazy'))
        
        # 你的固定配置
        repo = "gaosiyan/Discussions"
        repo_id = "R_kgDOPbjS8g"
        
        # 注意：你需要设置正确的分类名和分类ID
        # 可以从 https://giscus.app 获取，或者从你的仓库 Discussions 设置中获取
        category = getattr(config, 'giscus_category', 'Announcements')
        category_id = getattr(config, 'giscus_category_id', '')
        
        # 构建 HTML
        html = f'''
<div class="giscus-container" style="margin-top: 3rem; padding-top: 2rem; border-top: 1px solid #e1e4e8;">
    <script src="https://giscus.app/client.js"
            data-repo="{repo}"
            data-repo-id="{repo_id}"
            data-category="{category}"
            data-category-id="{category_id}"
            data-mapping="{mapping}"
            data-strict="0"
            data-reactions-enabled="{reactions}"
            data-emit-metadata="{metadata}"
            data-input-position="{position}"
            data-theme="{theme}"
            data-lang="{lang}"
            data-loading="{loading}"
            crossorigin="anonymous"
            async>
    </script>
</div>
'''
        return [nodes.raw('', html, format='html')]

def setup(app: Sphinx):
    """设置 Sphinx 扩展"""
    
    # 添加配置项（可在 conf.py 中覆盖）
    app.add_config_value('giscus_category', 'Announcements', 'html')
    app.add_config_value('giscus_category_id', '', 'html')
    app.add_config_value('giscus_mapping', 'pathname', 'html')
    app.add_config_value('giscus_reactions', '1', 'html')
    app.add_config_value('giscus_metadata', '0', 'html')
    app.add_config_value('giscus_position', 'bottom', 'html')
    app.add_config_value('giscus_theme', 'light', 'html')
    app.add_config_value('giscus_lang', 'zh-CN', 'html')
    app.add_config_value('giscus_loading', 'lazy', 'html')
    
    # 注册指令
    app.add_directive("giscus", GiscusComments)
    
    # 添加 CSS 样式
    app.add_css_file('giscus.css')
    
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }