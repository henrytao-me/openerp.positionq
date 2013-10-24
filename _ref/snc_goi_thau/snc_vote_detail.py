# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode
import types

class snc_vote_detail(osv.osv):
    def get_value_type(self, cr, uid, ids, fields, args, context=None):
        res = {}
        obj_solution = self.pool.get('snc.vote.solution')
        for obj in self.read(cr, uid, ids, ['value']):
            if type(obj['value']) == types.TupleType:
                if obj_solution.read(cr, uid, obj['value'][0], ['r_value'])['r_value'] < 0:
                    res[obj['id']] = True
                    continue
            res[obj['id']] = False
        return res
    
    _name = 'snc.vote.detail'
    _description = 'Chi Tiet Bo Phieu'
    _columns = {
        'vote_id': fields.many2one('snc.vote', string='Tên đợt bỏ phiếu', ondelete="cascade"),
        
        'name': fields.char('Tiêu đề', size=64),        
        'user_id': fields.many2one('res.users', string='Người bỏ phiếu', required=True),        
        'value': fields.many2one('snc.vote.solution', string='Phương án'),
#                                 domain=[('vote_id', '=', 1)]),
        'value_type': fields.function(get_value_type, method=True, type="boolean", string="Loại phương án",
                                      store=True),
        
        'create_date': fields.datetime('Ngày bỏ phiếu', readonly=True)
    }
    _defaults = {
        'user_id': lambda self, cr, uid, context=None: uid,
    }
    _order = 'create_date asc'
    
    def get_vote_detail(self, cr, uid, vote_id, is_dict = False):
        res = []
        ids = self.search(cr, uid, [('vote_id', '=', vote_id)])
        data = {}
        for obj in self.read(cr, uid, ids):
            if not data.get(obj['user_id'][0]) or data.get(obj['user_id'], {}).get('create_date', '') < obj['create_date']:
                data.update({
                    obj['user_id'][0]: obj
                })
        if is_dict == True:
            return data
        for obj in data:
            res.append(data[obj])
        return res
    
    def _update_vote_solution_info(self, cr, uid, vote_detail_ids):
        if not vote_detail_ids:
            return
        if type(vote_detail_ids) != types.ListType:
            vote_detail_ids = [vote_detail_ids]
        #
        obj_vote_solution = self.pool.get('snc.vote.solution')
        for data in self.read(cr, uid, vote_detail_ids, ['vote_id', 'value']):
            #update vote solution info
            vote_id = data.get('vote_id')
            vote_solution_id = data.get('value')
            if vote_id != False and vote_solution_id != False:
                obj_vote_solution.write(cr, uid, vote_solution_id[0], {
                    'vote_id': vote_id[0]
                })
    
    def create(self, cr, user, vals, context=None):        
        res = super(snc_vote_detail, self).create(cr, user, vals, context=context)
        self._update_vote_solution_info(cr, user, res)
        return res
    
    def write(self, cr, user, ids, vals, context=None):
        res = None
        try:
            res = super(snc_vote_detail, self).write(cr, user, ids, vals, context=context)
            self._update_vote_solution_info(cr, user, ids)
        except:
            pass
        return res
    
    
snc_vote_detail()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

