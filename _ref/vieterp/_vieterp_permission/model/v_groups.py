# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode

class v_groups(osv.osv):

    _name = 'v.groups'
    _description = 'V Groups'    
    _columns = {        
        'name': fields.char('Name', size=64, required=True, translate=True),
        'users': fields.many2many('res.users', 'res_vgroups_users_rel', 'gid', 'uid', 'Users'),
    }
    _defaults = {
        
    }
    
    def create(self, cr, uid, vals, context=None):
        res = super(v_groups, self).create(cr, uid, vals, context=context)
        if vals.has_key('users'):
            self.pool.get('v.access').reload_all(cr, uid)
        return res
    
    def write(self, cr, uid, ids, vals, context=None):
        res = super(v_groups, self).write(cr, uid, ids, vals, context=context)
        if vals.has_key('users'):
            self.pool.get('v.access').reload_all(cr, uid)
        return res
    
    def unlink(self, cr, uid, ids, context=None):
        res = super(v_groups, self).unlink(cr, uid, ids, context=context)
        self.pool.get('v.access').reload_all(cr, uid)
        return res
    
#    def get_all_user(self, cr, uid, groups_id=[]):
#        args = []
#        if groups_id:
#            args.append(('id', 'in', groups_id))
#        res = {}
#        ids = self.search(cr, uid, args)
#        for obj in self.read(cr, uid, ids, ['users']):
#            for user_id in obj['users']:
#                res[user_id] = True
#        return res.keys()
    
v_groups()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

