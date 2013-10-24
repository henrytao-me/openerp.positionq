# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode
import math 

class snc_nhan_dinh_tuan_trong_so(osv.osv_memory):
    
    _name = 'snc.nhan.dinh.tuan.trong.so'
    _description = 'Trong So Nhan Dinh Tuan'
    _columns = {
        'name': fields.char('Tiêu đề', size=8),        
    }
    _defaults = {
        'name': lambda *x: ' ',
    }
    
    def trong_so(self, cr, uid, args=None, context=None):
        if not context:
            context = {}
        res = {
            'tsxh': self.trong_so_xu_huong(cr, uid, args, context),
            'tsbd': self.trong_so_bien_do(cr, uid, args, context),
            'ts': self.trong_so_tuan(cr, uid, args, context)
        }
        return res
        
    def trong_so_xu_huong(self, cr, uid, args=None, context=None):
        if not context:
            context = {}
        res = {}
        #get setup info
        info = self.pool.get('snc.nhan.dinh.tuan.setup').get_info(cr, uid, ['cal_from', 
                                                                            'cal_to', 
                                                                            'dcxh'])
        users = self.pool.get('snc.nhan.dinh.tuan.setup').get_users(cr, uid)
        if not info:
            return res
        thong_ke = self.pool.get('snc.nhan.dinh.tuan.thong.ke').thong_ke(cr, uid, context={
                                                                        'from_date': info['cal_from'],
                                                                        'to_date': info['cal_to'],
                                                                        'thong_ke_chi_tiet': False
                                                                    })
        #data
        data = {}
        n = len(thong_ke['thong_ke'])
        for u in users:
            data.update({u['id']: {
                'name': u['name'],
                'ssxh': 0,
                'n': 0,
                'tsxh': 0
            }})
            for tk in thong_ke['thong_ke']:
                if tk['data'].get(u['id']):
                    data[u['id']].update({
                        'ssxh': data[u['id']].get('ssxh', 0) + tk['data'].get(u['id'], {}).get('diff_trend', 0),
                        'n': data[u['id']].get('n', 0) + 1
                    })
            #finalize
            if data[u['id']].get('n', 0) == 0:
                data[u['id']].update({'ssxh': info.get('dcxh', 0)})
            else:
                data[u['id']].update({'ssxh': data[u['id']].get('ssxh', 0) * n / data[u['id']].get('n')})
        #calculate k and percent ssxh
        k = 0
        for u in data.copy():
            if data[u].get('ssxh', 0) >= info.get('dcxh', 0):
                data[u].update({'k': 0})
            else:
                data[u].update({'k': info.get('dcxh', 0) - data[u].get('ssxh', 0)})
            k += data[u].get('k', 0)
        #calculate tsxh
        for u in data.copy():
            if k == 0:
                data[u].update({'tsxh': 1.0 / len(data.keys())})
            else:
                data[u].update({'tsxh': data[u].get('k', 0) / k})
        #
        res = {
            'k': k,
            'info': info,
            'data': data
        }
        return res
    
    def trong_so_bien_do(self, cr, uid, args=None, context=None):
        if not context:
            context = {}
        res = {}
        #get setup info
        info = self.pool.get('snc.nhan.dinh.tuan.setup').get_info(cr, uid, ['cal_from', 
                                                                            'cal_to', 
                                                                            'dcbd'])
        users = self.pool.get('snc.nhan.dinh.tuan.setup').get_users(cr, uid)
        if not info:
            return res
        thong_ke = self.pool.get('snc.nhan.dinh.tuan.thong.ke').thong_ke(cr, uid, context={
                                                                        'from_date': info['cal_from'],
                                                                        'to_date': info['cal_to'],
                                                                        'thong_ke_chi_tiet': False
                                                                    })
        #data
        data = {}
        n = len(thong_ke['thong_ke'])
        for u in users:
            data.update({u['id']: {
                'name': u['name'],
                'ssbd': 0,
                'n': 0,
                'tsbd': 0
            }})
            for tk in thong_ke['thong_ke']:
                if tk['data'].get(u['id']):
                    data[u['id']].update({
                        'ssbd': data[u['id']].get('ssbd', 0) + tk['data'].get(u['id'], {}).get('diff_abs', 0),
                        'n': data[u['id']].get('n', 0) + 1
                    })
            #finalize
            if data[u['id']].get('n', 0) == 0:
                data[u['id']].update({'ssbd': info.get('dcbd', 0)})
            else:
                data[u['id']].update({'ssbd': data[u['id']].get('ssbd', 0) * n / data[u['id']].get('n')})
        #calculate k and percent ssbd
        k = 0
        for u in data.copy():
            if data[u].get('ssbd', 0) >= info.get('dcbd', 0):
                data[u].update({'k': 0})
            else:
                data[u].update({'k': info.get('dcbd', 0) - data[u].get('ssbd', 0)})
            k += data[u].get('k', 0)
        #calculate tsbd
        for u in data.copy():
            if k == 0:
                data[u].update({'tsbd': 1.0 / len(data.keys())})
            else:
                data[u].update({'tsbd': data[u].get('k', 0) / k})
        #
        res = {
            'k': k,
            'info': info,
            'data': data
        }
        return res
    
    def trong_so_tuan(self, cr, uid, args=None, context=None):
        if not context:
            context = {}
        res = {}
        info = self.pool.get('snc.nhan.dinh.tuan.setup').get_info(cr, uid, ['percent_xh', 'percent_bd'])
        tsxh = self.trong_so_xu_huong(cr, uid, args, context)
        tsbd = self.trong_so_bien_do(cr, uid, args, context)
        res = {}
        for u in tsxh['data']:
            res.update({
                u: {
                    'name': tsxh['data'][u].get('name', '-'),
                    'tsxh': tsxh['data'][u].get('tsxh', 0),
                    'tsbd': tsbd['data'][u].get('tsbd', 0),
                }
            })
            res[u].update({
                'ts': (res[u].get('tsxh') * info.get('percent_xh') + res[u].get('tsbd') * info.get('percent_bd')) / (info.get('percent_xh') + info.get('percent_bd')) 
            })
        return res
    
snc_nhan_dinh_tuan_trong_so()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

