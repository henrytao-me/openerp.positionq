# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode
import types

class pq_bo_phan(osv.osv):
    
    _name = 'pq.bo.phan'
    _description = 'Bo phan'
    _columns = {
        'name': fields.char('Tên Bộ phận', size=128, required=True),
        'vi_tri': fields.one2many('pq.vi.tri', 'bo_phan', string="Vị trí"),
        
        'create_date': fields.datetime('Ngày giờ tạo', readonly=True),
        'user_id': fields.many2one('res.users', string="Người tạo",readonly=True),
    }
    _defaults = {
        'user_id': lambda self, cr, uid, context=None: uid,
    }

    def create(self, cr, uid, vals, context=None):
        self.pool.get('pq.redis').clear_all(cr, uid)
        return super(pq_bo_phan, self).create(cr, uid, vals, context)

    def write(self, cr, uid, ids, vals, context=None):
        self.pool.get('pq.redis').clear_all(cr, uid)
        return super(pq_bo_phan, self).write(cr, uid, ids, vals, context)

    def unlink(self, cr, uid, ids, context=None):
        self.pool.get('pq.redis').clear_all(cr, uid)
        return super(pq_bo_phan, self).unlink(cr, uid, ids, context)
    
pq_bo_phan()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

