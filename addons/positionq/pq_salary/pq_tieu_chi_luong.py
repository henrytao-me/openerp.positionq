# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode
import types

class pq_tieu_chi_luong(osv.osv):
    
    _name = 'pq.tieu.chi.luong'
    _description = 'Tieu Chi Luong'
    _columns = {
        'name': fields.char('Tên', size=128),
        
        'chenh_lech': fields.float('Chênh lệch', digits=(16,2), required=True),
        'muc_chenh_lech': fields.char('So với', size=128),
        
        'ty_le': fields.float('Tỷ lệ', digits=(16,2)),
        'muc_ty_le': fields.char('Của'),
        
        'create_date': fields.datetime('Ngày giờ tạo', readonly=True),
        'user_id': fields.many2one('res.users', string="Người tạo", readonly=True),
    }
    _defaults = {
        'chenh_lech': lambda *x: 0,
        'muc_chenh_lech': lambda *x: 'm1',
        'ty_le': lambda *x: 1,
        'muc_ty_le': lambda *x: 'm1',
        'user_id': lambda self, cr, uid, context = None: uid,
    }
    _sql_constraints = [
        
    ]
    
pq_tieu_chi_luong()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

