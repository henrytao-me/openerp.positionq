# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from openerp.osv.fields import datetime as datetime_field
import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT

class snc_nhan_dinh_ngay_exception(osv.osv):
    
    _name = 'snc.nhan.dinh.ngay.exception'
    _description = 'Cac Ngay Khong Nhan Dinh'
    _columns = {
        'name': fields.many2one('snc.nhan.dinh.ngay.setup', string='Thiết lập'),
        
        'date': fields.date('Ngày'),
        'reason': fields.char('Lý do', size=1000),
        
        'user_id': fields.many2one('res.users', string="Create user", readonly=True),
        'create_date': fields.datetime('Create date', readonly=True),
    }
    _defaults = {
        'user_id': lambda self, cr, uid, context=None: uid,
    }
    _order = 'date desc'
    
snc_nhan_dinh_ngay_exception()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

