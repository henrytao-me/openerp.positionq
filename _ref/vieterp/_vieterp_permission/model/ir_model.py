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


class ir_model(osv.osv):
    
    _rec_name= "model"
    _inherit = 'ir.model'
    _columns = {
        'is_project_specific': fields.boolean('Chỉ dùng riêng cho dự án hiện tại?'), #should be removed
        'v_object': fields.many2many('v.objects', 'res_vobjects_irmodel_rel', 'mid', 'oid', 'Đối tượng'),
    }
    _defaults = {
        
    }
    
ir_model()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: