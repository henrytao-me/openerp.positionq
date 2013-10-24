# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode

MODULE_UNINSTALL_FLAG = '_force_unlink'

class ir_model(osv.osv):
    
    _inherit = 'ir.model'
    _columns = {
        'vbase': fields.boolean('VietERP Base Object')
    }
    _defaults = {
        'vbase': lambda self,cr,uid,ctx={}: ctx.get('vbase', False),
        'state': lambda self,cr,uid,ctx={}: 'base' if ctx.get('vbase', False) == True else ((ctx and ctx.get('manual',False)) and 'manual' or 'base'),
    }
    
    def create(self, cr, user, vals, context=None):
        if  context is None:
            context = {}    
        res = super(ir_model, self).create(cr, user, vals, context=context)
        if context.get('vbase', False) == True:
            self.write(cr, user, res, {'state': 'base'})
        return res
    
ir_model()

#class x_vieterp_test(osv.osv):
#    
#    _name = 'x_vieterp.test'
#    _description = ''
#    _columns = {
#        'name': fields.char('Name from Code'),
#    }
#    _defaults = {
#        
#    }
#    
#x_vieterp_test()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

