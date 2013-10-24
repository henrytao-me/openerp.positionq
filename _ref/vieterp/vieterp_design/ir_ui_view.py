# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode

class view(osv.osv):

    _inherit = 'ir.ui.view'
    _columns = {
        'vbase': fields.boolean('VietERP Base View', readonly=True),
    }
    
    _defaults = {
        'vbase': lambda self,cr,uid,ctx={}: ctx.get('vbase', False)
    }
    
view()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

