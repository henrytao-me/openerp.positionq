# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.osv.fields import datetime as datetime_field
from openerp.tools.translate import _
import logging
import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from unidecode import unidecode

class snc_article_fix(osv.osv):
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
    
    def function_alias(self, cr, uid, ids, fields, args, context=None):
        if not context:
            context = {}
        res = {}
        for obj in self.browse(cr, uid, ids, context=context):
            #res[obj.id] = unidecode.unidecode(obj.name)
            res[obj.id] = unidecode(obj.name).replace(' ', '-').lower()
        return res
    ###################################################################
    ###################################################################
    ###################################################################
    _name = 'snc.article.fix'
    _description = 'Bai Viet Co Dinh'
    _columns = {
        'name': fields.char('Tiêu đề', size=128, required=True),
        #'alias': fields.char('alias', size=128, required=True),
        'alias': fields.function(function_alias, method=True, string='Alias', type='char', size=512, store=True),
        'content': fields.html('Nội dung'),
        'create_date': fields.datetime('Ngày giờ tạo', readonly=True),
        'create_date_format': fields.function(function_create_date_format, method=True, string='Ngày giờ tạo',
                                              type='char', size=1024),
        'user_id': fields.many2one('res.users', string="Người tạo",readonly=True),        
    }
    _defaults = {
        'user_id': lambda self, cr, uid, context=None: uid,
    }
    ###################################################################
    ###################################################################
    ###################################################################    
snc_article_fix()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

