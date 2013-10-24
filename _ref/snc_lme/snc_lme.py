# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode

class snc_lme(osv.osv):
    
#     def function_get_LME_details(self, cr, uid, ids, fields, args, context=None):
#         if not context:
#             context = {}
#         res = {}
#         for obj in self.read(cr, uid, ids,['name']):
#             vals={
#                    'fn_last':0,
#                    'fn_volume':0,
#                    'fn_open':0,
#                    'fn_high':0,
#                    'fn_low':0,
#             };
#             lme_ids = self.pool.get('snc.truc.gia.lme').search(cr,uid,[('ngay_tao','=',obj['name'])],
#                                               limit=1, order="ngay_gio_tao desc")
#             if lme_ids:
#                 tmp = self.pool.get('snc.truc.gia.lme').read(cr,uid, lme_ids[0], ['last',
#                                                                                    'volume',
#                                                                                    'open',
#                                                                                    'high',
#                                                                                    'low'], context=context)
#                 value.update({
#                     'fn_last': tmp.get('last'),
#                     'fn_volume': tmp.get('volume'),
#                     'fn_open': tmp.get('open'),
#                     'fn_high': tmp.get('high'),
#                     'fn_low': tmp.get('low'),
#                 })
#             res[obj['id']] = vals
#         return res
    
    def function_trend(self, cr, uid, ids, fields, args, context=None):
        res = {}
        for obj in self.read(cr, uid, ids, ['open', 'close']):
            vals = '0',
            if obj['close'] > obj['open']:
                vals = '1'
            elif obj['close'] < obj['open']:
                vals = '-1'
            res[obj['id']] = vals
        return res
    
    _name = 'snc.lme'
    _description = 'Truc Gia LME'
    _columns = {
        'name': fields.date('Ngày'),
        
        'close': fields.float('Close', digits=(16, 2)),
        'cash': fields.float('Cash', digits=(16, 2)),
        'volume': fields.float('Volume', digits=(16, 2)),
        'open': fields.float('Open', digits=(16, 2)),
        'high': fields.float('High', digits=(16, 2)),
        'low': fields.float('Low', digits=(16, 2)),
        
        'trend': fields.function(function_trend, method=True, string="Trend", type="selection", 
                                 selection=[('1', 'Tăng'),
                                            ('0', 'Không xác định'),
                                            ('-1', 'Giảm')]),
        
#         'fn_last': fields.function(function_get_LME_details, method=True, string='Last', 
#                                 type="float", digits=(16, 2), multi="function_get_LME_details"),
#         'fn_volume': fields.function(function_get_LME_details, method=True, string='Volume', 
#                                 type="float", digits=(16, 2), multi="function_get_LME_details"),
#         'fn_open': fields.function(function_get_LME_details, method=True, string='Open', 
#                                 type="float", digits=(16, 2), multi="function_get_LME_details"),
#         'fn_high': fields.function(function_get_LME_details, method=True, string='High', 
#                                 type="float", digits=(16, 2), multi="function_get_LME_details"),
#         'fn_low': fields.function(function_get_LME_details, method=True, string='Low', 
#                                 type="float", digits=(16, 2), multi="function_get_LME_details"),
        
        'create_date': fields.datetime('Create date', readonly=True),
        'user_id': fields.many2one('res.users', string="Create user",readonly=True),
    }
    _defaults = {
        'user_id': lambda self, cr, uid, context=None: uid,
    }
    _order = 'name desc'
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'name is unique'),
    ]
    
    def get_info(self, cr, uid, from_date=None, from_date_time=None, type="ngay", arg="close", init_data=False, context=None):
        res = None
        if not from_date and not from_date_time:
            return res
        if not from_date:
            tmp = datetime.datetime.strptime(from_date_time, DEFAULT_SERVER_DATETIME_FORMAT)
            from_date = tmp.strftime(DEFAULT_SERVER_DATE_FORMAT)
        # ngay
        if type=="ngay":
            res = self.get_info_ngay(cr, uid, from_date, from_date_time, arg, init_data, context)
        # tuan
        elif type=='tuan':
            res = self.get_info_tuan(cr, uid, from_date, init_data, context)
        # thang
        elif type=='thang':
            res = self.get_info_thang(cr, uid, from_date, init_data, context)
        return res
    
    def get_last_info(self, cr, uid, from_date=None, from_date_time=None, type="ngay", arg="close", 
                      init_data=False, context=None):
        res = None
        if not from_date and not from_date_time:
            return res
        if not from_date:
            tmp = datetime.datetime.strptime(from_date_time, DEFAULT_SERVER_DATETIME_FORMAT)
            from_date = tmp.strftime(DEFAULT_SERVER_DATE_FORMAT)
        # ngay
        if type=="ngay":
            if arg == 'close':
                tmp_ids = self.search(cr, uid, [('name', '<', from_date)], limit=1, order="name desc")
                if tmp_ids:
                    from_date = self.read(cr, uid, tmp_ids[0], ['name'])['name']
                    res = self.get_info_ngay(cr, uid, from_date, from_date_time, arg, init_data, context)
                elif init_data == True:
                    res = {
                        'volume': 0,
                        'open': 0,
                        'close': 0,
                        'high': 0,
                        'low': 0,
                        'trend': '0'
                    }
            elif arg == 'last':
                tmp_ids = self.pool.get('snc.truc.gia.lme').search(cr, uid, [('ngay_gio_tao', '<', from_date_time)],
                                                                   limit=1, order="ngay_gio_tao desc")
                if tmp_ids:
                    from_date_time = self.pool.get('snc.truc.gia.lme').read(cr, uid, tmp_ids[0], ['ngay_gio_tao'])['ngay_gio_tao']
                    res = self.get_info_ngay(cr, uid, from_date, from_date_time, arg, init_data, context)
                elif init_data == True:
                    res = {
                        'last': 0,
                        'volume': 0,
                        'open': 0,
                        'high': 0,
                        'low': 0
                    }
        # tuan
        elif type=='tuan':
            from_date = datetime.datetime.strptime(from_date, DEFAULT_SERVER_DATE_FORMAT) - datetime.timedelta(7)
            from_date = from_date.strftime(DEFAULT_SERVER_DATE_FORMAT)
            res = self.get_info_tuan(cr, uid, from_date, init_data, context)
        # thang
        elif type=='thang':
            from_date = datetime.datetime.strptime(from_date, DEFAULT_SERVER_DATE_FORMAT) - datetime.timedelta(35)
            from_date = from_date.strftime(DEFAULT_SERVER_DATE_FORMAT)
            res = self.get_info_thang(cr, uid, from_date, init_data, context)
        return res
    
    def get_info_from_range(self, cr, uid, from_date, to_date, init_data=None, context=None):
        res = None
        ids = self.search(cr, uid, [('name', '>=', from_date),
                                    ('name', '<=', to_date)])
        date_res = {}
        if ids:
            res = {
                'volume': 0,
                'open': 0,
                'close': 0,
                'high': 0,
                'low': 0,
                'trend': '0'
            }
            for obj in self.read(cr, uid, ids, ['name', 'open', 'high', 
                                                'low', 'close', 'volume']):
                #volume
                res.update({'volume': res.get('volume', 0) + obj['volume']})
                #open
                if not date_res.get('open') or date_res.get('open', '') > obj['name']:
                    date_res.update({'open': obj['name']})
                    res.update({'open': obj['open']})
                #close
                if not date_res.get('close') or date_res.get('close', '') < obj['name']:
                    date_res.update({'close': obj['name']})
                    res.update({'close': obj['close']})
                #high
                if not res.get('high') or res.get('high', -1) < obj['high']:
                    res.update({'high': obj['high']})
                #low
                if not res.get('low') or res.get('low', -1) > obj['low']:
                    res.update({'low': obj['low']})
            if res.get('close') > res.get('open'):
                res.update({'trend': '1'})
            elif res.get('close') < res.get('open'):
                res.update({'trend': '-1'}) 
        elif init_data == True:
            res = {
                'volume': 0,
                'open': 0,
                'close': 0,
                'high': 0,
                'low': 0,
                'trend': '0'
            }
        return res
    
    def get_info_ngay(self, cr, uid, from_date, from_date_time=None, arg="close", init_data=False, context=None):
        res = {'close': None, 'last': None}
        if arg in ['close', 'all']:
            res['close'] = self.get_info_from_range(cr, uid, from_date, from_date, init_data, context)
            if arg != 'all':
                return res['close']
        elif arg in ['last', 'all']:
            domain = [('ngay_tao', '=', from_date)]
            if from_date_time:
                domain = [('ngay_gio_tao', '<=', from_date_time)]
            truc_gia_ids = self.pool.get('snc.truc.gia.lme').search(cr, uid, domain,
                                                                    limit=1, order="ngay_gio_tao desc")
            if truc_gia_ids:
                res['last'] = self.pool.get('snc.truc.gia.lme').read(cr, uid, truc_gia_ids[0], 
                                                                     ['last', 'volume',
                                                                      'open', 'high', 'low'])
            elif init_data == True:
                res['last'] = {'last': 0,
                               'volume': 0,
                               'open': 0,
                               'high': 0,
                               'low': 0}
            if arg != 'all':
                return res['last']
        return res
    
    def get_info_tuan(self, cr, uid, from_date, init_data=False, context=None):
        res = None
        from_date = self.pool.get('vieterp.utils').get_this_monday(cr, uid, from_date)
        to_date = self.pool.get('vieterp.utils').get_this_friday(cr, uid, from_date)
        res = self.get_info_from_range(cr, uid, from_date, to_date, init_data, context)
        return res
    
    def get_info_thang(self, cr, uid, from_date, init_data=False, context=None):
        res = None
        from_date = self.pool.get('vieterp.utils').get_this_month(cr, uid, from_date)
        to_date = datetime.datetime.strptime(from_date, DEFAULT_SERVER_DATE_FORMAT)
        to_date = self.pool.get('vieterp.utils').get_this_month(cr, uid, to_date + datetime.timedelta(35))
        to_date -= datetime.timedelta(1)
        to_date = to_date.strftime(DEFAULT_SERVER_DATE_FORMAT)
        res = self.get_info_from_range(cr, uid, from_date, to_date, init_data, context)
        return res  
    
snc_lme()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

