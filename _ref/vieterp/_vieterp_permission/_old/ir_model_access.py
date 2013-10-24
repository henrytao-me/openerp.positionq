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
    
    SELECTION = (('Yes', 'Yes'),
                ('No', 'No'),
                ('Inherit', 'Inherit'))
   
    _inherit = 'ir.model.access'
    _columns = {
        'perm_manage': fields.boolean('Manage Access'),
        
        'perm_read_new': fields.selection(SELECTION, string='Quyền xem', required=True),
        'perm_unlink_new': fields.selection(SELECTION, string='Quyền xoá', required=True),
        'perm_write_new': fields.selection(SELECTION, string='Quyền sửa', required=True),
        'perm_create_new': fields.selection(SELECTION, string='Quyền tạo', required=True),
        
#         'perm_read': fields.function(function_perm, method=True, type='boolean', string='Quyền xem',
#                                      store=True, readonly=True, multi='perm'),
#         'perm_write': fields.function(function_perm, method=True, type='boolean', string='Quyền sửa',
#                                      store=True, readonly=True, multi='perm'),
#         'perm_create': fields.function(function_perm, method=True, type='boolean', string='Quyền tạo',
#                                      store=True, readonly=True, multi='perm'),
#         'perm_unlink': fields.function(function_perm, method=True, type='boolean', string='Quyền xoá',
#                                      store=True, readonly=True, multi='perm'),
    }
    _defaults = {
        'perm_read_new': lambda *x: 'Inherit',
        'perm_unlink_new': lambda *x: 'Inherit',
        'perm_write_new': lambda *x: 'Inherit',
        'perm_create_new': lambda *x: 'Inherit',
    }
    
ir_model_access()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: