# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode
import types

class pq_nhom_vi_tri(osv.osv):
    
    def func_custom(self, cr, uid, ids, fields, args, context=None):
        res = {}
        for id in ids:
            res[id] = {'pq_salary_w1': id,
                       'pq_salary_w2': id,
                       'pq_salary_w3': id}
        return res;

    def func_diem(self, cr, uid, ids, fields, args, context=None):
        res = {}
        for obj in self.read(cr, uid, ids, ['vi_tri']):
            val_min = 0
            val_max = 0
            for tobj in self.pool.get('pq.vi.tri').read(cr, uid, obj['vi_tri'], ['diem']):
                if val_min > tobj['diem'] or val_min == 0:
                    val_min = tobj['diem']
                if val_max < tobj['diem']:
                    val_max = tobj['diem']
            res[obj['id']] = {
                'diem_cao_nhat': val_max,
                'diem_thap_nhat': val_min
            }
        return res
    
    _name = 'pq.nhom.vi.tri'
    _description = 'Nhom Vi Tri'
    _columns = {
        'name': fields.char('Tên nhóm', size=128, required=True),
        'vi_tri': fields.one2many('pq.vi.tri', 'nhom_vi_tri', string="Vị trí"),
        'yeu_to': fields.one2many('pq.nhom.vi.tri.yeu.to', 'nhom_vi_tri', string="Yếu tố"),

        'diem_cao_nhat': fields.function(func_diem, method=True, type="float", digits=(16,2), string="Điểm cao nhất", multi=True),
        'diem_thap_nhat': fields.function(func_diem, method=True, type="float", digits=(16,2), string="Điểm thấp nhất", multi=True),
        
        'pq_salary_w1': fields.function(func_custom, string='pq_salary_w1', type='integer', multi=True, store=True),
        'pq_salary_w2': fields.function(func_custom, string='pq_salary_w2', type='integer', multi=True, store=True),
        'pq_salary_w3': fields.function(func_custom, string='pq_salary_w3', type='integer', multi=True, store=True),
        
        'nhom_luong': fields.one2many('pq.nhom.luong', 'nhom_vi_tri', string="Nhóm lương"),
        
        'create_date': fields.datetime('Ngày giờ tạo', readonly=True),
        'user_id': fields.many2one('res.users', string="Người tạo", readonly=True),
    }
    _defaults = {
        'user_id': lambda self, cr, uid, context = None: uid,
    }
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'name is unique'),
    ]
    
    def create(self, cr, uid, vals, context=None):
        res = super(pq_nhom_vi_tri, self).create(cr, uid, vals, context)
        self.pool.get('pq.nhom.vi.tri.yeu.to').auto_sync(cr, uid, nhom_vi_tri_id=res)     
        return res
    
pq_nhom_vi_tri()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

