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

# Extension of res.groups and res.users for the special groups view in the users
# form.  This extension presents groups with selection and boolean widgets:
# - Groups are shown by application, with boolean and/or selection fields.
#   Selection fields typically defines a role "Name" for the given application.
# - Uncategorized groups are presented as boolean fields and grouped in a
#   section "Others".
#
# The user form view is modified by an inherited view (base.user_groups_view);
# the inherited view replaces the field 'groups_id' by a set of reified group
# fields (boolean or selection fields).  The arch of that view is regenerated
# each time groups are changed.
#
# Naming conventions for reified groups fields:
# - boolean field 'in_group_ID' is True iff
#       ID is in 'groups_id'
# - boolean field 'in_groups_ID1_..._IDk' is True iff
#       any of ID1, ..., IDk is in 'groups_id'
# - selection field 'sel_groups_ID1_..._IDk' is ID iff
#       ID is in 'groups_id' and ID is maximal in the set {ID1, ..., IDk}

def name_boolean_group(id): return 'in_group_' + str(id)
def name_boolean_groups(ids): return 'in_groups_' + '_'.join(map(str, ids))
def name_selection_groups(ids): return 'sel_groups_' + '_'.join(map(str, ids))

def is_boolean_group(name): return name.startswith('in_group_')
def is_boolean_groups(name): return name.startswith('in_groups_')
def is_selection_groups(name): return name.startswith('sel_groups_')
def is_reified_group(name):
    return is_boolean_group(name) or is_boolean_groups(name) or is_selection_groups(name)

def get_boolean_group(name): return int(name[9:])
def get_boolean_groups(name): return map(int, name[10:].split('_'))
def get_selection_groups(name): return map(int, name[11:].split('_'))

def partition(f, xs):
    "return a pair equivalent to (filter(f, xs), filter(lambda x: not f(x), xs))"
    yes, nos = [], []
    for x in xs:
        (yes if f(x) else nos).append(x)
    return yes, nos



class groups_view(osv.osv):
    _inherit = 'res.groups'

    def create(self, cr, uid, values, context=None):
        res = super(groups_view, self).create(cr, uid, values, context)
        self.update_user_groups_view_snc_access(cr, uid, context)
        return res

    def write(self, cr, uid, ids, values, context=None):
        res = super(groups_view, self).write(cr, uid, ids, values, context)
        self.update_user_groups_view_snc_access(cr, uid, context)
        return res

    def unlink(self, cr, uid, ids, context=None):
        res = super(groups_view, self).unlink(cr, uid, ids, context)
        self.update_user_groups_view_snc_access(cr, uid, context)
        return res

    def update_user_groups_view_snc_access(self, cr, uid, context=None):
        # the view with id 'base.user_groups_view' inherits the user form view,
        # and introduces the reified group fields
        view = self.get_user_groups_view_snc_access(cr, uid, context)
        if view:
            xml1, xml2 = [], []
            xml1.append(E.separator(string=_('Application'), colspan="4"))
            for app, kind, gs in self.get_groups_by_application_snc_access(cr, uid, context):
                # hide groups in category 'Hidden' (except to group_no_one)
                attrs = {'groups': 'base.group_no_one'} if app and app.xml_id == 'base.module_category_hidden' else {}
                if kind == 'selection':
                    # application name with a selection field
                    field_name = name_selection_groups(map(int, gs))
                    xml1.append(E.field(name=field_name, **attrs))
                    xml1.append(E.newline())
                else:
                    # application separator with boolean fields
                    app_name = app and app.name or _('Other')
                    xml2.append(E.separator(string=app_name, colspan="4", **attrs))
                    for g in gs:
                        field_name = name_boolean_group(g.id)
                        xml2.append(E.field(name=field_name, **attrs))

            xml = E.field(*(xml1 + xml2), name="groups_id", position="replace")
            xml.addprevious(etree.Comment("GENERATED AUTOMATICALLY BY GROUPS"))
            xml_content = etree.tostring(xml, pretty_print=True, xml_declaration=True, encoding="utf-8")
            view.write({'arch': xml_content})
        return True

    def get_user_groups_view_snc_access(self, cr, uid, context=None):
        try:
            view = self.pool.get('ir.model.data').get_object(cr, SUPERUSER_ID, 'snc_access', 'user_groups_view', context)
            assert view and view._table_name == 'ir.ui.view'
        except Exception:
            view = False
        return view
    
    def get_application_groups_snc_access(self, cr, uid, domain=None, context=None):
        domain = [('is_public', '=', True)]
        return self.search(cr, uid, domain or [])

    def get_groups_by_application_snc_access(self, cr, uid, context=None):
        """ return all groups classified by application (module category), as a list of pairs:
                [(app, kind, [group, ...]), ...],
            where app and group are browse records, and kind is either 'boolean' or 'selection'.
            Applications are given in sequence order.  If kind is 'selection', the groups are
            given in reverse implication order.
        """
        def linearized(gs):
            gs = set(gs)
            # determine sequence order: a group should appear after its implied groups
            order = dict.fromkeys(gs, 0)
            for g in gs:
                for h in gs.intersection(g.trans_implied_ids):
                    order[h] -= 1
            # check whether order is total, i.e., sequence orders are distinct
            if len(set(order.itervalues())) == len(gs):
                return sorted(gs, key=lambda g: order[g])
            return None

        # classify all groups by application
        gids = self.get_application_groups_snc_access(cr, uid, context=context)
        by_app, others = {}, []
        for g in self.browse(cr, uid, gids, context):
            if g.category_id:
                by_app.setdefault(g.category_id, []).append(g)
            else:
                others.append(g)
        # build the result
        res = []
        apps = sorted(by_app.iterkeys(), key=lambda a: a.name or 0)
        #
        for app in apps:
            gs = linearized(by_app[app])
            if gs:
                res.append([app, 'selection', gs])
            else:
                res.append([app, 'boolean', by_app[app]])
        if others:
            res.append([False, 'boolean', others])
        #sort
        for ritem in res:
            if ritem[1] == 'boolean':
                r1, r2 = [], []
                index = 1
                n = int((len(ritem[2]) - 1) / 2) + 1
                gs = {}
                for g in sorted(ritem[2], key=lambda a: a.name or 0):
                    gs[index] = g
                    index += 1
                i = 1
                ritem[2] = []
                while i <= n:
                    ritem[2].append(gs[i])
                    if gs.get(n + i):
                        ritem[2].append(gs[n + i])
                    i += 1
        #
        return res
    
groups_view()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

