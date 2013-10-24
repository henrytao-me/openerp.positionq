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

class ir_model_access(osv.osv):
    _inherit = 'ir.model.access'
    _columns = {
        'perm_manage': fields.boolean('Manage Access'),
    }

ir_model_access()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: