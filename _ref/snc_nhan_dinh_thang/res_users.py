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
    
    _inherit = 'res.users'
    _columns = {
        'nhan_dinh_tuan': fields.many2many('snc.nhan.dinh.tuan.setup', 'snc_nhan_dinh_tuan_setup_res_users_rel', 'uid', 'nid', 'Nhận định tuần'),
    }
    _defaults = {
        
    }
    
res_users()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
