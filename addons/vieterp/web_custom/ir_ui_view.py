# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################

import logging
from lxml import etree
import os

from openerp import tools
from openerp.osv import fields,osv
from openerp.tools import graph
from openerp.tools.safe_eval import safe_eval as eval
from openerp.tools.view_validation import valid_view

_logger = logging.getLogger(__name__)

class view(osv.osv):

    _inherit = 'ir.ui.view'
    
    def _type_field(self, cr, uid, ids, name, args, context=None):
        res = super(view, self)._type_field(cr, uid, ids, name, args, context=context)
        return res
    
    _columns = {
        'type': fields.function(_type_field, type='selection', selection=[
            ('custom','Custom'),
            ('tree','Tree'),
            ('form','Form'),
            ('mdx','mdx'),
            ('graph', 'Graph'),
            ('calendar', 'Calendar'),
            ('diagram','Diagram'),
            ('gantt', 'Gantt'),
            ('kanban', 'Kanban'),
            ('search','Search')], string='View Type', required=True, select=True, store=True),
    }
    
view()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

