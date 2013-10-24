# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode
import types

class mymod(osv.osv):
    
    _name = 'mymod'
    _description = 'My Mod'
    _columns = {
        'name': fields.char('Tên tham số', size=128, required=True),
        'state': fields.selection([
            ('new','New'),
            ('assigned','Assigned'),
            ('negotiation','Negotiation'),
            ('won','Won'),
            ('lost','Lost')], 'Stage', readonly=True),
    }
    _defaults = {
        'state': lambda *x: 'new'
    }
    
    def mymod_new(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, { 'state' : 'new' })
        return True

    def mymod_assigned(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, { 'state' : 'assigned' })
        return True
    
    def mymod_negotiation(self, cr, uid, ids):
        self.write(cr, uid, ids, { 'state' : 'negotiation' })
        return True
    
    def mymod_won(self, cr, uid, ids):
        self.write(cr, uid, ids, { 'state' : 'won' })
        return True
    
    def mymod_lost(self, cr, uid, ids):
        self.write(cr, uid, ids, { 'state' : 'lost' })
        return True
    
    def act_mymod_assigned_2(self, cr, uid, ids, context=None):        
        self.signal_mymod_assigned(cr, uid, ids)        
        return True
    
mymod()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

