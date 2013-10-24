# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode
import types

class pq_vi_tri(osv.osv):
    
    def func_diem(self, cr, uid, ids, fields, args, context=None):
        res = {}
        # get pq_vi_tri_yeu_to
        vi_tri_yeu_to = self.pool.get('pq.vi.tri.yeu.to').get_matrix(cr, uid, [('id', 'in', ids)])
        # starts
        for obj in self.read(cr, uid, ids, ['name']):
            res[obj['id']] = vi_tri_yeu_to.get('matrix',{}).get(obj['id'],{}).get('diem',0)
        return res
    
    _name = 'pq.vi.tri'
    _description = 'Vi tri'
    _columns = {
        'name': fields.char('Tên vị trí', size=128, required=True),
        'bo_phan': fields.many2one('pq.bo.phan', string="Bộ phận", required=True),
        'nhom_vi_tri': fields.many2one('pq.nhom.vi.tri', string="Nhóm vị trí", required=True),
        
        'diem': fields.function(func_diem, method=True, string="Điểm", type="float", digits=(16,2)),
        
        'create_date': fields.datetime('Ngày giờ tạo', readonly=True),
        'user_id': fields.many2one('res.users', string="Người tạo",readonly=True),
    }
    _defaults = {
        'user_id': lambda self, cr, uid, context=None: uid,
    }
    
    def create(self, cr, uid, vals, context=None):
        res = super(pq_vi_tri, self).create(cr, uid, vals, context)
        self.pool.get('pq.vi.tri.yeu.to').auto_sync(cr, uid, vi_tri_id=res)     
        return res
    
pq_vi_tri()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

