# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode
import math 

class snc_nhan_dinh_ngay_thong_ke(osv.osv_memory):
    
    _name = 'snc.nhan.dinh.ngay.thong.ke'
    _description = 'Report'
    _columns = {
        'name': fields.char('Tiêu đề', size=8),
        'from_date': fields.date('Từ ngày'),
        'to_date': fields.date('Đến ngày'),
    }
    _defaults = {
        'name': lambda *x: ' ',
    }
    
    def get_this_monday(self, cr, uid, date):
        res = date
        not_datetime = False
        if not isinstance(date, datetime.datetime):
            not_datetime = True
            date = datetime.datetime.strptime(date, DEFAULT_SERVER_DATE_FORMAT)
        timedelta = datetime.timedelta((int(date.strftime('%w')) - 1 + 7) % 7)
        date = date - timedelta
        if not_datetime:
            date = date.strftime(DEFAULT_SERVER_DATE_FORMAT)
        res = date
        return res
    
    def get_this_friday(self, cr, uid, date):
        res = date
        not_datetime = False
        if not isinstance(date, datetime.datetime):
            not_datetime = True
            date = datetime.datetime.strptime(date, DEFAULT_SERVER_DATE_FORMAT)
        timedelta = datetime.timedelta((int(date.strftime('%w')) - 1 + 7) % 7)
        date = date - timedelta
        timedelta = datetime.timedelta(4)
        date = date + timedelta
        if not_datetime:
            date = date.strftime(DEFAULT_SERVER_DATE_FORMAT)
        res = date
        return res
    
    def search_range(self, cr, uid, args={}, context={}):
        if not context:
            context = {}
        now = datetime.datetime.now().strftime(DEFAULT_SERVER_DATE_FORMAT)
        now = datetime.datetime.strptime(now, DEFAULT_SERVER_DATE_FORMAT)  
        #
        from_date = context.get('from_date', now)
        if not isinstance(from_date, datetime.datetime):
            from_date = datetime.datetime.strptime(from_date, DEFAULT_SERVER_DATE_FORMAT)
        to_date= context.get('to_date', now)
        if not isinstance(to_date, datetime.datetime):
            to_date = datetime.datetime.strptime(to_date, DEFAULT_SERVER_DATE_FORMAT)
        #
        timedelta = datetime.timedelta((int(from_date.strftime('%w')) - 1 + 7) % 7)
        from_date = from_date - timedelta
        #
        timedelta = datetime.timedelta((int(to_date.strftime('%w')) - 1 + 7) % 7)
        to_date = to_date - timedelta
        timedelta = datetime.timedelta(4)
        to_date = to_date + timedelta
        #
        return from_date, to_date
    
    def get_users_from_range(self, cr, uid, from_date, to_date):
        res = {}
        if isinstance(from_date, datetime.datetime):
            from_date = from_date.strftime(DEFAULT_SERVER_DATE_FORMAT)
        if isinstance(to_date, datetime.datetime):
            to_date = to_date.strftime(DEFAULT_SERVER_DATE_FORMAT)
        ids = self.pool.get('snc.nhan.dinh.ngay').search(cr, uid, [('time_format', '>=', from_date),
                                                              ('time_format', '<=', to_date)],
                                                    order="create_date desc")
        if ids:
            res = {}
            for obj in self.pool.get('snc.nhan.dinh.ngay').read(cr, uid, ids, ['user_id']):
                res.update({
                    obj['user_id'][0]: obj['user_id']
                })
            res = res.values()
            res.sort(key=lambda tup: tup[1])
        return res
    
    def get_info_real(self, cr, uid, date):
        res = None
        if isinstance(date, datetime.datetime):
            date = date.strftime(DEFAULT_SERVER_DATE_FORMAT)
        ids = self.pool.get('snc.truc.gia.lme').search(cr, uid, [('ngay_tao', '=', date)], 
                                                       order='ngay_gio_tao desc', limit=1)
        if ids:
            tmp = self.pool.get('snc.truc.gia.lme').read(cr, uid, ids[0], ['fn_high', 
                                                                           'fn_low', 
                                                                           'fn_open',
                                                                           'fn_close',
                                                                           'fn_trend'])
            if tmp.get('fn_close', 0) > 0:                
                res = {
                    'high': tmp.get('fn_high'),
                    'low': tmp.get('fn_low'),
                    'trend': tmp.get('fn_trend'),
                }
        return res
    
    def get_info_by_user(self, cr, uid, date, user_id):
        res = None
        if isinstance(date, datetime.datetime):
            date = date.strftime(DEFAULT_SERVER_DATE_FORMAT)
        fields = ['high', 'low', 'trend',
                  'diff_high_abs', 'diff_high_percent',
                  'diff_low_abs', 'diff_low_percent', 
                  'diff_trend']
        ids = self.pool.get('snc.nhan.dinh.ngay').search(cr, uid, [('time_format', '=', date),
                                                                   ('user_id', '=', user_id)],
                                                    order='create_date desc', limit=1)
        if ids:
            res = self.pool.get('snc.nhan.dinh.ngay').read(cr, uid, ids[0], fields)                                
        return res
    
    def thong_ke_list(self, cr, uid, args={}, context={}):
        res = []
        from_date, to_date = self.search_range(cr, uid, args, context=context)
        res = self.get_users_from_range(cr, uid, from_date, to_date)
        return res
    
    def thong_ke_rows(self, cr, uid, args={}, context={}):
        res = []
        from_date, to_date = self.search_range(cr, uid, args, context)        
        #get list user
        list_user = self.thong_ke_chi_tiet_list(cr, uid, args, context)
        #render data
        delta = datetime.timedelta(1)
        delta_4 = datetime.timedelta(4)
        delta_7 = datetime.timedelta(7)
        i = from_date
        n = to_date
        while True:
            if i > n:
                break            
            row = {
                'date': i.strftime(DEFAULT_SERVER_DATE_FORMAT),                
                'user': {}
            }
            #
            user_data = {}
            for d in self.thong_ke_chi_tiet_rows(cr, uid, args, context={'from_date': i, 'to_date': i+delta_4}):
                u = d.get('user', {})
                for ui in u:
                    if not user_data.get(ui):
                        user_data.update({ui: {'diff_abs': 0, 'diff_percent': 0, 'diff_trend': 0, 'trend_count': 0}})
                    user_data[ui]['diff_abs'] += (u[ui].get('diff_high_abs', 0) + u[ui].get('diff_low_abs', 0)) / 2
                    user_data[ui]['diff_percent'] += (u[ui].get('diff_high_percent', 0) + u[ui].get('diff_low_percent', 0)) / 2
                    if u[ui]:
                        user_data[ui]['trend_count'] += 1 
                    user_data[ui]['diff_trend'] += u[ui].get('diff_trend', 0)
            for ui in user_data:
                user_data[ui].update({
                    'avg_diff_abs': user_data[ui].get('diff_abs') / 5,
                    'avg_diff_percent': user_data[ui].get('diff_percent') / 5,
                    'avg_diff_trend': 5,                    
                })
                if user_data[uid].get('trend_count', 0) > 0:
                    user_data[ui]['avg_diff_trend'] = user_data[ui].get('diff_trend') * 5 / user_data[ui].get('trend_count')
            #append user_data
            row['user'] = user_data
            #append rows
            res.append(row)
            #next
            i += delta_7
        return res
    
    def thong_ke_chi_tiet_list(self, cr, uid, args={}, context={}):
        res = []
        from_date, to_date = self.search_range(cr, uid, args, context=context)
        res = self.get_users_from_range(cr, uid, from_date, to_date)
        return res
    
    def thong_ke_chi_tiet_rows(self, cr, uid, args={}, context={}):        
        res = []
        from_date, to_date = self.search_range(cr, uid, args, context)
        #get list user
        list_user = self.thong_ke_chi_tiet_list(cr, uid, args, context)
        #render data
        delta = datetime.timedelta(1)
        i = from_date
        n = to_date
        while True:                        
            if i > n:
                break
            if i > self.get_this_friday(cr, uid, i):
                i += delta
                continue
            row = {
                'date': i.strftime(DEFAULT_SERVER_DATE_FORMAT),
                'real': self.get_info_real(cr, uid, i) or {},
                'user': {}
            }
            #get nhan_dinh from user
            for user in list_user:
                row['user'][user[0]] = self.get_info_by_user(cr, uid, i, user[0]) or {}
            #append
            res.append(row)
            #next
            i += delta
        return res
    
    def thong_ke_all(self, cr, uid, args={}, context={}):
        res = {'a': 'a data', 'b': 'b data'}
        return res
    
snc_nhan_dinh_ngay_thong_ke()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

