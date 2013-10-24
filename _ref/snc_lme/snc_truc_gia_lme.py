# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode

class snc_truc_gia_lme(osv.osv):

    def function_abc(self, cr, uid, ids, fields, args, context=None):
        if not context:
            context = {}
        res = {}.fromkeys(ids, {})
        for data in self.read(cr, uid, ids, ['last', 'open', 'high', 'low'], context=context):
            res[data['id']].update(self.get_other_values(cr, uid, ids, 
                                                         data['last'], 
                                                         data['open'], 
                                                         data['high'], 
                                                         data['low'], 
                                                         context=context))
        return res
    
    def function_ngay_gio_tao(self, cr, uid, ids, fields, args, context=None):
        res = {}.fromkeys(ids, {})
        for data in self.read(cr, uid, ids, ['ngay_gio_tao'], context=context):
            tmp_UTC = datetime.datetime.strptime(data['ngay_gio_tao'], DEFAULT_SERVER_DATETIME_FORMAT)
            tmp_in_user_timezone = datetime_field.context_timestamp(cr, uid, tmp_UTC, context=context)
            
            res[data['id']]['ngay_tao'] = tmp_in_user_timezone.strftime(DEFAULT_SERVER_DATE_FORMAT)
            res[data['id']]['gio_tao'] = tmp_in_user_timezone.strftime('%H:%M')
        return res
    
    def function_rates(self, cr, uid, ids, fields, args, context=None):
        res = {}.fromkeys(ids, self.get_rates(cr, uid, context=context))
        return res
    
    def get_rates(self, cr, uid, context=None):
        rate_USD_VND = 0
        rate_USD_CNY = 0
        
        currency_obj = self.pool.get('res.currency')
        CNY_id = currency_obj.search(cr, uid, [('name', '=', 'CNY')])
        if CNY_id:
            CNY = currency_obj.read(cr, uid, CNY_id[0], ['rate'], context=context)
            rate_USD_CNY = CNY['rate']
            
        VND_id = currency_obj.search(cr, uid, [('name', '=', 'VND')])
        if VND_id:
            VND = currency_obj.read(cr, uid, VND_id[0], ['rate'], context=context)
            rate_USD_VND = VND['rate']
        
        res = {'rate_USD_VND': rate_USD_VND, 'rate_USD_CNY': rate_USD_CNY}
        return res
    
    def default_rate_USD_VND(self, cr, uid, context=None):
        return self.get_rates(cr, uid, context=context)['rate_USD_VND']
    
    def default_rate_USD_CNY(self, cr, uid, context=None):
        return self.get_rates(cr, uid, context=context)['rate_USD_CNY']
    
    def function_close(self, cr, uid, ids, fields, args, context=None):
        res = {}
        for obj in self.read(cr, uid, ids, ['ngay_tao']):
            vals = {
                'close': 0,
                'cash': 0
            }
            lme_ids = self.pool.get('snc.lme').search(cr, uid, [('name', '=', obj['ngay_tao'])])
            if lme_ids:
                tmp = self.pool.get('snc.lme').read(cr, uid, lme_ids[0], ['close', 'cash'])
                vals.update({
                    'close': tmp['close'],
                    'cash': tmp['cash']
                })
            res[obj['id']] = vals
        return res
     
    def def_open(self, cr, uid, context=None):
        res = 0
        ids = self.search(cr, uid, [], limit=1, order="ngay_gio_tao desc")
        if ids:
            res = self.read(cr, uid, ids[0], ['open'])['open']
        return res
    
    def def_high(self, cr, uid, context=None):
        res = 0
        ids = self.search(cr, uid, [], limit=1, order="ngay_gio_tao desc")
        if ids:
            res = self.read(cr, uid, ids[0], ['high'])['high']
        return res
    
    def def_low(self, cr, uid, context=None):
        res = 0
        ids = self.search(cr, uid, [], limit=1, order="ngay_gio_tao desc")
        if ids:
            res = self.read(cr, uid, ids[0], ['low'])['low']
        return res
     
    _name = 'snc.truc.gia.lme'
    _rec_name = 'ngay_tao'
    _description = 'Truc Gia LME'
    _columns = {
        'name': fields.char('Name', size=1),
        
        'ngay_gio_tao': fields.datetime('Ngày giờ tạo', required=True),
        'gio_tao': fields.function(function_ngay_gio_tao, method=True, string='Giờ tạo', type='char', size=5, multi='ngay_gio_tao',
                                   store={
                                        'snc.truc.gia.lme': (lambda self, cr, uid, ids, *args: ids, ['ngay_gio_tao'], 5),
                                    }),
        'ngay_tao': fields.function(function_ngay_gio_tao, method=True, string='Ngày tạo', type='date', multi='ngay_gio_tao',
                                   store={
                                        'snc.truc.gia.lme': (lambda self, cr, uid, ids, *args: ids, ['ngay_gio_tao'], 5),
                                    }),
        
        'last': fields.float('Last', digits=(16, 2), required=True),
        'volume': fields.float('Volume', digits=(16, 2), required=True),
        'open': fields.float('Open', digits=(16, 2), required=True),
        'high': fields.float('High', digits=(16, 2), required=True),
        'low': fields.float('Low', digits=(16, 2), required=True),
        
        'close': fields.function(function_close, method=True, string="Close", type="float", digits=(16,2), multi="function_close"),
        'cash': fields.function(function_close, method=True, string="Cash", type="float", digits=(16,2), multi="function_close"),
        
        'rate_USD_VND': fields.function(function_rates, method=True, string='USD/VND', type='float', multi='rates', digits=(16, 2)),
        'rate_USD_CNY': fields.function(function_rates, method=True, string='USD/CNY', type='float', multi='rates', digits=(16, 2)),
        
        'last_usdc_lb': fields.function(function_abc, method=True, type='float', string='Last', digits=(16, 2), readonly=True, multi='abc'),
        'open_usdc_lb': fields.function(function_abc, method=True, type='float', string='Open', digits=(16, 2), readonly=True, multi='abc'),
        'high_usdc_lb': fields.function(function_abc, method=True, type='float', string='High', digits=(16, 2), readonly=True, multi='abc'),
        'low_usdc_lb': fields.function(function_abc, method=True, type='float', string='Low', digits=(16, 2), readonly=True, multi='abc'),
        
        'last_cny_tan': fields.function(function_abc, method=True, type='float', string='Last', digits=(16, 2), readonly=True, multi='abc'),
        'open_cny_tan': fields.function(function_abc, method=True, type='float', string='Open', digits=(16, 2), readonly=True, multi='abc'),
        'high_cny_tan': fields.function(function_abc, method=True, type='float', string='High', digits=(16, 2), readonly=True, multi='abc'),
        'low_cny_tan': fields.function(function_abc, method=True, type='float', string='Low', digits=(16, 2), readonly=True, multi='abc'),
        
        'last_vnd_kg': fields.function(function_abc, method=True, type='float', string='Last', digits=(16, 2), readonly=True, multi='abc'),
        'open_vnd_kg': fields.function(function_abc, method=True, type='float', string='Open', digits=(16, 2), readonly=True, multi='abc'),
        'high_vnd_kg': fields.function(function_abc, method=True, type='float', string='High', digits=(16, 2), readonly=True, multi='abc'),
        'low_vnd_kg': fields.function(function_abc, method=True, type='float', string='Low', digits=(16, 2), readonly=True, multi='abc'),
        
        'create_date': fields.datetime('Create date', readonly=True),
        'user_id': fields.many2one('res.users', string="Người tạo",readonly=True),
    }
    _defaults = {
        'name': lambda *x: '/',
        'ngay_gio_tao': lambda *x: datetime.datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
        'rate_USD_VND': default_rate_USD_VND,
        'rate_USD_CNY': default_rate_USD_CNY,
        'user_id': lambda self, cr, uid, context=None: uid,
        'open': def_open,
        'high': def_high,
        'low': def_low
    }
    _order = 'ngay_gio_tao desc'
    
    def read_group(self, cr, uid, domain, fields, groupby, offset=0, limit=None, context=None, orderby=False):
        if context is None:
            context = {}
        if context.get('search_ngay_tao_hom_nay', False):
            to_search_ngay_tao_hom_nay = True
            for d in domain:
                if d[0] == 'ngay_tao':
                    to_search_ngay_tao_hom_nay = False
                    break
            if to_search_ngay_tao_hom_nay:
                domain.append(('ngay_tao', '=', datetime.datetime.now().strftime(DEFAULT_SERVER_DATE_FORMAT)))
        return super(snc_truc_gia_lme, self).read_group(cr, uid, domain, fields, groupby, offset=offset, limit=limit, context=context, orderby=orderby)
    
    def get_other_values(self, cr, uid, ids, last, open, high, low, context=None):
        res = {}
        
        # get all needed Unit of Measures.
        uom_obj = self.pool.get('product.uom')
        tan_uom_id = uom_obj.search(cr, uid, [('name', '=', 'tấn')])
        tan_uom_id = tan_uom_id and tan_uom_id[0] or False
        lb_uom_id = uom_obj.search(cr, uid, [('name', '=', 'Lb')])
        lb_uom_id = lb_uom_id and lb_uom_id[0] or False
        kg_uom_id = uom_obj.search(cr, uid, [('name', '=', 'kg')])
        kg_uom_id = kg_uom_id and kg_uom_id[0] or False
        
        # get all needed currencies.
        currency_obj = self.pool.get('res.currency')
        USD_id = currency_obj.search(cr, uid, [('name', '=', 'USD')])
        USD_id = USD_id and USD_id[0] or False
        CNY_id = currency_obj.search(cr, uid, [('name', '=', 'CNY')])
        CNY_id = CNY_id and CNY_id[0] or False
        VND_id = currency_obj.search(cr, uid, [('name', '=', 'VND')])
        VND_id = VND_id and VND_id[0] or False
        
        last_usdc_lb = open_usdc_lb = high_usdc_lb = low_usdc_lb = 0
        last_cny_tan = open_cny_tan = high_cny_tan = low_cny_tan = 0
        last_vnd_kg = open_vnd_kg = high_vnd_kg = low_vnd_kg = 0
        
        if tan_uom_id:
            if lb_uom_id:
                last_usdc_lb = uom_obj._compute_price(cr, uid, tan_uom_id, last, lb_uom_id) * 100
                open_usdc_lb = uom_obj._compute_price(cr, uid, tan_uom_id, open, lb_uom_id) * 100
                high_usdc_lb = uom_obj._compute_price(cr, uid, tan_uom_id, high, lb_uom_id) * 100
                low_usdc_lb = uom_obj._compute_price(cr, uid, tan_uom_id, low, lb_uom_id) * 100
            
            if CNY_id and USD_id:
                last_cny_tan = currency_obj.compute(cr, uid, USD_id, CNY_id, last, round=False, context=context)
                open_cny_tan = currency_obj.compute(cr, uid, USD_id, CNY_id, open, round=False, context=context)
                high_cny_tan = currency_obj.compute(cr, uid, USD_id, CNY_id, high, round=False, context=context)
                low_cny_tan = currency_obj.compute(cr, uid, USD_id, CNY_id, low, round=False, context=context)
            
            if VND_id and USD_id and kg_uom_id:
                last_vnd_kg = currency_obj.compute(cr, uid, USD_id, VND_id, last, round=False, context=context)
                open_vnd_kg = currency_obj.compute(cr, uid, USD_id, VND_id, open, round=False, context=context)
                high_vnd_kg = currency_obj.compute(cr, uid, USD_id, VND_id, high, round=False, context=context)
                low_vnd_kg = currency_obj.compute(cr, uid, USD_id, VND_id, low, round=False, context=context)
                
                last_vnd_kg = uom_obj._compute_price(cr, uid, tan_uom_id, last_vnd_kg, kg_uom_id)
                open_vnd_kg = uom_obj._compute_price(cr, uid, tan_uom_id, open_vnd_kg, kg_uom_id)
                high_vnd_kg = uom_obj._compute_price(cr, uid, tan_uom_id, high_vnd_kg, kg_uom_id)
                low_vnd_kg = uom_obj._compute_price(cr, uid, tan_uom_id, low_vnd_kg, kg_uom_id)
        
        res['last_usdc_lb'] = last_usdc_lb
        res['open_usdc_lb'] = open_usdc_lb
        res['high_usdc_lb'] = high_usdc_lb
        res['low_usdc_lb'] = low_usdc_lb
        
        res['last_cny_tan'] = last_cny_tan
        res['open_cny_tan'] = open_cny_tan
        res['high_cny_tan'] = high_cny_tan
        res['low_cny_tan'] = low_cny_tan
        
        res['last_vnd_kg'] = last_vnd_kg
        res['open_vnd_kg'] = open_vnd_kg
        res['high_vnd_kg'] = high_vnd_kg
        res['low_vnd_kg'] = low_vnd_kg
        
        return res

    def onchange_values(self, cr, uid, ids, last, open, high, low, context=None):
        res = {'value': {}}
        res['value'].update(self.get_other_values(cr, uid, ids, last, open, high, low, context=context))
        return res

#     def get_lme_in_quarter(self, cr, uid, from_date, context=None):
#         res = 0
#         quarter = self.pool.get('vieterp.utils').get_this_quarter(cr, uid, from_date)        
#         #get open
#         open = 0
#         tmp = quarter
#         day = self.pool.get('vieterp.utils').get_day(cr, uid, tmp)
#         if day == 1 or day == 7:
#             monday = datetime.datetime.strptime(tmp, DEFAULT_SERVER_DATE_FORMAT) + datetime.timedelta(7)
#             monday = self.pool.get('vieterp.utils').get_this_monday(cr, uid, monday)
#             tmp = monday.strftime(DEFAULT_SERVER_DATE_FORMAT)
#         open = self.get_info_ngay(cr, uid, tmp, context).get('open', 0)
#         #get close
#         close = 0        
#         tmp = datetime.datetime.strptime(quarter, DEFAULT_SERVER_DATE_FORMAT) + datetime.timedelta(35)
#         tmp = self.pool.get('vieterp.utils').get_this_quarter(cr, uid, tmp) - datetime.timedelta(1)
#         day = self.pool.get('vieterp.utils').get_day(cr, uid, tmp)
#         if day == 1 or day == 7:
#             tmp = self.pool.get('vieterp.utils').get_this_friday(cr, uid, tmp)
#         tmp = tmp.strftime(DEFAULT_SERVER_DATE_FORMAT)
#         close = self.get_info_ngay(cr, uid, tmp, context).get('close', 0)
#         #
#         res = close - open
#         #
#         return res  
#
#     def default_get(self, cr, uid, fields, context=None):
#         if context is None:
#             context = {}
#         res = super(snc_truc_gia_lme, self).default_get(cr, uid, fields, context=context)
#         ids = self.search(cr, uid, [], context=context)
#         if ids:
#             last_data = self.read(cr, uid, ids[0], ['open', 'high', 'low'], context=context)
#             res.update({'open': last_data['open'], 'high': last_data['high'], 'low': last_data['low']})
#         return res
#     
#     
#     
#     
#     def create(self, cr, uid, vals, context=None):
#         res = {}
# #         res = self.read(cr, uid, ['ngay_gio_tao'], context=context)
# #         res = res and res[0] or {}
#         
#         tmp_UTC = datetime.datetime.strptime(vals.get('ngay_gio_tao'), DEFAULT_SERVER_DATETIME_FORMAT)
#         tmp_reformat = datetime_field.context_timestamp(cr, uid, tmp_UTC, context=context)
#         lme_date = tmp_reformat.strftime(DEFAULT_SERVER_DATE_FORMAT)
#         
#         vals1 ={'name':lme_date,
#                } 
#         
#         snc_lme_obj = self.pool.get('snc.lme')
#         lme_ids = snc_lme_obj.search(cr, uid, [('name','=',lme_date)])
#         
#         if lme_ids: 
#             pass 
#         else:
#             lme_id = snc_lme_obj.create(cr, uid, vals1, context = context)
#             vals.update({'lme_id': lme_id})
#                 
#             #start
#             res = super(snc_truc_gia_lme, self).create(cr, uid, vals, context=context)                                      
#         
#         return res
#     
#     
#     def get_last_lme(self, cr, uid):
#         res = 0
#         ids = self.search(cr, uid, [], limit=1)
#         if ids:
#             data = self.read(cr, uid, ids[0], ['last'])
#             res = data['last']        
#         return res
#     
#     def get_info(self, cr, uid, from_date, type="ngay", context=None):
#         res = {}
#         if type == 'ngay':
#             res = self.get_info_ngay(cr, uid, from_date, context)
#         elif type == 'tuan':
#             res = self.get_info_tuan(cr, uid, from_date, context)
#         return res
#     
#     def get_info_ngay(self, cr, uid, from_date, context=None):
#         if not context:
#             context = {}
#         res = {}
#         if isinstance(from_date, datetime.datetime):
#             from_date = from_date.strftime(DEFAULT_SERVER_DATE_FORMAT)
#         ids = self.search(cr, uid, [('ngay_tao', '=', from_date)], limit=1)
#         if ids:
#             obj = self.read(cr, uid, ids[0], ['ngay_tao', 'fn_open', 'fn_high', 
#                                               'fn_low', 'fn_close', 'fn_trend', 'fn_volume'])
#             if obj['fn_close'] > 0:
#                 res.update({
#                     'volume': obj['fn_volume'],
#                     'open': obj['fn_open'],
#                     'high': obj['fn_high'],
#                     'low': obj['fn_low'],
#                     'close': obj['fn_close'],
#                     'trend': obj['fn_trend']
#                 })
#         if not res and context.get('init', False):
#             res = {
#                 'open': 0,
#                 'high': 0,
#                 'low': 0,
#                 'close': 0,
#                 'trend': 0
#             }
#         return res
#     
#     def get_info_tuan(self, cr, uid, from_date, context=None):
#         if not context:
#             context = {}
#         res = {}
#         if isinstance(from_date, datetime.datetime):
#             from_date = from_date.strftime(DEFAULT_SERVER_DATE_FORMAT)
#         
#         from_date = self.pool.get('vieterp.utils').get_this_monday(cr, uid, from_date)
#         to_date = self.pool.get('vieterp.utils').get_this_friday(cr, uid, from_date)
#         
#         ids = self.search(cr, uid, [('ngay_tao', '>=', from_date),
#                                     ('ngay_tao', '<=', to_date)])
#         date_log = {}
#         date_res = {}
#         if ids:
#             for obj in self.read(cr, uid, ids, ['ngay_tao', 'fn_open', 'fn_high', 
#                                               'fn_low', 'fn_close', 'fn_trend', 'fn_volume']):
#                 if date_log.get(obj['ngay_tao']):
#                     continue
#                 date_log.update({obj['ngay_tao']: True})
#                 if obj['fn_close'] > 0:
#                     #volume
#                     res.update({'volume': res.get('volume', 0) + obj['fn_volume']})
#                     #open
#                     if not date_res.get('open') or date_res.get('open', '') > obj['ngay_tao']:
#                         date_res.update({'open': obj['ngay_tao']})
#                         res.update({'open': obj['fn_open']})
#                     #close
#                     if not date_res.get('close') or date_res.get('close', '') < obj['ngay_tao']:
#                         date_res.update({'close': obj['ngay_tao']})
#                         res.update({'close': obj['fn_close']})
#                     #high
#                     if not res.get('high') or res.get('high', -1) < obj['fn_high']:
#                         res.update({'high': obj['fn_high']})
#                     #low
#                     if not res.get('low') or res.get('low', -1) > obj['fn_low']:
#                         res.update({'low': obj['fn_low']})
#         
#         if res:
#             if res.get('close') > res.get('open'):
#                 res.update({'trend': 1})
#             else:
#                 res.update({'trend': -1}) 
#         
#         if not res and context.get('init', False):
#             res = {
#                 'volume': 0,
#                 'open': 0,
#                 'high': 0,
#                 'low': 0,
#                 'close': 0,
#                 'trend': 0
#             }
#         return res
#     


    
snc_truc_gia_lme()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

