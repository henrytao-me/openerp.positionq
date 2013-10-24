# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode

class v_objects(osv.osv):
    
    def function_full_name(self, cr, uid, ids, fields, args, context):
        res = {}
        for obj in self.read(cr, uid, ids, ['name', 'parent_object']):
            if not obj['parent_object']:
                res[obj['id']] = obj['name']
            else:
                tmp = [
                    self.read(cr, uid, obj['parent_object'][0], ['full_name'])['full_name'],
                    obj['name']
                ]
                res[obj['id']] = ' / '.join(tmp) 
        return res
    
    def fnct_search_full_name(self, cr, uid, obj, name, args, context):                
#        ids = self.search(cr, uid, [('name', 'ilike', args[0]['2'])])
        res = [('name', 'ilike', args[0][2])]
        return res
    
    _rec_name = 'full_name'
    _name = 'v.objects'
    _description = 'V Objects'    
    _columns = {        
        'name': fields.char('Tên đối tượng', size=64, required=True, translate=True),
        'full_name': fields.function(function_full_name, method=True, type="char", size=256, 
                                     string="Tên đối tượng",
                                     fnct_search=fnct_search_full_name),

        'parent_object': fields.many2one('v.objects', string="Đối tượng cha"),
        'children_object': fields.one2many('v.objects', 'parent_object', string="Đối tượng con"),
        
        'models': fields.many2many('ir.model', 'res_vobjects_irmodel_rel', 'oid', 'mid', 'ir_model'),
        
        'is_active': fields.boolean('Active')     
    }
    _defaults = {
        'is_active': lambda *x: True
    }
    
    def create(self, cr, uid, vals, context=None):
        res = super(v_objects, self).create(cr, uid, vals, context=context)
        self.pool.get('v.access').reload_all(cr, uid)
        return res
    
    def write(self, cr, uid, ids, vals, context=None):
        res = super(v_objects, self).write(cr, uid, ids, vals, context=context)
        if vals.has_key('models') or vals.has_key('is_active'):
            self.pool.get('v.access').reload_all(cr, uid)
        return res
    
    def unlink(self, cr, uid, ids, context=None):
        res = super(v_objects, self).unlink(cr, uid, ids, context=context)
        self.pool.get('v.access').reload_all(cr, uid)
        return res
    
#    def get_all_model(self, cr, uid, objects_id=[]):
#        args = []
#        args.append(('is_active', '=', True))
#        if objects_id:
#            args.append(('id', 'in', objects_id))
#        res = {}
#        ids = self.search(cr, uid, args)
#        if ids:
#            for obj in self.read(cr, uid, ids, ['models']):
#                for m in obj['models']:
#                    res[m] = True
#        res = res.keys()
#        return res
#    
    
v_objects()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

