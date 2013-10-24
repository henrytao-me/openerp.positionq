# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.osv.fields import datetime as datetime_field
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from unidecode import unidecode
import types
from openerp import tools

import locale
from locale import localeconv
import re
from openerp.tools.safe_eval import safe_eval as eval

_logger = logging.getLogger(__name__)


class ir_model_depend(osv.osv):
    
    def _get_ir_model_depend_detail(self, cr, uid, ids, context=None):
        res = []
        for obj in self.pool.get('ir.model.depend.detail').read(cr, uid, ids, ['name']):
            if not obj['name'] or obj['name'] == False:
                continue
            if obj['name'][0] in res:
                continue
            res.append(obj['name'][0])
        return res
    
    def function_count(self, cr, uid, ids, fields, args, context=None):
        res = {}
        for obj in self.read(cr, uid, ids, ['model_depend']):
            res[obj['id']] = len(obj['model_depend'])
        return res
    
    def function_root_model(self, cr, uid, ids, fields, args, context=None):
        res = {}
        ir_model_depend_detail = self.pool.get('ir.model.depend.detail')
        for obj in self.read(cr, uid, ids, ['model_depend']):
            res[obj['id']] = {
                'root_model': 0,
                'root_model_name': '-'
            }
            if obj['model_depend']:
                depend_detail_id = obj['model_depend'][0]
                tmp_id = self.pool.get('ir.model.depend.detail').search(cr, uid, [('id', 'in', obj['model_depend']),
                                                                               ('is_root', '=', True)],
                                                                        limit = 1)
                if tmp_id:
                    depend_detail_id = tmp_id[0]
                #get real model id
                tmp = ir_model_depend_detail.read(
                                        cr, uid, depend_detail_id, ['model']).get('model', (0, '-'))
                res[obj['id']] = {
                    'root_model': tmp[0],
                    'root_model_name': tmp[1]
                }
        return res
    
    _name = 'ir.model.depend'
    _description = 'Nhom Doi Tuong'
    _columns = {
        'name': fields.char('Tên nhóm', size=256),
        'model_depend': fields.one2many('ir.model.depend.detail', 'name', string="Model"),
        
        'count': fields.function(function_count, method=True, string="Num Of Children", type="integer",
                                 store={
                                    'ir.model.depend.detail': (_get_ir_model_depend_detail, [], 10)
                                 }),
        
        'root_model': fields.function(function_root_model, method=True, type="integer", string="Root Model",
                                      multi='function_root_model',
                                      store={
                                        'ir.model.depend.detail': (_get_ir_model_depend_detail, [], 10)
                                      }),
        'root_model_name': fields.function(function_root_model, method=True, type="char", size=128, 
                                    string="Root Model", multi='function_root_model',
                                    store={
                                        'ir.model.depend.detail': (_get_ir_model_depend_detail, [], 10)
                                    }),
    }
    _defaults = {
    }
    
    def get_child_model(self, cr, uid, id):
        res = []
        ids = self.read(cr, uid, id, ['model_depend'])['model_depend']
        for obj in self.pool.get('ir.model.depend.detail').read(cr, uid, ids, ['model']):
            if not obj['model'] or obj['model'] == False:
                continue
            res.append(obj['model'][0])
        return res
    
    def write(self, cr, uid, ids, vals, context=None):
        res = super(ir_model_depend, self).write(cr, uid, ids, vals, context=context)
        self.pool.get('ir.model.access.new')._is_reload = True
        return res
    
    def create(self, cr, uid, vals, context=None):    
        res = super(ir_model_depend, self).create(cr, uid, vals, context=context)
        self.pool.get('ir.model.access.new')._is_reload = True
        return res
    
ir_model_depend()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: