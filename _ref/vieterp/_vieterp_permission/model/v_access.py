# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.osv.fields import datetime as datetime_field
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from unidecode import unidecode
import types

class v_access(osv.osv):
    
    SELECTION = (('2', 'Yes'),
                ('1', 'Inherit'),
                ('0', 'No'))
    
    def function_level(self, cr, uid, ids, fields, args, context={}):
        res = {}
        for obj in self.read(cr, uid, ids, ['group_id', 'user_id', 'object_id']):
            level = 3
            if not obj['group_id']:
                level -= 1
            if not obj['user_id']:
                level -= 1
            if not obj['object_id']:
                level -= 1
            res[obj['id']] = level
        return res
    
    def function_f_real_perm(self, cr, uid, ids, fields, args, context={}):
        perm = fields.replace('f_real_', '')
        _context = context.copy()
        _context.update({'real_'+perm: True})
        ls = self.read(cr, uid, ids, ['level', perm, 'parent_'+perm, 'real_'+perm])
        ls.sort(key=lambda x: x['level'])
        for obj in ls:
            real_perm = obj['parent_'+perm]            
            if obj[perm] == '0':
                real_perm = False
            elif obj[perm] == '2':
                real_perm = True
            #if real_perm != obj['real_'+perm] or (real_perm == obj['real_'+perm] and obj[perm] != '1'):
            self.write(cr, uid, obj['id'], {'real_'+perm: real_perm}, context=_context)
        return dict((k, '') for k in ids)
    
    def function_tg_real_perm(self, cr, uid, ids, fields, args, context={}):
        perm = fields.replace('tg_real_', '')
        self._update_perm(cr, uid, ids, perm, context=context)
        return dict((k, '') for k in ids)
    
    def _update_perm(self, cr, uid, ids, perm, context={}):
        if not isinstance(ids, types.ListType):
            ids = [ids]
        if context.get('real_'+perm, False) == True or context.get('force', False) == True:
            ls = self.read(cr, uid, ids, ['level', 'group_id', 'user_id', 'object_id'])
            ls.sort(key=lambda x: x['level'])
            for obj in ls:
                group_id = False if not obj['group_id'] else obj['group_id'][0]
                user_id = False if not obj['user_id'] else obj['user_id'][0]
                object_id = False if not obj['object_id'] else obj['object_id'][0]                
                if obj['level'] == 1:       #update parent_perm_... level 2
                    tmp_ids = self.search(cr, uid, [
                        ('level','=',2), 
                        '|', '&', ('group_id','=',group_id), ('group_id','!=',False),
                        '|', '&', ('user_id','=',user_id), ('user_id','!=',False),
                             '&', ('object_id','=',object_id), ('object_id','!=',False),
                                                    ])
                    self._update_parent_perm_level_2(cr, uid, perm, tmp_ids, context=context)
                elif obj['level'] == 2:     #update parent_perm_... level 3
                    tmp_ids = self.search(cr, uid, [
                        ('level','=',3),
                        '|', '&', '&', ('group_id','=',group_id), ('group_id','!=',False),
                                  '&', ('user_id','=',user_id), ('user_id','!=',False),
                        '|', '&', '&', ('group_id','=',group_id), ('group_id','!=',False),
                                  '&', ('object_id','=',object_id), ('object_id','!=',False),
                             '&', '&', ('user_id','=',user_id), ('user_id','!=',False),
                                  '&', ('object_id','=',object_id), ('object_id','!=',False),
                                                    ])
                    self._update_parent_perm_level_3(cr, uid, perm, tmp_ids, context=context)
                elif obj['level'] == 3:     #update ir.model.access
                    self._update_real_perm(cr, uid, perm, obj['id'], context=context)
                    pass
        return True
    
    def _update_parent_perm_level_2(self, cr, uid, perm, ids, context={}):
        if not isinstance(ids, types.ListType):
            ids = [ids]
        bak = {'group': {}, 'user': {}, 'object': {}}
        for obj in self.read(cr, uid, ids, ['group_id', 'user_id', 'object_id', 'parent_'+perm]):
            group_id = False if not obj['group_id'] else obj['group_id'][0]
            user_id = False if not obj['user_id'] else obj['user_id'][0]
            object_id = False if not obj['object_id'] else obj['object_id'][0]
            #
            if group_id and not bak['group'].has_key(group_id):
                tmp_ids = self.search(cr, uid, [('level','=',1), ('group_id','=',group_id)])
                if tmp_ids:
                    bak['group'][group_id] = self.read(cr, uid, tmp_ids[0], ['real_'+perm])['real_'+perm]
            #       
            if user_id and not bak['user'].has_key(user_id):
                tmp_ids = self.search(cr, uid, [('level','=',1), ('user_id','=',user_id)])
                if tmp_ids:
                    bak['user'][user_id] = self.read(cr, uid, tmp_ids[0], ['real_'+perm])['real_'+perm]
            #
            if object_id and not bak['object'].has_key(object_id):
                tmp_ids = self.search(cr, uid, [('level','=',1), ('object_id','=',object_id)])
                if tmp_ids:
                    bak['object'][object_id] = self.read(cr, uid, tmp_ids[0], ['real_'+perm])['real_'+perm]
            #
            parent_perm = bak['group'].get(group_id, False) or bak['user'].get(user_id, False) or bak['object'].get(object_id, False)
            if obj['parent_'+perm] != parent_perm:
                self.write(cr, uid, obj['id'], {'parent_'+perm: parent_perm}, context=context)
    
    def _update_parent_perm_level_3(self, cr, uid, perm, ids, context={}):
        if not isinstance(ids, types.ListType):
            ids = [ids]
        bak = {'gu': {}, 'go': {}, 'uo': {}}
        for obj in self.read(cr, uid, ids, ['group_id', 'user_id', 'object_id', 'parent_'+perm]):
            group_id = False if not obj['group_id'] else obj['group_id'][0]
            user_id = False if not obj['user_id'] else obj['user_id'][0]
            object_id = False if not obj['object_id'] else obj['object_id'][0]
            gu = str(group_id) + '_' + str(user_id)
            go = str(group_id) + '_' + str(object_id)
            uo = str(user_id) + '_' + str(object_id)
            #
            if not bak['gu'].has_key(gu):
                tmp_ids = self.search(cr, uid, [('level','=',2), 
                                                ('group_id','=',group_id),
                                                ('user_id','=',user_id)])
                if tmp_ids:
                    bak['gu'][gu] = self.read(cr, uid, tmp_ids[0], ['real_'+perm, perm])
            #
            if not bak['go'].has_key(go):
                tmp_ids = self.search(cr, uid, [('level','=',2), 
                                                ('group_id','=',group_id),
                                                ('object_id','=',object_id)])
                if tmp_ids:
                    bak['go'][go] = self.read(cr, uid, tmp_ids[0], ['real_'+perm, perm])
            #
            if not bak['uo'].has_key(uo):
                tmp_ids = self.search(cr, uid, [('level','=',2),
                                                ('user_id','=',user_id),
                                                ('object_id','=',object_id)])
                if tmp_ids:
                    bak['uo'][uo] = self.read(cr, uid, tmp_ids[0], ['real_'+perm, perm])
            #
            #parent_perm_inherit = bak['gu'].get(gu, False) or bak['go'].get(go, False) or bak['uo'].get(uo, False)
            parent_perm = False
            parent_perm_inherit = False
            is_force = False
            tmp_data = {'gu': gu, 'go': go, 'uo': uo}
            for v in tmp_data:
                if bak[v].get(tmp_data[v], {'real_'+perm: False, perm: '1'})[perm] != '1':
                    is_force = True
                if is_force == True:
                    if bak[v].get(tmp_data[v], {'real_'+perm: False, perm: '1'})[perm] != '1':
                        parent_perm = parent_perm or bak[v].get(tmp_data[v], {'real_'+perm: False, perm: '1'})['real_'+perm]
                else:
                    parent_perm_inherit = parent_perm_inherit or bak[v].get(tmp_data[v], {'real_'+perm: False, perm: '1'})['real_'+perm]
            if is_force == False:
                parent_perm = parent_perm_inherit
            #
            if obj['parent_'+perm] != parent_perm:
                self.write(cr, uid, obj['id'], {'parent_'+perm: parent_perm}, context=context)
    
    def _update_real_perm(self, cr, uid, perm, ids, context={}):
        if not isinstance(ids, types.ListType):
            ids = [ids]
        ids = self.search(cr, uid, [('id', 'in', ids), ('level', '=', 3)])
        for obj in self.read(cr, uid, ids, ['real_'+perm, 'user_id', 'object_id']):
            try:
                user_id = obj['user_id'][0]
                object_id = obj['object_id'][0]
                real_perm = obj['real_'+perm]
                #
                group_id = self.pool.get('res.users').read(cr, uid, user_id, ['special_group'])['special_group'][0]
                model_ids = self.pool.get('v.objects').read(cr, uid, object_id, ['models'])['models']
                #
                for model_id in model_ids:
                    ids = self.pool.get('ir.model.access').search(cr, uid, [('group_id', '=', group_id),
                                                                            ('model_id', '=', model_id)])
                    if ids:
                        self.pool.get('ir.model.access').write(cr, uid, ids, {perm: real_perm})
                    else:
                        self.pool.get('ir.model.access').create(cr, uid, {'name': 'v_access',
                                                                          'is_active': True,
                                                                          'model_id': model_id,
                                                                          'group_id': group_id,
                                                                          perm: real_perm})
            except:
                raise
                pass
        return True
    
    _name = 'v.access'
    _description = 'Customized access control management'
    _columns = {
        'group_id': fields.many2one('v.groups', string="Nhóm người dùng"),
        'user_id': fields.many2one('res.users', string="Người dùng"),
        'object_id': fields.many2one('v.objects', string="Đối tượng"),
        #
        'level': fields.function(function_level, method=True, string="Level", type="integer", 
                store={
                    'v.access': (lambda self,cr,uid,ids,context=None: ids, None, 10),
                }),
        #     
        'perm_read': fields.selection(SELECTION, string='Xem', required=True),
        'perm_unlink': fields.selection(SELECTION, string='Xoá', required=True),
        'perm_write': fields.selection(SELECTION, string='Sửa', required=True),
        'perm_create': fields.selection(SELECTION, string='Tạo', required=True),
        'perm_manage': fields.selection(SELECTION, string='Quản trị', required=True),
        #
        'parent_perm_read': fields.boolean('Xem'),
        'parent_perm_unlink': fields.boolean('Xóa'),
        'parent_perm_write': fields.boolean('Sửa'),
        'parent_perm_create': fields.boolean('Tạo'),
        'parent_perm_manage': fields.boolean('Quản trị'),
        #
        'real_perm_read': fields.boolean('Xem'),
        'real_perm_unlink': fields.boolean('Xóa'),
        'real_perm_write': fields.boolean('Sửa'),
        'real_perm_create': fields.boolean('Tạo'),
        'real_perm_manage': fields.boolean('Quản trị'),
        #read
        'f_real_perm_read': fields.function(function_f_real_perm, method=True, string="Xem", type="char", 
                store={
                    'v.access': (lambda self,cr,uid,ids,context=None: ids, ['perm_read', 
                                                                            'parent_perm_read'], 20),
                }),
        'tg_real_perm_read': fields.function(function_tg_real_perm, method=True, string="Xem", type="char",
                store={
                    'v.access': (lambda self,cr,uid,ids,context=None: ids, ['real_perm_read'], 15),
                }),
        #write
        'f_real_perm_write': fields.function(function_f_real_perm, method=True, string="Sửa", type="char", 
                store={
                    'v.access': (lambda self,cr,uid,ids,context=None: ids, ['perm_write', 
                                                                            'parent_perm_write'], 20),
                }),
        'tg_real_perm_write': fields.function(function_tg_real_perm, method=True, string="Sửa", type="char",
                store={
                    'v.access': (lambda self,cr,uid,ids,context=None: ids, ['real_perm_write'], 15),
                }),
        #create
        'f_real_perm_create': fields.function(function_f_real_perm, method=True, string="Tạo", type="char", 
                store={
                    'v.access': (lambda self,cr,uid,ids,context=None: ids, ['perm_create', 
                                                                            'parent_perm_create'], 20),
                }),
        'tg_real_perm_create': fields.function(function_tg_real_perm, method=True, string="Tạo", type="char",
                store={
                    'v.access': (lambda self,cr,uid,ids,context=None: ids, ['real_perm_create'], 15),
                }),
        #unlink
        'f_real_perm_unlink': fields.function(function_f_real_perm, method=True, string="Xóa", type="char", 
                store={
                    'v.access': (lambda self,cr,uid,ids,context=None: ids, ['perm_unlink', 
                                                                            'parent_perm_unlink'], 20),
                }),
        'tg_real_perm_unlink': fields.function(function_tg_real_perm, method=True, string="Xóa", type="char",
                store={
                    'v.access': (lambda self,cr,uid,ids,context=None: ids, ['real_perm_unlink'], 15),
                }),
        #manage
        'f_real_perm_manage': fields.function(function_f_real_perm, method=True, string="Quản trị", type="char", 
                store={
                    'v.access': (lambda self,cr,uid,ids,context=None: ids, ['perm_manage', 
                                                                            'parent_perm_manage'], 20),
                }),
        'tg_real_perm_manage': fields.function(function_tg_real_perm, method=True, string="Quản trị", type="char",
                store={
                    'v.access': (lambda self,cr,uid,ids,context=None: ids, ['real_perm_manage'], 15),
                }),
        #
        'ready': fields.boolean('Ready'),
        '_free': fields.char('Free', readonly=True)
    }
    _defaults = {
        'perm_read': lambda *x: '1',
        'perm_unlink': lambda *x: '1',
        'perm_write': lambda *x: '1',
        'perm_create': lambda *x: '1',
        'perm_manage': lambda *x: '1',
        
        'parent_perm_read': lambda *x: False,
        'parent_perm_write': lambda *x: False,
        'parent_perm_create': lambda *x: False,
        'parent_perm_unlink': lambda *x: False,
        'parent_perm_manage': lambda *x: False,
        
        'real_perm_read': lambda *x: False,
        'real_perm_write': lambda *x: False,
        'real_perm_create': lambda *x: False,
        'real_perm_unlink': lambda *x: False,
        'real_perm_manage': lambda *x: False,
        
        'ready': lambda *x: True,
        '_free': lambda *x: ''
    }
    _order = 'group_id, user_id, object_id'
    
    _is_reload = True
    _reloaded = True
    _time_max = 2
    _time_index = 0
    
    def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False):
#        self.reload_access(cr, uid, context=context)
        res = super(v_access, self).search(cr, uid, args, offset=offset, limit=limit, 
                                           order=order, context=context, count=count)
        return res

    def create(self, cr, uid, vals, context={}):
        res = super(v_access, self).create(cr, uid, vals, context=context)
        id = res
        if id:
            obj = self.read(cr, uid, id, ['level'])
            if obj['level'] == 2:
                for perm in ['perm_read', 'perm_write', 'perm_create', 'perm_unlink', 'perm_manage']:
                    self._update_parent_perm_level_2(cr, uid, perm, id, context)
            elif obj['level'] == 3:
                for perm in ['perm_read', 'perm_write', 'perm_create', 'perm_unlink', 'perm_manage']:
                    self._update_parent_perm_level_3(cr, uid, perm, id, context)
                pass
        return res
    
    def unlink(self, cr, uid, ids, context={}):
        res = super(v_access, self).unlink(cr, uid, ids, context=context)
        self.rebuild_perm(cr, uid, context=context)
        return res
    
    def rebuild_perm(self, cr, uid, context={}):
        ids = self.search(cr, uid, []) 
        if ids:
            context.update({'force': True})
            for perm in ['perm_read', 'perm_write', 'perm_create', 'perm_unlink', 'perm_manage']:
                self._update_perm(cr, uid, ids, perm, context=context)
    
    def reload_single(self, cr, uid, group_id = False, user_id = False, object_id = False, 
                      is_create = False, context={}):
        ids = self.search(cr, uid, [('group_id', '=', group_id),
                                    ('user_id', '=', user_id), 
                                    ('object_id', '=', object_id)])
        if ids:
            self.write(cr, uid, ids[0], {'ready': True}, context=context)
        else:
            if is_create == True:
                self.create(cr, uid, {'group_id': group_id, 'user_id': user_id, 'object_id': object_id}, context=context)
        return True
    
    def reload_access(self, cr, uid, context={}):
        if self._is_reload == False:
            return False
        #
        if context.get('force_reload', False) == True:
            self._time_index = 0
        self._time_index = self._time_index - 1        
        if self._time_index > 0:
            return False
        #
        self._is_reload = False
        self._reloaded = False
        #pre update access rights
        ids = self.search(cr, uid, [])
        if ids:
            self.write(cr, uid, ids, {'ready': False})
        #check all access rights & remove all draft
        groups_id = self.pool.get('v.groups').search(cr, uid, [])
        objects_id = self.pool.get('v.objects').search(cr, uid, [('is_active', '=', True)])
        for group in self.pool.get('v.groups').read(cr, uid, groups_id, ['users']):
            group_id = group['id']
            self.reload_single(cr, uid, group_id, context=context)
            for user_id in group['users']:
                self.reload_single(cr, uid, False, user_id, context=context)
                self.reload_single(cr, uid, group_id, user_id, context=context)
                for object_id in objects_id:
                    self.reload_single(cr, uid, False, False, object_id, context=context)
                    self.reload_single(cr, uid, group_id, False, object_id, context=context)
                    self.reload_single(cr, uid, False, user_id, object_id, context=context)                    
                    self.reload_single(cr, uid, group_id, user_id, object_id, is_create=True, context=context)
        #done update access rights
        ids = self.search(cr, uid, [('ready', '=', False)])
        #reload real permission
        self.unlink(cr, uid, ids)
        #done
        self._reloaded = True
        return True
    
    def reload_all(self, cr, uid):
        self._is_reload = True
        self._time_index = self._time_max
        return True
    
    ###############################################################################################
    
    def process_access(self, cr, uid):
        if self._is_reload == True:
            self.reload_access(cr, uid, {'force_reload': True})
            return 2
        elif self._reloaded == False:
            return 1
        return 2
    
    def get_status(self, cr, uid):
        if self._is_reload == True:
            return 0
        elif self._reloaded == False:
            return 1
        return 2
    
    def change_permission(self, cr, uid, id, perm, value, data_ids, context=None):
        if not data_ids: 
            data_ids = []
        if not isinstance(data_ids, types.ListType):
            data_ids = [data_ids]
        #fix input value
        id = int(id)
        value = str(value)
        res = {}
        #check id
        ids = self.search(cr, uid, [('id', '=', id)])
        if ids:            
            self.write(cr, uid, ids[0], {perm: value}, context=context)
            update_ids = self.search(cr, uid, [('id', 'in', data_ids)])
            for obj in self.read(cr, uid, update_ids, [perm, 'real_'+perm]):
                res[obj['id']] = obj
        return res
    
    def get_group_permission(self, cr, uid, args, context=None):
        res = {}
        #init args
        for key in ['group_id', 'user_id', 'object_id']:
            has_key = False
            for arg in args:
                 if arg[0] == key:
                     has_key = True
            if has_key == False:
                args.append((key, '=', False))
        #
        ids = self.search(cr, uid, args)
        res_id = 0
        if ids: 
           res_id = ids[0] 
        else:
            vals = {}
            for arg in args:
                vals[arg[0]] = arg[2]
            new_id = self.create(cr, uid, vals, context=context)
            res_id = new_id
        res = self.read(cr, uid, res_id)            
        return res
    
    ###############################################################################################
    
v_access()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

