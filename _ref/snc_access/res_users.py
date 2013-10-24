# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode
import types

from functools import partial
import logging
from lxml import etree
from lxml.builder import E

import openerp
from openerp import SUPERUSER_ID
from openerp import pooler, tools
import openerp.exceptions
from openerp.osv.orm import browse_record

class res_users(osv.osv):
    
    def def_is_public(self, cr, uid, context={}):
        res = context.get('is_public', False)
        return res
    
    _inherit = 'res.users'
    _columns = {
        'is_public': fields.boolean('Public User')
    }
    _defaults = {        
        'is_public': def_is_public
    }
    _order = "is_public desc, login"
    
res_users()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
