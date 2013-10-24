# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from unidecode import unidecode

class snc_article_topic(osv.osv):
    ###################################################################
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
    _name = 'snc.article.topic'
    _description = 'Chu De Bai Viet'
    _columns = {
        'article_ids': fields.one2many('snc.article', 'name', string='Chủ đề bài viết'),
        'name': fields.char('Tiêu đề bài viết', size=128, required=True),
        'alias': fields.function(function_alias, method=True, string='Alias', type='char', size=2048),
        
        'sort': fields.integer('Sort'),
        'is_active': fields.boolean('Active'),
        'create_date': fields.datetime('Ngày giờ tạo', readonly=True),
        'user_id': fields.many2one('res.users', string="Người tạo",readonly=True),
    }
    _defaults = {
        'is_active': lambda *x: True,
        'sort': lambda *x: 0,
        'user_id': lambda self, cr, uid, context=None: uid,
    }
    
snc_article_topic()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

