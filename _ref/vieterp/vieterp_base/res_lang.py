# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.osv.fields import datetime as datetime_field
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from unidecode import unidecode
import types
from openerp import tools

import locale
from locale import localeconv
import re
from openerp.tools.safe_eval import safe_eval as eval

_logger = logging.getLogger(__name__)


class res_lang(osv.osv):
    
    _inherit = 'res.lang'
    _columns = {
    }
    
    def load_lang(self, cr, uid, lang, lang_name=None):
        # create the language with locale information
        fail = True
        iso_lang = tools.get_iso_codes(lang)
        for ln in tools.get_locales(lang):
            try:
                locale.setlocale(locale.LC_ALL, str(ln))
                fail = False
                break
            except locale.Error:
                continue
        if fail:
            lc = locale.getdefaultlocale()[0]
            msg = 'Unable to get information for locale %s. Information from the default locale (%s) have been used.'
            _logger.warning(msg, lang, lc)

        if not lang_name:
            lang_name = tools.ALL_LANGUAGES.get(lang, lang)


        def fix_xa0(s):
            """Fix badly-encoded non-breaking space Unicode character from locale.localeconv(),
               coercing to utf-8, as some platform seem to output localeconv() in their system
               encoding, e.g. Windows-1252"""
            if s == '\xa0':
                return '\xc2\xa0'
            return s

        def fix_datetime_format(format):
            """Python's strftime supports only the format directives
               that are available on the platform's libc, so in order to
               be 100% cross-platform we map to the directives required by
               the C standard (1989 version), always available on platforms
               with a C standard implementation."""
            for pattern, replacement in tools.DATETIME_FORMATS_MAP.iteritems():
                format = format.replace(pattern, replacement)
            return str(format)

        lang_info = {
            'code': lang,
            'iso_code': iso_lang,
            'name': lang_name,
            'translatable': 1,
            'date_format' : iso_lang == 'vi_VN' and '%d/%m/%Y' or fix_datetime_format(locale.nl_langinfo(locale.D_FMT)),
            'time_format' : iso_lang == 'vi_VN' and '%H:%M:%S' or fix_datetime_format(locale.nl_langinfo(locale.T_FMT)),
            'decimal_point' : iso_lang == 'vi_VN' and ',' or fix_xa0(str(locale.localeconv()['decimal_point'])),
            'thousands_sep' : iso_lang == 'vi_VN' and '.' or fix_xa0(str(locale.localeconv()['thousands_sep'])),
            'grouping': '[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]',
        }
        lang_id = False
        try:
            lang_id = self.create(cr, uid, lang_info)
        finally:
            tools.resetlocale()
        return lang_id
    
res_lang()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: