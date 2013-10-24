# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode
import math 

class snc_nhan_dinh_tuan_thong_ke(osv.osv_memory):
    
    _name = 'snc.nhan.dinh.tuan.thong.ke'
    _description = 'Thong Ke Nhan Dinh Tuan'
    _columns = {
        'name': fields.char('Tiêu đề', size=8),
        'from_date': fields.date('Từ ngày'),
        'to_date': fields.date('Đến ngày'),
    }
    _defaults = {
        'name': lambda *x: ' ',
    }

    def search_range(self, cr, uid, args=None, context=None):
        if not context:
            context = {}
        
        now = datetime.datetime.now().strftime(DEFAULT_SERVER_DATE_FORMAT)
        now = datetime.datetime.strptime(now, DEFAULT_SERVER_DATE_FORMAT)  
        #
        from_date = context.get('from_date', now - datetime.timedelta(28))   
        to_date= context.get('to_date', now)
        #
        from_date = self.pool.get('vieterp.utils').get_this_monday(cr, uid, from_date)
        to_date = self.pool.get('vieterp.utils').get_this_friday(cr, uid, to_date)
        #
        if not isinstance(from_date, datetime.datetime):
            from_date = datetime.datetime.strptime(from_date, DEFAULT_SERVER_DATE_FORMAT)
        if not isinstance(to_date, datetime.datetime):
            to_date = datetime.datetime.strptime(to_date, DEFAULT_SERVER_DATE_FORMAT)
        #
        return from_date, to_date
    
    
    def thong_ke(self, cr, uid, args=None, context=None):
        if not context:
            context = {}
        
        res = {}
        from_date, to_date = self.search_range(cr, uid, args=args, context=context)
        #get users
        users = self.pool.get('snc.nhan.dinh.tuan').get_users_from_range(cr, uid,
                            datetime.datetime.strftime(from_date, DEFAULT_SERVER_DATE_FORMAT),
                            datetime.datetime.strftime(to_date, DEFAULT_SERVER_DATE_FORMAT))
        #get thong_ke
        thong_ke = []
        i = from_date        
        while i < to_date:
            str_i = datetime.datetime.strftime(i, DEFAULT_SERVER_DATE_FORMAT)
            thong_ke.append({
                'time': str_i,
                'data': self.pool.get('snc.nhan.dinh.tuan').thong_ke(cr, uid, str_i)
            })
            i += datetime.timedelta(7)
        #get chi_tiet
        thong_ke_chi_tiet = []
        if context.get('thong_ke_chi_tiet', True):            
            i = from_date
            while i <= to_date:
                str_i = datetime.datetime.strftime(i, DEFAULT_SERVER_DATE_FORMAT)
                thong_ke_chi_tiet.append({
                    'time': str_i,
                    'real': self.pool.get('snc.truc.gia.lme').get_info(cr, uid, str_i, type="tuan"),
                    'data': self.pool.get('snc.nhan.dinh.tuan').thong_ke_chi_tiet(cr, uid, str_i)
                })
                i += datetime.timedelta(7)
        #sort
        thong_ke = sorted(thong_ke, key=lambda k: k['time'], reverse=True)
        thong_ke_chi_tiet = sorted(thong_ke_chi_tiet, key=lambda k: k['time'], reverse=True)
        #return
        res = {
            'users': users,
            'thong_ke': thong_ke,
            'thong_ke_chi_tiet': thong_ke_chi_tiet
        }
        return res
    
snc_nhan_dinh_tuan_thong_ke()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

