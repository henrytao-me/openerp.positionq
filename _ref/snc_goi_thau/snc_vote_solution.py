# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode

class snc_vote_solution(osv.osv):
    
    def function_get_value(self, cr, uid ,ids, fields, args, context=None):
        res = {}
        #init tham so
        tham_so_obj = self.pool.get('snc.tham.so')
        sql = '''
            SELECT id
            FROM snc_tham_so
        '''
        cr.execute(sql)
        if cr.rowcount:
            for tham_so_data in tham_so_obj.read(cr, uid, [x[0] for x in cr.fetchall()], ['code', 'gia_tri_hien_tai'], context=context):
                expression = tham_so_data['code'] + ' = ' + str(tham_so_data['gia_tri_hien_tai'])
                exec expression
        
        #cache vote_create_date
        vote_cache = {}
        #set value
        for obj in self.read(cr, uid, ids, ['vote_id', 'formula', 'r_value', 'lme'], context=context):
            #get snc.vote create date
            if not vote_cache.get(obj['vote_id']):
                vote_cache.update({
                    obj['vote_id']: self.pool.get('snc.vote').read(cr, uid, obj['vote_id'][0], ['create_date', 'lme'])
                })
            #get lme
            lme = vote_cache[obj['vote_id']].get('lme', 0)
            #
            value = 0
            data = {
                'f_value': 0,
                'name': 0
            } 
            f_value = 0
            try:                
                f_value = eval(obj['formula'])                
            except Exception, e:
#                logging.error(str(e))
                pass
            value = obj['r_value'] if obj['r_value'] >= 0 else f_value
            data.update({
                'f_value': f_value,
                'name': value
            })
            res[obj['id']] = data
        return res
        
    _name = 'snc.vote.solution'
    _description = 'Phuong An Bo Phieu'
    _columns = {
        'vote_id': fields.many2one('snc.vote', 'Đợt bỏ phiếu', ondelete="cascade"),
        'title': fields.char('Tên Phương án', size=128),                
        'formula': fields.char('Công thức', size=128),
        'f_value': fields.function(function_get_value, method=True, type='float', digits=(16,2),
                                 string='Giá trị', multi='function_get_value'),
        'r_value': fields.float('Giá trị', digits=(16,2)),
        
        'name': fields.function(function_get_value, method=True, type='float', digits=(16,2),
                                string='Giá trị', multi='function_get_value', 
                                store=True),
        
        'user_id': fields.many2one('res.users', string='Người tạo', required=True, readonly=True),
        'sort': fields.integer('Thứ tự'),
    }
    _defaults = {
        'sort': lambda *x: 0,
        'r_value': lambda *x: -1,        
        'user_id': lambda self, cr, uid, context=None: uid,
#        'title': lambda self, cr, uid, context=None: self.pool.get('res.users').read(cr, uid, uid, ['login']).get('login'),
        'title': lambda *x: 'Đề xuất', 
    }
    _order = 'sort desc, r_value asc'
    
    def read(self, cr, user, ids, fields=None, context=None, load='_classic_read'):
        if not context:
            context = {}
        res = []
        #check context vote_id exist
#        print '------------------------------------'
#        print '------------------------------------'
        if context.get('voting', None) == '1' and len(ids) > 1:
            ids = []
            ids1 = []
            ids2 = []
            if context.get('vote_id'):
                ids1 = self.search(cr, user, [('vote_id', '=', context.get('vote_id'))])
            else:
                ids2 = self.search(cr, user, [('vote_id', '=', False), ('user_id', '=', user)])
            ids = ids1 + ids2
            ids = self.search(cr, user, [('id', 'in', ids)])
#        print '------------------------------------'
#        print '------------------------------------'
        res = super(snc_vote_solution, self).read(cr, user, ids, fields=fields, context=context, load=load)
        return res
snc_vote_solution()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

