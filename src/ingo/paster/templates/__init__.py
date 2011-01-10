from paste.deploy.converters import asbool
from paste.script.templates import Template, var
from tempita import paste_script_template_renderer

class ExtensionTemplate(Template):
    _template_dir = ('ingo.paster', 'templates/extension')
    template_renderer = staticmethod(paste_script_template_renderer)
    
    summary = 'inGo extension template'
    egg_plugins = ['PasteScript', 'inGo']
    vars = []
    ensure_names = ['description', 'author', 'author_email', 'url']
    
    def pre(self, command, output_dir, vars):
        """Called before template is applied."""
        package_logger = vars['package']
        if package_logger == 'root':
            # Rename the app logger in the rare case a extension is named 'root'
            package_logger = 'root_ext'
        vars['package_logger'] = package_logger

        # Ensure these exist in the namespace
        for name in self.ensure_names:
            vars.setdefault(name, '')

        vars['version'] = vars.get('version', '0.1')
        vars['zip_safe'] = asbool(vars.get('zip_safe', 'false'))