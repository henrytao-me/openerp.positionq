# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode
import types

class pq_bac(osv.osv):
    
    _name = 'pq.bac'
    _description = 'Bac'
    _columns = {
        'name': fields.char('Tên Bậc', size=128, required=True),
        
        'create_date': fields.datetime('Ngày giờ tạo', readonly=True),
        'user_id': fields.many2one('res.users', string="Người tạo",readonly=True),
    }
    _defaults = {
        'user_id': lambda self, cr, uid, context=None: uid,
    }

    def create(self, cr, uid, vals, context=None):
        self.pool.get('pq.redis').clear_all(cr, uid)
        return super(pq_bac, self).create(cr, uid, vals, context)

    def write(self, cr, uid, ids, vals, context=None):
        self.pool.get('pq.redis').clear_all(cr, uid)
        return super(pq_bac, self).write(cr, uid, ids, vals, context)

    def unlink(self, cr, uid, ids, context=None):
        self.pool.get('pq.redis').clear_all(cr, uid)
        return super(pq_bac, self).unlink(cr, uid, ids, context)
    
pq_bac()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

