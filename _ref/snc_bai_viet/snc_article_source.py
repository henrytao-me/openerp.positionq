# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from unidecode import unidecode

class snc_article_source(osv.osv):
    ###################################################################
    ###################################################################
    ###################################################################
    _name = 'snc.article.source'
    _description = 'Nguon Bai Viet'
    _columns = {
        'name': fields.char('Nguồn', size=512, required=True),
        'article_ids': fields.one2many('snc.article', 'name', string='Bài viết'),        
        
        'create_date': fields.datetime('Ngày giờ tạo', readonly=True)
    }
    _defaults = {
                 
    }
    _order = 'name asc'
    
snc_article_source()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

