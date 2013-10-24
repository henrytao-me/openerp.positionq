# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode
import types

class pq_ltt_muc_do(osv.osv):
    
    _name = 'pq.ltt.muc.do'
    _description = 'Luong Thi Truong - Muc Do'
    _columns = {
        'name': fields.char('Tên mức độ', size=128),
        
        'create_date': fields.datetime('Ngày giờ tạo', readonly=True),
        'user_id': fields.many2one('res.users', string="Người tạo", readonly=True),
    }
    _defaults = {
        'user_id': lambda self, cr, uid, context = None: uid,
    }
    _sql_constraints = [
        
    ]
    
pq_ltt_muc_do()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

