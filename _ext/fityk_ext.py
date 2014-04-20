# this is hack is needed to use our layout.html on ReadTheDocs
from sphinx.jinja2glue import BuiltinTemplateLoader
from jinja2 import TemplateNotFound
class MyTemplateLoader(BuiltinTemplateLoader):
    def get_source(self, environment, template):
        # If template name in Jinja's "extends" is prepended with "!"
        # Sphinx skips project's template paths.
        # In BuiltinTemplateLoader self.templatepathlen is used to remove
        # project's template paths and leave only Sphinx's paths.
        # This hack should leave the last path, so "!layout.html" will find
        # the template from Fityk. To avoid recursion, Fityk template
        # is not using "!".
        print("\n(MyTemplateLoader.get_source) searching for %s" % template)
        loaders = self.loaders
        # exclamation mark starts search from theme
        if template.startswith('!'):
            loaders = loaders[self.templatepathlen-1:]
            template = template[1:]
        for loader in loaders:
            print("\ttrying in: %s" % ":".join(loader.searchpath))
            try:
                return loader.get_source(environment, template)
            except TemplateNotFound:
                pass
        raise TemplateNotFound(template)
