# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.osv.fields import datetime as datetime_field
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from unidecode import unidecode
import types

class ir_model_access_new(osv.osv):
    
    SELECTION = (('Yes', 'Yes'),
                ('No', 'No'),
                ('Inherit', 'Inherit'))
    
    _name = 'ir.model.access.new'
    _description = 'Customized access control management'
    _columns = {
        'group_id': fields.integer('Nhóm người dùng', readonly=True),
        'user_id': fields.integer('Người dùng', readonly=True),
        'model_id': fields.integer('Đối tượng', readonly=True),
        
        'group_name': fields.char('Nhóm người dùng', size=256, readonly=True),
        'user_name': fields.char('Người dùng', size=256, readonly=True),
        'model_name': fields.char('Đối tượng', size=256, readonly=True),
        
        'perm_read': fields.boolean('Quyền xem'),
        'perm_write': fields.boolean('Quyền sửa'),
        'perm_create': fields.boolean('Quyền tạo'),
        'perm_unlink': fields.boolean('Quyền xoá'),
        'perm_manage': fields.boolean('Quyền quản trị'),
        
        'perm_read_new': fields.selection(SELECTION, string='Quyền xem', required=True),
        'perm_unlink_new': fields.selection(SELECTION, string='Quyền xoá', required=True),
        'perm_write_new': fields.selection(SELECTION, string='Quyền sửa', required=True),
        'perm_create_new': fields.selection(SELECTION, string='Quyền tạo', required=True),
        
        'sort': fields.integer('Sort')
    }
    _defaults = {
        'sort': lambda *x: 0,
        'perm_read_new': lambda *x: 'Inherit',
        'perm_unlink_new': lambda *x: 'Inherit',
        'perm_write_new': lambda *x: 'Inherit',
        'perm_create_new': lambda *x: 'Inherit',
    }
    _order = 'group_name, sort desc, user_name, model_name'
    
    _is_reload = True
    _is_reloading = False
    
    def update_access(self, cr, uid, data, context=None):
        perm_read = perm_write = perm_create = perm_unlink = False
        perm_read_new = data.get('perm_read_new', 'No')
        perm_write_new = data.get('perm_write_new', 'No')
        perm_create_new = data.get('perm_create_new', 'No')
        perm_unlink_new = data.get('perm_unlink_new', 'No')
        
        group_obj = self.pool.get('res.groups')
        group_id = data.get('group_id', False)
        group = group_id and group_obj.browse(cr, uid, group_id, context=context) or False
        
        if not group.special_user:
            perm_read = (perm_read_new == 'No') and False or True
            perm_write = (perm_write_new == 'No') and False or True
            perm_create = (perm_create_new == 'No') and False or True
            perm_unlink = (perm_unlink_new == 'No') and False or True
        else:
            should_check_full_read = should_check_full_write = should_check_full_create = should_check_full_unlink = False
            
            if perm_read_new == 'No': perm_read = False
            elif perm_read_new == 'Yes': perm_read = True
            else: should_check_full_read = True
            
            if perm_write_new == 'No': perm_write = False
            elif perm_write_new == 'Yes': perm_write = True
            else: should_check_full_write = True
            
            if perm_create_new == 'No': perm_create = False
            elif perm_create_new == 'Yes': perm_create = True
            else: should_check_full_create = True
            
            if perm_unlink_new == 'No': perm_unlink = False
            elif perm_unlink_new == 'Yes': perm_unlink = True
            else: should_check_full_unlink = True
            
            if should_check_full_read or should_check_full_write or should_check_full_create or should_check_full_unlink:
                group_ids = []
                for other_group in group.special_user.groups_id:
                    if other_group.id != group_id:
                        group_ids.append(other_group.id)
                
                if should_check_full_read:
                    perm_read = False
                    sql = '''SELECT 1 FROM ir_model_access WHERE perm_read = True AND group_id IN %s AND model_id = %s'''
                    cr.execute(sql, (tuple(group_ids + [-1, -1]), model_id.id))
                    if cr.rowcount: perm_read = True
                
                if should_check_full_write:
                    perm_write = False
                    sql = '''SELECT 1 FROM ir_model_access WHERE perm_write = True AND group_id IN %s AND model_id = %s'''
                    cr.execute(sql, (tuple(group_ids + [-1, -1]), model_id.id))
                    if cr.rowcount: perm_write = True
                    
                if should_check_full_create:
                    perm_create = False
                    sql = '''SELECT 1 FROM ir_model_access WHERE perm_create = True AND group_id IN %s AND model_id = %s'''
                    cr.execute(sql, (tuple(group_ids + [-1, -1]), model_id.id))
                    if cr.rowcount: perm_create = True
                
                if should_check_full_unlink:
                    perm_unlink = False
                    sql = '''SELECT 1 FROM ir_model_access WHERE perm_unlink = True AND group_id IN %s AND model_id = %s'''
                    cr.execute(sql, (tuple(group_ids + [-1, -1]), model_id.id))
                    if cr.rowcount: perm_unlink = True
            
            logging.info('Processed special group: ''%s'' of user ''%s'' with result: %s-%s-%s-%s (RWUC)', 
                         group.name, group.special_user.name, perm_read, perm_write, perm_create, perm_unlink)
        
        res = {'perm_read': perm_read, 'perm_write': perm_write, 'perm_create': perm_create, 'perm_unlink': perm_unlink}
        return res
    
    def get_permission(self, cr, uid, model_id, group_id):
        res = {}
        ir_model_access = self.pool.get('ir.model.access')        
        ids = ir_model_access.search(cr, uid, [('model_id', '=', model_id), ('group_id', '=', group_id)])
        if ids:
            data = ir_model_access.read(cr, uid, ids[0], ['perm_read', 'perm_write', 'perm_create',
                                                          'perm_unlink', 'perm_manage',
                                                          'perm_read_new', 'perm_write_new', 'perm_create_new', 'perm_unlink_new'])
            permission = {
                'perm_read': data.get('perm_read', False),
                'perm_write': data.get('perm_write', False),
                'perm_create': data.get('perm_create', False),
                'perm_unlink': data.get('perm_unlink', False),
                'perm_manage': data.get('perm_manage', False),
                'perm_read_new': data.get('perm_read_new', False),
                'perm_write_new': data.get('perm_write_new', False),
                'perm_create_new': data.get('perm_create_new', False),
                'perm_unlink_new': data.get('perm_unlink_new', False),
            }
            res.update(permission)
        return res
    
    def fix_model_depend_permission(self, cr, uid):
        ir_model_access = self.pool.get('ir.model.access')
        ir_model_depend = self.pool.get('ir.model.depend')
        
        ids = ir_model_depend.search(cr, uid, [])
        
        for obj in ir_model_depend.read(cr, uid, ids, ['root_model']):
            root_model = obj['root_model']
            child_model = ir_model_depend.get_child_model(cr, uid, obj['id'])
            child_model.pop(child_model.index(root_model))
            
            #get root_model permission
            root_ids = ir_model_access.search(cr, uid, [('model_id', '=', root_model)])
            
            #remove all child model permission
            child_ids = ir_model_access.search(cr, uid, [('model_id', 'in', child_model)])
            ir_model_access.unlink(cr, uid, child_ids)
            
            #update new permission from root model to all child model
            if root_ids:
                for access in ir_model_access.read(cr, uid, root_ids):
                    if access.get('group_id', False) == False:
                        continue
                    for model_id in child_model:
                        ir_model_access.create(cr, uid, {
                            'name': 'auto',
                            'model_id': model_id,
                            'group_id': access['group_id'][0],
                            'perm_read': access['perm_read'], 
                            'perm_write': access['perm_write'],
                            'perm_create': access['perm_create'],
                            'perm_unlink': access['perm_unlink'],
                            'perm_manage': access['perm_manage'], 
                        })            
        return True
    
    def reload(self, cr, uid, context=None):
        if self._is_reload != True:
            return False
        self._is_reload = False
        self._is_reloading = True
        
        #clear table
        sql = '''
            DELETE FROM ir_model_access_new
        '''
        cr.execute(sql)
        #fix model depend permission
        self.fix_model_depend_permission(cr, uid)
        #create special user group
        user_ids = self.pool.get('res.users').search(cr, uid, [('is_project_specific', '=', True)])        
        self.pool.get('res.users').create_special_group(cr, uid, user_ids)
        user_data = {}
        for obj in self.pool.get('res.users').read(cr, uid, user_ids, ['name', 'special_group']):
            user_data[obj['id']] = obj
            
        #get model ids        
        model_ids = self.pool.get('ir.model.depend').search(cr, uid, [('count', '>', 0)])
        model_data = {}
        for obj in self.pool.get('ir.model.depend').read(cr, uid, model_ids, ['name', 'root_model']):
            model_data[obj['id']] = obj
        
        #for group_ids
        group_ids = self.pool.get('res.groups').search(cr, uid, [('special_user', '=', False),
                                                                 ('is_project_specific', '=', True)])
        
        for group in self.pool.get('res.groups').read(cr, uid, group_ids, ['full_name', 'special_uid', 'users']):
            for model in model_ids:
#                vals = {
#                    'group_id': group['id'],
##                    'user_id': user_data[user]['special_group'][0],                        
#                    'model_id': model,
#                    'group_name': group['full_name'],
##                    'user_name': user_data[user]['name'],
#                    'model_name': model_data[model]['name'],
#                    'sort': 1
#                }                
#                vals.update(self.get_permission(cr, uid, model_data[model]['root_model'], group['id']))
#                self.create(cr, uid, vals)
                
                for user in group['users']:
                    if not user_data.get(user) or not user_data.get(user, {}).get('special_group'):
                        continue
                    vals = {
                        'group_id': group['id'],
                        'user_id': user_data[user]['special_group'][0],                        
                        'model_id': model,
                        'group_name': group['full_name'],
                        'user_name': user_data[user]['name'],
                        'model_name': model_data[model]['name']
                    }
                    vals.update(self.get_permission(cr, uid, model_data[model]['root_model'], user_data[user]['special_group'][0]))
                    self.create(cr, uid, vals)
        #finalize
        self._is_reloading = False        
        return True
    
    def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False):
        self.reload(cr, uid, context=context)
        res = super(ir_model_access_new, self).search(cr, uid, args, offset=offset, limit=limit, order=order,
                                                         context=context, count=count)
        return res
    
    def read_group(self, cr, uid, domain, fields, groupby, offset=0, limit=None, context=None, orderby=False):
        res = []
        try:
            res = super(ir_model_access_new, self).read_group(cr, uid, domain, fields, groupby, 
                                                           offset=offset, limit=limit, 
                                                           context=context, orderby=orderby)
        except:
            pass
        return res
         
    def write(self, cr, uid, ids, vals, context=None):
        if not vals:
            vals = {}
        res = super(ir_model_access_new, self).write(cr, uid, ids, vals, context=context)
        #check for finish reload
        if self._is_reloading != False:
            return
        #
        for obj in self.read(cr, uid, ids, ['group_id', 'user_id', 'model_id']):
            is_group = True
            #get group
            group_id = obj['group_id']
            if obj['user_id']:      #if set permission for user
                group_id = obj['user_id']
                is_group = False
            #get model
            ir_model_access = self.pool.get('ir.model.access')
#            for model_id in self.pool.get('ir.model.depend').read(cr, uid, obj['model_id'], ['child_model'])['child_model']:
            for model_id in self.pool.get('ir.model.depend').get_child_model(cr, uid, obj['model_id']):
                data = vals.copy()
                data.update({
                    'model_id': model_id,
                    'group_id': group_id
                })
                data.update(self.update_access(cr, uid, data, context=context))
                model_access_id = ir_model_access.search(cr, uid, [('model_id', '=', model_id), 
                                                                   ('group_id', '=', group_id)])
                if not model_access_id:
                    data.update({
                        'name': 'auto'
                    })
                    ir_model_access.create(cr, uid, data)
                else:
                    ir_model_access.write(cr, uid, model_access_id, data)            
        return res
    
ir_model_access_new()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

