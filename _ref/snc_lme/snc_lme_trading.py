# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
import json
from datetime import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode

class snc_lme_trading(osv.osv):
#    SELECTION_TYPE = (('X', _('X - LME Close')),
#                      ('O', _('O - Non prompts LME')),
#                      ('TW', _('TW - Third Wednesday')))
    
    def function_name(self, cr, uid, ids, fields, args, context=None):
        res = {}
        for data in self.read(cr, uid, ids, ['lme_close', 'non_prompts_lme', 'is_third_wednesday'], context=context):
            if data['lme_close'] and data['non_prompts_lme'] and data['is_third_wednesday']:
                res[data['id']] = 'LME Close - Non Prompts LME - Is 3rd Wednesday'
            elif data['lme_close'] and data['non_prompts_lme']:
                res[data['id']] = 'LME Close - Non Prompts LME'
            elif data['non_prompts_lme'] and data['is_third_wednesday']:            
                res[data['id']] = 'Non Prompts LME - Is 3rd Wednesday'
            elif data['lme_close'] and data['is_third_wednesday']:
                res[data['id']] = 'LME Close - Is 3rd Wednesday'
            elif data['lme_close']:
                res[data['id']] = 'LME Close'
            elif data['non_prompts_lme']:
                res[data['id']] = 'Non Prompts LME'
            elif data['is_third_wednesday']:
                res[data['id']] = 'Is 3rd Wednesday'
        return res
    
    _name = 'snc.lme.trading'
    _description = 'LME Trading'
    _columns = {
        'name': fields.function(function_name, method=True, type='char', size=128,
                                string='Loại', store=True),
#        'type': fields.selection(SELECTION_TYPE, string='Loại', required=True),
        'ngay': fields.date('Ngày', required=True),
        'is_third_wednesday': fields.boolean('Is 3rd Wednesday?', readonly=True),
        'lme_close': fields.boolean('LME Close', readonly=True),
        'non_prompts_lme': fields.boolean('Non prompts LME', readonly=True),
    }
    _defaults = {
        'is_third_wednesday': lambda *x: False,
    }
    
    def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False):
        if not context:
            context = {}
        res = super(snc_lme_trading, self).search(cr, uid, args, offset=offset, limit=limit, order=order, context=context, count=count)
        return res
    
#    def mark_3rd_Wednesday(self, cr, uid, context=None):
#        current_year = int(datetime.strftime(datetime.now(), '%Y'))
#        for year in range(current_year - 20, current_year + 20):
#            for month in range(1, 13):
#                for day in range(15, 22):
#                    try:
#                        the_day = date(year, month, day)
#                        if datetime.strftime(the_day, '%A') == 'Wednesday':
#                            the_day = '%d-%02d-%02d' % (year, month, day)
#                            ids = self.search(cr, uid, [('ngay', '=', the_day), ('is_third_wednesday', '=', True)], context=context)
#                            if not ids:
#                                self.create(cr, uid, {'type': 'X', 'is_third_wednesday': True, 'ngay': the_day}, context=context)
#                    except:
#                        break
#        return True
    
    def lme_trading_custom(self, cr, uid, args=None, context=None):
        res = []
#        lme_obj = self.pool.get('snc.lme.trading')
#        lme_ids = lme_obj.search(cr, uid, [])
#        if lme_ids:
#            for data in self.read(cr, uid, lme_ids, ['type', 'is_third_wednesday','ngay'], context=context):
#                del data['id']
#                res.append(data)
#        print res
        return res
    def lme_trading_custom_load(self, cr, uid, args=None, context=None):
        res = []
        
        lme_obj = self.pool.get('snc.lme.trading')
        lme_ids = lme_obj.search(cr, uid, [])
        if lme_ids:
            for data in self.read(cr, uid, lme_ids, ['lme_close', 'non_prompts_lme', 'ngay', 'is_third_wednesday'], context=context):
                del data['id']
                res.append(data)
        print res
        return res
    
    def lme_trading_custom_save(self, cr, uid, args=None, context=None):
        res = False
        lme_obj = self.pool.get('snc.lme.trading')
        
        if args:
            ngay = args.get('ngay')
            if ngay:
                lme_ids = lme_obj.search(cr, uid, [('ngay', '=', str(ngay))])
                if lme_ids:                
                    res = lme_obj.write(cr, uid, lme_ids, args)
                else:
                    lme_obj.create(cr, uid, args)
                    res = True
                
        return res
        
    
snc_lme_trading()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

