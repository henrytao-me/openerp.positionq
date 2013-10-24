# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from unidecode import unidecode
import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
import types

class snc_article(osv.osv):
    
    ###################################################################
    def function_alias(self, cr, uid, ids, fields, args, context=None):
        if not context:
            context = {}
        res = {}
        utils = self.pool.get('vieterp.utils')
        for obj in self.read(cr, uid, ids, ['name'], context=context):
            res[obj['id']] = utils.get_alias_from_string(cr, uid, obj['name'])
        return res
    
    ###################################################################
    def unlink(self, cr, uid, ids, context=None):
        if not context:
            context = {}
        snc_ids = self.read(cr, uid, ids,['user_id'],context=context)
        for obj in snc_ids:
            if obj['user_id'][0] != uid:
                raise osv.except_osv(_('Lỗi!'), _('Không thể xoá dữ liệu của các user khác'))
        return super(snc_article, self).unlink(cr, uid, ids, context=context)
    ###################################################################
    def write(self, cr, user, ids, vals, context=None):
        snc_ids = self.read(cr, user, ids,['user_id'],context=context)
        for obj in snc_ids:
            if obj['user_id'][0] != user:
                raise osv.except_osv(_('Lỗi!'), _('Không thể thay đổi dữ liệu của các user khác'))
        return super(snc_article, self).write(cr, user, ids, vals, context=context)
    
    ###################################################################
        
    _name = 'snc.article'
    _description = 'Bai Viet Theo Chu De'
    _columns = {
        'name': fields.char('Tiêu đề bài viết', size=128, required=True),
        'topic_id': fields.many2one('snc.article.topic', string='Chủ đề'),        
        'alias': fields.function(function_alias, method=True, string="Alias", type='char', size=512, store=True),
        'description': fields.html('Mô tả ngắn gọn', required=True),
        'content': fields.html('Nội dung chi tiết', required=True),
        'view': fields.integer('Lượt xem'),
        'level': fields.selection([('1', 'Tin hot'), ('2', 'Tin đáng chú ý'), ('100', 'Tin bình thường')], 'Mức độ'),
        'source': fields.many2one('snc.article.source', string="Nguồn"),
        
        'is_active': fields.boolean('Active'),
        'create_date': fields.datetime('Ngày giờ tạo', readonly=True),
        'user_id': fields.many2one('res.users', string='Người đăng tin', readonly=True),
    }
    _defaults = {
        'is_active': lambda *x: True,
        'view': lambda *x: 0,
        'level': lambda *x: 100,
        'user_id': lambda self, cr, uid, context=None: uid,
    }
    _order = 'create_date desc'
    
    ###################################################################
    
    def get_article_most_read(self, cr, uid, fields = None, num_of_day = 10, limit=None):
        
        d1 = datetime.timedelta(days=num_of_day)
        d2 = datetime.datetime.now() - d1
        d2 = d2.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        
        article_ids = self.search (cr,uid,[('create_date','>=', d2)], limit=limit)
        
        if fields:
            if 'view' not in fields:
                fields.append('view')
                
        article_ls = self.pool.get('snc.article').read(cr, uid, article_ids, fields)
        article_ls.sort(key = lambda x: x['view'], reverse=True) 
        
        return article_ls
    
    ###################################################################
    def GetArticle(self, cr, uid, topic_ids = None, fields = None, limit = 3):
        res = []
        is_list = True
        if not topic_ids:
            topic_ids = []
        if type(topic_ids) != types.ListType:
            is_list = False
            topic_ids = [topic_ids]
        # get data
        for topic_id in topic_ids:
            ids = self.search(cr, uid, [('topic_id', '=', topic_id)], limit = limit)
            data = []
            if ids:
                data = self.read(cr, uid, ids, fields)
                res.append({
                    'topic_id': topic_id,
                    'name': data[0]['topic_id'][1],
                    'news': data
                })
        return res
    
snc_article()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

