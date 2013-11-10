# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode
import types
import json

class pq_redis(osv.osv):
    
    _name = 'pq.redis'
    _description = 'Redis'
    _columns = {
        'name': fields.char('Name', size=128),

        'key': fields.char('Key', size=128),
        'value': fields.char('Value', size=1024000),
        
        'create_date': fields.datetime('Ngày giờ tạo', readonly=True),
        'user_id': fields.many2one('res.users', string="Người tạo",readonly=True),
    }
    _defaults = {
        'user_id': lambda self, cr, uid, context=None: uid,
    }

    def dumps_value(self, val):
        return json.dumps(val)

    def loads_value(self, val):
        return json.loads(val)

    def set(self, cr, uid, key, value):
        ids = self.search(cr, uid, [('key', '=', key)])
        if not ids: 
            self.create(cr, uid, {
                'key': key,
                'value': self.dumps_value(value)
            })
        else:
            self.write(cr, uid, ids, {
                'value': self.dumps_value(value)
            })

    def get(self, cr, uid, key):
        ids = self.search(cr, uid, [('key', '=', key)])
        if not ids:
            return None
        res = None
        try:
            res = self.loads_value(self.read(cr, uid, ids[0], ['value'])['value'])
        except:
            pass
        return res

    def clear(self, cr, uid, key):
        ids = self.search(cr, uid, [('key', '=', key)])
        if not ids:
            return False
        return self.unlink(cr, uid, ids)

    def clear_all(self, cr, uid):
        ids = self.search(cr, uid, [])
        return self.unlink(cr, uid, ids)

    
pq_redis()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

