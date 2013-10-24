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


class res_users(osv.osv):
        
    def default_tz(self, cr, uid, context=None):
        res = self.pool.get('ir.config_parameter').get_param(cr, uid, 'vieterp.default_user_timezone', context=context)
        return res
    
    def default_lang(self, cr, uid, context=None):
        res = self.pool.get('ir.config_parameter').get_param(cr, uid, 'vieterp.default_user_language', context=context)
        return res
    
    def default_is_project_specific(self, cr, uid, context=None):
        if not context:
            context = {}
        res = context.get('is_project_specific', False)
        return res
    
    _inherit = 'res.users'
    _columns = {
        'special_group': fields.many2one('res.groups', string="Special Group"),
        'is_project_specific': fields.boolean('Chỉ dùng riêng cho dự án hiện tại?'),
        'vgroups_id': fields.many2many('v.groups', 'res_vgroups_users_rel', 'uid', 'gid', 'Groups'),
    }
    _defaults = {
        'tz': default_tz,
        'lang': default_lang,
        'is_project_specific': default_is_project_specific,
    }
    
    def create_special_group(self, cr, uid, user_ids = None, context=None):
        if not user_ids:
            return False
        if type(user_ids) != types.ListType:
            user_ids = [user_ids]
        for obj in self.read(cr, uid, user_ids, ['special_group', 'login']):
            if obj['special_group'] == False:
                #create special group
                new_group_id = self.pool.get('res.groups').create(cr, uid, {'name': str(obj['id']) + ' - ' + obj['login'],
                                                                            'users': [(6, 0, [obj['id']])],
                                                                            'special_user': obj['id']
                                                                            }, context=context)
                #update new user
                self.write(cr, uid, obj['id'], {'special_group': new_group_id}, context=context)            
        return True
    
    def update_special_group(self, cr, uid, user_ids = None, context=None):
        if not user_ids:
            return False
        if type(user_ids) != types.ListType:
            user_ids = [user_ids]
        for obj in self.read(cr, uid, user_ids, ['special_group', 'login', 'is_project_specific']):
            if obj['special_group'] == False:                
                if obj['is_project_specific'] == True:
                    self.create_special_group(cr, uid, obj['id'], context=context)
            else:
                self.pool.get('res.groups').write(cr, uid, obj['special_group'][0], 
                                                  {'name': str(obj['id']) + ' - ' + obj['login']})
        return True
    
    def write(self, cr, uid, ids, vals, context=None):
        res = super(res_users, self).write(cr, uid, ids, vals, context=context)
        self.update_special_group(cr, uid, ids, context=context)
        if vals.has_key('vgroups_id'):
            self.pool.get('v.access').reload_all(cr, uid)
        return res
    
    def create(self, cr, uid, vals, context=None):
        res = super(res_users, self).create(cr, uid, vals, context=context)
        new_uid = res
        if new_uid:
            self.create_special_group(cr, uid, new_uid, context=context)        
        return res
    
    def unlink(self, cr, uid, ids, context=None):        
        res = super(res_users, self).unlink(cr, uid, ids, context=context)
        self.pool.get('v.access').reaload_all(cr, uid)
        return res
    
#    def reset_all_group(self, cr, uid, context=None):
#        ids = self.search(cr, uid, [])
#        if ids:
#            self.reset_group(cr, uid, ids, context=context)
#    
#    def reset_group(self, cr, uid, ids, context=None):
#        for obj in self.read(cr, uid, ids, ['is_project_specific', 'special_group', 'groups_id']):
#            if not obj['is_project_specific']:
#                continue
#            if not obj['special_group']:
#                continue
#            self.pool.get('res.users').write(cr, uid, obj['id'], 
#                                             {'groups_id': [(6, 0, [obj['special_group'][0]])]})
#            self.pool.get('res.groups').write(cr, uid, obj['special_group'][0],
#                                              {'users': [(6, 0, [obj['id']])]})
    
res_users()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
