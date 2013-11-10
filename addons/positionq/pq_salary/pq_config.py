# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode
import types

class pq_config(osv.osv):
    
    _name = 'pq.config'
    _description = 'Thiet lap'
    _columns = {
        'name': fields.char('Thiết lập', size=128),
                
        'so_bac': fields.integer('Số bậc'), 
        'bac_min': fields.float('Giá trị thấp nhất', digits=(16,2)),
        'bac_max': fields.float('Giá trị cao nhất', digits=(16,2)),
        
        'enable': fields.boolean('Kích hoạt'),
        
        'create_date': fields.datetime('Ngày giờ tạo', readonly=True),
        'user_id': fields.many2one('res.users', string="Người tạo", readonly=True),
    }
    _defaults = {
        'so_bac': lambda *x: 5,
        'bac_min': lambda *x: 100,
        'bac_max': lambda *x: 1000,
        
        'enable': lambda *x: True,
        
        'user_id': lambda self, cr, uid, context = None: uid,
    }
    _sql_constraints = [
        
    ]

    def create(self, cr, uid, vals, context=None):
        self.pool.get('pq.redis').clear_all(cr, uid)
        return super(pq_config, self).create(cr, uid, vals, context)

    def write(self, cr, uid, ids, vals, context=None):
        self.pool.get('pq.redis').clear_all(cr, uid)
        return super(pq_config, self).write(cr, uid, ids, vals, context)

    def unlink(self, cr, uid, ids, context=None):
        self.pool.get('pq.redis').clear_all(cr, uid)
        return super(pq_config, self).unlink(cr, uid, ids, context)
    
    def get_info(self, cr, uid):
        res = {}
        ids = self.search(cr, uid, [('enable', '=', True)])
        if ids:
            res = self.read(cr, uid, ids[0], ['so_bac', 'bac_max', 'bac_min'])
        if not res:
            res = {'so_bac': 5,
                   'bac_min': 100,
                   'bac_max': 1000}
        return res
    
pq_config()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

