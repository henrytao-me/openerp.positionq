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


class res_groups(osv.osv):
    
    def default_is_project_specific(self, cr, uid, context=None):
        if not context:
            context = {}
        res = context.get('is_project_specific', False)
        return res
    
    _inherit = 'res.groups'
    _columns = {
        'special_user': fields.many2one('res.users', string="Special User"),
        'is_project_specific': fields.boolean('Chỉ dùng riêng cho dự án hiện tại?')
    }
    _defaults = {        
        'is_project_specific': default_is_project_specific,
    }
    _order = 'is_project_specific, special_user, category_id, name'
    
    def write(self, cr, uid, ids, vals, context=None):
        res = super(res_groups, self).write(cr, uid, ids, vals, context=context)
        self.pool.get('ir.model.access.new')._is_reload = True
        return res
    
    def create(self, cr, uid, vals, context=None):    
        res = super(res_groups, self).create(cr, uid, vals, context=context)
        self.pool.get('ir.model.access.new')._is_reload = True
        return res
    
res_groups()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: