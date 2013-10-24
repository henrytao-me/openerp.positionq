# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.osv.fields import datetime as datetime_field
from openerp.tools.translate import _
import logging
import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT 
from unidecode import unidecode
import types
from calendar import isleap

class vieterp_utils(osv.osv_memory):
    
    def get_alias_from_string(self, cr, uid, raw_string, context=None):
        if not context:
            context = {}
        return unidecode(raw_string).replace(' ', '-').replace(':', '-').replace('.', '').replace('%', '').lower()
    
    def get_datetime_format_from_datetime(self, cr, uid, datetime_str_in_UTC, format='%H:%M:%S %d/%m/%Y', context=None):
        if not context:
            context = {}
        datetime_UTC = datetime.datetime.strptime(datetime_str_in_UTC, DEFAULT_SERVER_DATETIME_FORMAT)
        datetime_in_user_timezone = datetime_field.context_timestamp(cr, uid, datetime_UTC, context=context)
        return datetime_in_user_timezone.strftime(format)    

    def get_date_format_from_date(self, cr, uid, datetime_str_in_UTC, format='%d/%m/%Y', context=None):        
        if not context:
            context = {}            
        datetime_UTC = datetime.datetime.strptime(datetime_str_in_UTC, DEFAULT_SERVER_DATE_FORMAT)
        datetime_in_user_timezone = datetime_field.context_timestamp(cr, uid, datetime_UTC, context=context)
        return datetime_in_user_timezone.strftime(format)

    def get_date_format_from_datetime(self, cr, uid, datetime_str_in_UTC, format=DEFAULT_SERVER_DATE_FORMAT, context=None):        
        if not context:
            context = {}        
        datetime_UTC = datetime.datetime.strptime(datetime_str_in_UTC, DEFAULT_SERVER_DATETIME_FORMAT)
        datetime_in_user_timezone = datetime_field.context_timestamp(cr, uid, datetime_UTC, context=context)
        return datetime_in_user_timezone.strftime(format)

    def get_model_column_info(self, cr, uid, model, column_name):
        # convert column_name to standard
        is_list = True
        if not isinstance(column_name, types.ListType):
            is_list = False
            column_name = [column_name]
        res = {}
        for column in column_name:
            res.update({
                column: {
                    'type': ''
                } 
            })
        try:
            obj = self.pool.get(model)            
            for column in column_name:
                tmp = obj._columns.get(column, None)
                if tmp:
                    res[column]['type'] = tmp._type
                    if tmp._type == 'many2one':
                        res[column].update({
                            'obj': tmp._obj
                        })
                    elif tmp._type == 'one2one' or tmp._type == 'one2many':
                        res[column].update({
                            'obj': tmp._obj,
                            'fields_id': tmp._fields_id
                        })
            if is_list == False:
                for tmp in res:
                    return res[tmp]
        except:
            print 'Error: vieterp_utils - get_model_column_type'
        return res

    def get_this_monday(self, cr, uid, date):
        res = date
        not_datetime = False
        if not isinstance(date, datetime.datetime):
            not_datetime = True
            date = datetime.datetime.strptime(date, DEFAULT_SERVER_DATE_FORMAT)
        timedelta = datetime.timedelta((int(date.strftime('%w')) - 1 + 7) % 7)
        date = date - timedelta
        if not_datetime:
            date = date.strftime(DEFAULT_SERVER_DATE_FORMAT)
        res = date
        return res

    def get_this_friday(self, cr, uid, date):
        res = date
        not_datetime = False
        if not isinstance(date, datetime.datetime):
            not_datetime = True
            date = datetime.datetime.strptime(date, DEFAULT_SERVER_DATE_FORMAT)
        timedelta = datetime.timedelta((int(date.strftime('%w')) - 1 + 7) % 7)
        date = date - timedelta
        timedelta = datetime.timedelta(4)
        date = date + timedelta
        if not_datetime:
            date = date.strftime(DEFAULT_SERVER_DATE_FORMAT)
        res = date
        return res

    def get_this_month(self, cr, uid, date):
        res = date
        not_datetime = False
        if not isinstance(date, datetime.datetime):
            not_datetime = True
            date = datetime.datetime.strptime(date, DEFAULT_SERVER_DATE_FORMAT)
        date = date.strftime('%Y-%m-1')
        date = datetime.datetime.strptime(date, DEFAULT_SERVER_DATE_FORMAT)
        if not_datetime:
            date = date.strftime(DEFAULT_SERVER_DATE_FORMAT)
        res = date
        return res
    
    def get_last_month(self, cr, uid, date):
        res = date
        not_datetime = False
        if not isinstance(date, datetime.datetime):
            not_datetime = True
            date = datetime.datetime.strptime(date, DEFAULT_SERVER_DATE_FORMAT)
        date = self.get_this_month(cr, uid, date) - datetime.timedelta(35)
        date = self.get_this_month(cr, uid, date)
        if not_datetime:
            date = date.strftime(DEFAULT_SERVER_DATE_FORMAT)
        return res

    def get_this_quarter(self, cr, uid, date):
        res = date
        not_datetime = False
        if not isinstance(date, datetime.datetime):
            not_datetime = True
            date = datetime.datetime.strptime(date, DEFAULT_SERVER_DATE_FORMAT)
        month = int(date.strftime('%m'))
        month = (month - 1) / 3 + 1
        month = (month - 1) * 3 + 1
        date = date.strftime('%Y-' + str(month) + '-1')
        date = datetime.datetime.strptime(date, DEFAULT_SERVER_DATE_FORMAT)
        if not_datetime:
            date = date.strftime(DEFAULT_SERVER_DATE_FORMAT)
        res = date        
        return res

    def get_now(self, cr, uid):       
        now = datetime.datetime.now()        
        now = datetime_field.context_timestamp(cr, uid, now)
        return now

    def get_day(self, cr, uid, date, type=DEFAULT_SERVER_DATE_FORMAT):        
        res = 1
        if not isinstance(date, datetime.datetime):
            date = datetime.datetime.strptime(date, type)
        res = int(date.strftime('%w')) + 1
        return res

    _name = 'vieterp.utils'
    _description = 'Module utils'
    _columns = {
    }
    _defaults = {
    }
vieterp_utils()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

