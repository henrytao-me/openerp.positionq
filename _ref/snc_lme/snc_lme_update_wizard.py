# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode

class snc_lme_update_wizard(osv.osv_memory):
        
    def save_snc_lme_update(self, cr, uid, ids, vals, context=None):
        obj = self.pool.get('snc.truc.gia.lme')
        obj.fetch_lme_data(cr, uid, vals)
        return {
                'name': _('Tổng hợp LME'),
                'view_type': 'form',
                'view_mode': 'tree',
                'res_model': 'snc.lme',
                'type': 'ir.actions.act_window',
                'target': 'current',
                }           
    
    ###################################################################
          
    _name = 'snc.lme.update.wizard'
    _description = 'Cap Nhat Truc gia LME'
    _columns = {
        'name': fields.char('Name', size=8),
    }
    _defaults = {}
    
snc_lme_update_wizard()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

