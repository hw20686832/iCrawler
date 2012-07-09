import inspect

from scrapy.utils.misc import walk_modules
from scrapy.conf import settings

from yowa.utils.redis_service import cs
from yowa.utils.q2b import strQ2B

class ParserManager(object):

    def __init__(self, domain):
        self.base = settings.get('TEMPLATE_MODULES', 'yowa.templates')
        self.template_module = '.'.join((self.base, domain))
        self._parsers = {}
        for module in walk_modules(self.template_module):
            self._filter_parsers(module)

    def _filter_parsers(self, module):
        for pscls in self.iter_parser_classes(module):
            self._parsers[pscls.name] = pscls

    def iter_parser_classes(self, module):
        from yowa.templates.BaseTemplate import Base
    
        for obj in vars(module).itervalues():
            if inspect.isclass(obj) and \
               issubclass(obj, Base) and \
               obj.__module__ == module.__name__ and \
               getattr(obj, 'name', None):
                yield obj

    def create(self, parser_name, **parser_kwargs):
        try:
            pscls = self._parsers[parser_name]
        except KeyError:
            raise KeyError("Parser template not found: %s" % parser_name)

        return pscls(**parser_kwargs)

    def list(self):
        return self._parsers.keys()


__all__ = ['cs', 'strQ2B', 'ParserManager']
