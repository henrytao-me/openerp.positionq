# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode
import types

class res_groups(osv.osv):
    
    def def_is_public(self, cr, uid, context={}):
        res = context.get('is_public', False)
        return res
    
    _inherit = 'res.groups'
    _columns = {
        'alias': fields.char('Alias', size=64),
        'is_public': fields.boolean('Public Group')
    }
    _defaults = {        
        'is_public': def_is_public
    }
    _order = "is_public desc, category_id, name"
    
res_groups()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: