#############################################
# orm_unlink
#############################################

from openerp.osv.orm import BaseModel
from openerp import SUPERUSER_ID

def unlink(self, cr, uid, ids, context=None, force=False):
    """
    Delete records with given ids

    :param cr: database cursor
    :param uid: current user id
    :param ids: id or list of ids
    :param context: (optional) context arguments, like lang, time zone
    :return: True
    :raise AccessError: * if user has no unlink rights on the requested object
                        * if user tries to bypass access rules for unlink on the requested object
    :raise UserError: if the record is default property for other records

    """
    if not ids:
        return True
    if isinstance(ids, (int, long)):
        ids = [ids]

    result_store = self._store_get_values(cr, uid, ids, self._all_columns.keys(), context)

    self._check_concurrency(cr, ids, context)

    self.check_access_rights(cr, uid, 'unlink')

    ir_property = self.pool.get('ir.property')

    # Check if the records are used as default properties.
    domain = [('res_id', '=', False),
              ('value_reference', 'in', ['%s,%s' % (self._name, i) for i in ids]),
             ]
    if ir_property.search(cr, uid, domain, context=context):
        raise except_orm(_('Error'), _('Unable to delete this document because it is used as a default property'))

    # Delete the records' properties.
    property_ids = ir_property.search(cr, uid, [('res_id', 'in', ['%s,%s' % (self._name, i) for i in ids])], context=context)
    ir_property.unlink(cr, uid, property_ids, context=context)

    self._workflow_trigger(cr, uid, ids, 'trg_delete', context=context)

    self.check_access_rule(cr, uid, ids, 'unlink', context=context)
    pool_model_data = self.pool.get('ir.model.data')
    ir_values_obj = self.pool.get('ir.values')
    for sub_ids in cr.split_for_in_conditions(ids):
        cr.execute('delete from ' + self._table + ' ' \
                   'where id IN %s', (sub_ids,))

        # Removing the ir_model_data reference if the record being deleted is a record created by xml/csv file,
        # as these are not connected with real database foreign keys, and would be dangling references.
        # Note: following steps performed as admin to avoid access rights restrictions, and with no context
        #       to avoid possible side-effects during admin calls.
        # Step 1. Calling unlink of ir_model_data only for the affected IDS
        reference_ids = pool_model_data.search(cr, SUPERUSER_ID, [('res_id','in',list(sub_ids)),('model','=',self._name)])
        # Step 2. Marching towards the real deletion of referenced records
        if reference_ids:
            pool_model_data.unlink(cr, SUPERUSER_ID, reference_ids)

        # For the same reason, removing the record relevant to ir_values
        ir_value_ids = ir_values_obj.search(cr, uid,
                ['|',('value','in',['%s,%s' % (self._name, sid) for sid in sub_ids]),'&',('res_id','in',list(sub_ids)),('model','=',self._name)],
                context=context)
        if ir_value_ids:
            ir_values_obj.unlink(cr, uid, ir_value_ids, context=context)

    for order, object, store_ids, fields in result_store:
        if object != self._name or force == True:      ###################fix bug
            obj = self.pool.get(object)
            cr.execute('select id from '+obj._table+' where id IN %s', (tuple(store_ids),))
            rids = map(lambda x: x[0], cr.fetchall())
            if rids:
                obj._store_set_values(cr, uid, rids, fields, context)

    return True

BaseModel.unlink = unlink