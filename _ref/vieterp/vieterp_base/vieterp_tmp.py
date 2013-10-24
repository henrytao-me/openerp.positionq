# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.osv.fields import datetime as datetime_field
from openerp.tools.translate import _
import logging
import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from unidecode import unidecode

class vieterp_tmp(osv.osv):
    ###################################################################
    def function_create_date_format(self, cr, uid, ids, fields, args, context=None):
        if not context:
            context = {}    
        res = {}        
        for obj in self.browse(cr, uid, ids, context=context):            
            tmp_UTC = datetime.datetime.strptime(obj.create_date, DEFAULT_SERVER_DATETIME_FORMAT)
            tmp_in_user_timezone = datetime_field.context_timestamp(cr, uid, tmp_UTC, context=context)
            res[obj.id] = tmp_in_user_timezone.strftime('%H:%M:%S %d/%m/%Y')
        return res
    ###################################################################
    ###################################################################
    ###################################################################
    _name = 'vieterp.tmp'
    _description = 'Module tạm'
    _columns = {
        'name': fields.char('Tiêu đề', size=128, required=True),        
        'create_date': fields.datetime('Ngày giờ tạo', readonly=True),
        'create_date_format': fields.function(function_create_date_format, method=True, string='Ngày giờ tạo',
                                              type='char', size=1024),        
    }
    _defaults = {
    }
    ###################################################################
    ###################################################################
    ###################################################################    
vieterp_tmp()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

