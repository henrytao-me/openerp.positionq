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


class ir_model_depend_detail(osv.osv):
    
    _name = 'ir.model.depend.detail'
    _description = 'Nhom Doi Tuong'
    _columns = {
        'name': fields.many2one('ir.model.depend', string="Group Name", required=True),
        'model': fields.many2one('ir.model', string='Model', required=True,
                                       domain=[('osv_memory','=', False), ('is_project_specific', '=', True)]),
        'is_root': fields.boolean('Root Model')
    }
    _defaults = {
        'is_root': lambda *x: False
    }
    _order = "name, is_root desc, model"
    
    def write(self, cr, uid, ids, vals, context=None):
        res = super(ir_model_depend_detail, self).write(cr, uid, ids, vals, context=context)
        self.pool.get('ir.model.access.new')._is_reload = True
        return res
    
    def create(self, cr, uid, vals, context=None):    
        res = super(ir_model_depend_detail, self).create(cr, uid, vals, context=context)
        self.pool.get('ir.model.access.new')._is_reload = True
        return res
    
ir_model_depend_detail()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: