# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from openerp.osv.fields import datetime as datetime_field
import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT

class snc_nhan_dinh_tuan_exception(osv.osv):
    
    def function_date(self, cr, uid, ids, fields, args, context=None):
        res = {}
        for obj in self.read(cr, uid, ids, ['date']):
            res[obj['id']] = self.pool.get('vieterp.utils').get_this_monday(cr, uid, obj['date'])
        return res
    
    _name = 'snc.nhan.dinh.tuan.exception'
    _description = 'Cac Ngay Khong Nhan Dinh'
    _columns = {
        'name': fields.many2one('snc.nhan.dinh.tuan.setup', string='Thiết lập'),

        'date_org': fields.date('Tuần'),
        'date': fields.function(function_date, method=True, type="date", string="Tuần",
            store={
                'snc.nhan.dinh.tuan.exception': (lambda self, cr, uid, ids, *args: ids, ['date_org'], 10), 
            }),
        
        'reason': fields.char('Lý do', size=1000),
        
        'user_id': fields.many2one('res.users', string="Create user", readonly=True),
        'create_date': fields.datetime('Create date', readonly=True),
    }
    _defaults = {
        'user_id': lambda self, cr, uid, context=None: uid,
    }
    _order = 'date desc'
    
snc_nhan_dinh_tuan_exception()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

