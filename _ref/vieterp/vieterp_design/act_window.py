# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode

class act_window(osv.osv):

    _inherit = 'ir.actions.act_window'
    _columns = {
        'vbase': fields.boolean('VietERP Base Action', readonly=True),
    }
    
    _defaults = {
        'vbase': lambda self,cr,uid,ctx={}: ctx.get('vbase', False)
    }
    
act_window()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

