# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode
import types

class pq_tcc1(osv.osv):
    
    def func_trong_so(self, cr, uid, ids, fields, args, context=None):
        res = {}
        for obj in self.read(cr, uid, ids, ['method', 'tcc2']):
            value = 0
            for tobj in self.pool.get('pq.tcc2').read(cr, uid, obj['tcc2'], ['trong_so']):
                if obj['method'] == 10: # tong
                    value += tobj['trong_so']
                elif obj['method'] == 20: # lon nhat
                    if value < tobj['trong_so']:
                        value = tobj['trong_so']
            res[obj['id']] = value
        return res
    
    _name = 'pq.tcc1'
    _description = 'Tieu Chi Cap 1'
    _columns = {
        'name': fields.char('Tên tiêu chí', size=128, required=True),
        'tieu_chi': fields.many2one('pq.tieu.chi', string="Tiêu chí", required=True, ondelete="cascade"),
        'tcc2': fields.one2many('pq.tcc2', 'tcc1', string="Tiêu chí cấp 2"),
        
        'method': fields.selection([(10, 'Tổng'), (20, 'Lớn nhất')], 'Phương pháp'),
        
        'trong_so': fields.function(func_trong_so, method=True, string="Trọng số", type="float", digits=(16,2)),
        
        'create_date': fields.datetime('Ngày giờ tạo', readonly=True),
        'user_id': fields.many2one('res.users', string="Người tạo",readonly=True),
    }
    _defaults = {
        'method': lambda *x: 10,
        'user_id': lambda self, cr, uid, context=None: uid,
    }

    def create(self, cr, uid, vals, context=None):
        self.pool.get('pq.redis').clear_all(cr, uid)
        return super(pq_tcc1, self).create(cr, uid, vals, context)

    def write(self, cr, uid, ids, vals, context=None):
        self.pool.get('pq.redis').clear_all(cr, uid)
        return super(pq_tcc1, self).write(cr, uid, ids, vals, context)

    def unlink(self, cr, uid, ids, context=None):
        self.pool.get('pq.redis').clear_all(cr, uid)
        return super(pq_tcc1, self).unlink(cr, uid, ids, context)
    
pq_tcc1()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

