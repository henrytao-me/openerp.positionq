# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode
import types

class pq_tieu_chi(osv.osv):
    
    def func_trong_so(self, cr, uid, ids, fields, args, context=None):
        res = {}
        for obj in self.read(cr, uid, ids, ['method', 'tcc1']):
            value = 0
            if obj['method'] == 10:  # diem chuan
                for tcc1 in self.pool.get('pq.tcc1').read(cr, uid, obj['tcc1'], ['trong_so']):
                    value += tcc1['trong_so']
            elif obj['method'] == 20: # thuc te
                for tcc1 in self.pool.get('pq.tcc1').read(cr, uid, obj['tcc1'], ['trong_so']):
                    value += tcc1['trong_so']
            res[obj['id']] = value
        return res
    
    _name = 'pq.tieu.chi'
    _description = 'Tieu Chi'
    _columns = {
        'name': fields.char('Tên tiêu chí', size=128, required=True),
        'yeu_to': fields.many2one('pq.yeu.to', string="Yếu tố", required=True, ondelete="cascade"),
        'tcc1': fields.one2many('pq.tcc1', 'tieu_chi', string="Tiêu chí cấp 1"),
        
        'method': fields.selection([(10, 'Điểm chuẩn'), (20, 'Điểm thực tế')], 'Phương pháp'),
        
        'trong_so': fields.function(func_trong_so, method=True, string="Trọng số", type="float", digits=(16,2)),
        
        'create_date': fields.datetime('Ngày giờ tạo', readonly=True),
        'user_id': fields.many2one('res.users', string="Người tạo",readonly=True),
    }
    _defaults = {
        'method': lambda *x: 10,
        'user_id': lambda self, cr, uid, context=None: uid,
    }
    
pq_tieu_chi()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

