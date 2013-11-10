# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode
import types

class pq_yeu_to(osv.osv):
    
    _name = 'pq.yeu.to'
    _description = 'Yeu To'
    _columns = {
        'name': fields.char('Tên yếu tố', size=128, required=True),
        'tieu_chi': fields.one2many('pq.tieu.chi', 'yeu_to', string='Tiêu chí'),
        
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
        self.pool.get('pq.redis').clear_all(cr, uid)
        
        res = super(pq_yeu_to, self).create(cr, uid, vals, context)
        self.pool.get('pq.nhom.vi.tri.yeu.to').auto_sync(cr, uid, yeu_to_id=res)
        self.pool.get('pq.vi.tri.yeu.to').auto_sync(cr, uid, yeu_to_id=res)     
        return res

    def write(self, cr, uid, ids, vals, context=None):
        self.pool.get('pq.redis').clear_all(cr, uid)
        return super(pq_yeu_to, self).write(cr, uid, ids, vals, context)

    def unlink(self, cr, uid, ids, context=None):
        self.pool.get('pq.redis').clear_all(cr, uid)
        return super(pq_yeu_to, self).unlink(cr, uid, ids, context)
    
pq_yeu_to()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

