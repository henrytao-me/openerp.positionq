# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging

class snc_article_audio(osv.osv):
    
    def function_alias(self, cr, uid, ids, fields, args, context=None):
        if not context:
            context = {}
        res = {}
        utils = self.pool.get('vieterp.utils')
        for obj in self.read(cr, uid, ids, ['name']):
            res[obj['id']] = utils.get_alias_from_string(cr, uid, obj['name'])
        return res
    
    _name = 'snc.article.audio'
    _description = 'Ban Tin Audio'
    _columns = {
        'name': fields.char('Tiêu đề', size=128, required=True),
#        'alias': fields.function(function_alias, method=True, string='Alias', type='char', size=512),
        'file': fields.binary('Audio File'),
        'description': fields.char('Mô tả', size=128),
        'filemanager': fields.char('File Manager', size=256),
        
        'is_active': fields.boolean('Active'),
        
        'user_id': fields.many2one('res.users', string="Người tạo",readonly=True),
        'create_date': fields.datetime('Ngày giờ tạo', readonly=True)
    }
    _defaults = {
        'is_active': lambda *x: True,
        'user_id': lambda self, cr, uid, context=None: uid,
    }
    _order = 'is_active, create_date desc'
    
    
snc_article_audio()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

