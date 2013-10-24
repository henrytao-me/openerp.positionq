# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode
import types

class pq_tcc2(osv.osv):
    
    _name = 'pq.tcc2'
    _description = 'Tieu Chi Cap 2'
    _columns = {
        'name': fields.char('Tên tiêu chí', size=128, required=True),
        'tcc1': fields.many2one('pq.tcc1', string="Tiêu chí cấp 1", required=True, ondelete="cascade"),
        
        'trong_so': fields.float('Trọng số', digits=(16,2)),
        
        'create_date': fields.datetime('Ngày giờ tạo', readonly=True),
        'user_id': fields.many2one('res.users', string="Người tạo",readonly=True),
    }
    _defaults = {
        'trong_so': lambda *x: 0,
        'user_id': lambda self, cr, uid, context=None: uid,
    }
    
pq_tcc2()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

