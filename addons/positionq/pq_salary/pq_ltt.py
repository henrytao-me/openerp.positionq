# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode
import types

class pq_ltt(osv.osv):
    
    _name = 'pq.ltt'
    _description = 'Luong Thi Truong'
    _columns = {
        'name': fields.char('Tên nhóm', size=128),
        'ltt_vi_tri': fields.many2one('pq.ltt.vi.tri', string="Vị trí công việc", ondelete="cascade"),
        'ltt_muc_do': fields.many2one('pq.ltt.muc.do', string="Mức độ", ondelete="cascade"),
        
        'luong': fields.float('Lương', digits=(16,2)),
        
        'create_date': fields.datetime('Ngày giờ tạo', readonly=True),
        'user_id': fields.many2one('res.users', string="Người tạo", readonly=True),
    }
    _defaults = {
        'user_id': lambda self, cr, uid, context = None: uid,
    }
    _sql_constraints = [
        
    ]
    
pq_ltt()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

