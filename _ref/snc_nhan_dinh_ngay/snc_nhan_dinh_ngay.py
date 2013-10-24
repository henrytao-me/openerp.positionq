# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode
import math 

class snc_nhan_dinh_ngay(osv.osv):
       
    def function_update_date(self, cr, uid, ids, fields, args, context=None):
        res = {}
        for id in ids:
            res[id] = datetime.datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        return res
    
    def function_time_format(self, cr, uid, ids, fields, args, context={}):
        res = {}
        for obj in self.read(cr, uid, ids, ['time']):
            time = datetime.datetime.strptime(obj['time'], DEFAULT_SERVER_DATETIME_FORMAT)
            time = datetime_field.context_timestamp(cr, uid, time, context=context)
            res[obj['id']] = time.strftime(DEFAULT_SERVER_DATE_FORMAT)            
        return res
    
    def function_calculate(self, cr, uid, ids, fields, args, context={}):
        res = {}
        for obj in self.read(cr, uid, ids, ['time_format', 'high', 'low', 'trend']):
            vals = {
                'real_high': 0,
                'real_low': 0,
                'real_trend': '0',
                
                'diff_high_abs': 0,
                'diff_high_percent': 0,
                'diff_low_abs': 0,
                'diff_low_percent': 0,
                
                'diff_trend': 0,
                
                'diff_abs': 0,
                'diff_percent': 0
            }
            #
            from_date = obj['time_format']            
            #
            lme = self.pool.get('snc.lme').get_info(cr, uid, type="ngay", arg="close", from_date=from_date)
            if lme:
                vals.update({
                    'real_high': lme.get('high', 0),
                    'real_low': lme.get('low', 0),
                    'real_trend': lme.get('trend', '0'),
                })
            vals.update({
                'diff_high_abs': math.fabs(vals.get('real_high') - obj.get('high')),
                'diff_low_abs': math.fabs(vals.get('real_low') - obj.get('low')), 
            })
            if vals.get('real_high', 0) != 0:
                vals['diff_high_percent'] = math.fabs(float(((obj.get('high') / vals.get('real_high') - 1) * 100)))                 
            if vals.get('real_low', 0) != 0:
                vals['diff_low_percent'] = math.fabs(float(((obj.get('low') / vals.get('real_low') - 1) * 100)))
            #trend
            if vals.get('real_trend') != obj.get('trend'):
                vals['diff_trend'] = 1
            #diff abs, percent
            vals.update({
                'diff_abs': (vals.get('diff_high_abs') + vals.get('diff_low_abs', 0)) / 2,
                'diff_percent': (vals.get('diff_high_percent') + vals.get('diff_low_percent', 0)) / 2
            })
            #
            res[obj['id']] = vals
        return res
    
    _name = 'snc.nhan.dinh.ngay'
    _description = 'Nhan Dinh Ngay'
    _columns = {
        'name': fields.char('Tiêu đề', size=8),
        
        'time': fields.datetime('Thời gian nhận định'),
        'time_format': fields.function(function_time_format, method=True, string='Thời gian nhận định',
                                              type='date', store=True),
        
        'high': fields.float('Cao nhất', digits=(16,2), required=True),
        'low': fields.float('Thấp nhất', digits=(16,2), required=True),
        'trend': fields.selection([('1','Tăng'),('-1','Giảm')], 'Xu hướng', required=True),        
                
        'real_high': fields.function(function_calculate, method=True, string="Cao nhất",
                                      type="float", digits=(16,2), multi="function_calculate"),
        'real_low': fields.function(function_calculate, method=True, string="Thấp nhất",
                                      type="float", digits=(16,2), multi="function_calculate"),
        'real_trend': fields.function(function_calculate, method=True, string="Xu hướng",
                                      type="selection", multi="function_calculate",
                                      selection=[('1', 'Tăng'),
                                                 ('0', 'Không xác định'),
                                                 ('-1', 'Giảm')]),
        
        'diff_high_abs': fields.function(function_calculate, method=True, string='SS ||', 
                                        type="float", digits=(16,2), multi="function_calculate"),
        'diff_high_percent': fields.function(function_calculate, method=True, string='SS %', 
                                        type="float", digits=(16,2), multi="function_calculate"),
        
        'diff_low_abs': fields.function(function_calculate, method=True, string='SS ||', 
                                        type="float", digits=(16,2), multi="function_calculate"),
        'diff_low_percent': fields.function(function_calculate, method=True, string='SS %', 
                                        type="float", digits=(16,2), multi="function_calculate"),
            
        'diff_trend': fields.function(function_calculate, method=True, string='Xu hướng', 
                                        type="integer", multi="function_calculate"),
                
        'diff_abs': fields.function(function_calculate, method=True, string='SS ||', 
                                        type="float", digits=(16,2), multi="function_calculate"),
        'diff_percent': fields.function(function_calculate, method=True, string='SS %', 
                                        type="float", digits=(16,2), multi="function_calculate"),
        
        'user_id': fields.many2one('res.users', string="Người nhận định", readonly=True),
        'create_date': fields.datetime('Ngày giờ tạo', readonly=True),
        'update_date': fields.function(function_update_date, method= True, string='Ngày cập nhật',
                                       store=True, type ='datetime'),
    }
    _defaults = {
        'name': lambda *x: ' ',
        'user_id': lambda self, cr, uid, context=None: uid,
        'time': lambda *x: datetime.datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
    }
    _order = "time_format desc, update_date desc"
    _num_of_date = 5
    
    def search(self, cr, uid, args, offset=0, limit=None, order=None, context={}, count=False):
        if context.get('read.user_id', '') == 'current':
            args.append(('user_id', '=', uid))
        res = super(snc_nhan_dinh_ngay, self).search(cr, uid, args, offset=offset, 
                                                limit=limit, order=order, context=context, count=count)
        return res
    
    def create(self, cr, uid, vals, context=None):
        if not context:
            context = {}
        context.update({'raise': True})
        self.pool.get('snc.nhan.dinh.ngay.setup').check_state_available(cr, uid, context=context)
        #check re-create
        now = self.pool.get('vieterp.utils').get_now(cr, uid)
        now = now.strftime(DEFAULT_SERVER_DATE_FORMAT)
        
        if vals.get('time'):
            t = ''
            try:
                t = datetime.datetime.strptime(vals['time'], DEFAULT_SERVER_DATETIME_FORMAT)
            except:
                t = datetime.datetime.strptime(vals['time'], DEFAULT_SERVER_DATE_FORMAT)
            t = datetime_field.context_timestamp(cr, uid, t)
            t = t.strftime(DEFAULT_SERVER_DATE_FORMAT)
            if t < now:         
                raise osv.except_osv(_('Cảnh báo!'), _('Không được tạo lại nhận định quá khứ.'))
        #start                    
        res = super(snc_nhan_dinh_ngay, self).create(cr, uid, vals, context=None)
        return res
    
    def write(self, cr, uid, ids, vals, context=None):
        if not context:
            context = {}
        context.update({'raise': True})
        self.pool.get('snc.nhan.dinh.ngay.setup').check_state_available(cr, uid, context=context)
        #check re-write
        now = self.pool.get('vieterp.utils').get_now(cr, uid)
        now = now.strftime(DEFAULT_SERVER_DATE_FORMAT)
        for obj in self.read(cr, uid, ids, ['time_format']):
            if obj['time_format'] < now:
                raise osv.except_osv(_('Cảnh báo!'), _('Không được thay đổi nhận định quá khứ.'))
        #start
        res = super(snc_nhan_dinh_ngay, self).write(cr, uid, ids, vals, context=context)
        return res
        
    def unlink(self, cr, uid, ids, context=None):
        if not context:
            context = {}
        context.update({'raise': True})
        self.pool.get('snc.nhan.dinh.ngay.setup').check_state_available(cr, uid, context=context)
        #check re-unlink
        now = self.pool.get('vieterp.utils').get_now(cr, uid)
        now = now.strftime(DEFAULT_SERVER_DATE_FORMAT)
        for obj in self.read(cr, uid, ids, ['time_format']):
            if obj['time_format'] < now:
                raise osv.except_osv(_('Cảnh báo!'), _('Không được hủy nhận định quá khứ.'))
        #start
        res = super(snc_nhan_dinh_ngay, self).unlink(cr, uid, ids, context=context)
        return res
    
    def get_from_date_to_date(self, cr, uid, from_date, to_date=None, context={}):
        if not to_date: 
            to_date = from_date
        #
        from_date = self.pool.get('vieterp.utils').get_this_monday(cr, uid, from_date)
        to_date = self.pool.get('vieterp.utils').get_this_friday(cr, uid, to_date)
        #
        return from_date, to_date
    
    def get_except_date(self, cr, uid, from_date, to_date):
        res = []
        info = self.pool.get('snc.nhan.dinh.ngay.setup').get_info(cr, uid, ['exception'])        
        ids = self.pool.get('snc.nhan.dinh.ngay.exception').search(cr, uid, [('id', 'in', info.get('exception', [])),
                                                                             ('date', '>=', from_date),
                                                                             ('date', '<=', to_date)])
        if ids:
            for obj in self.pool.get('snc.nhan.dinh.ngay.exception').read(cr, uid, ids, ['date']):
                res.append(obj['date'])
        return res
    
    def get_users_from_range(self, cr, uid, from_date, to_date):
        res = {}
        except_date = self.get_except_date(cr, uid, from_date, to_date)
        ids = self.search(cr, uid, [('time_format', '>=', from_date),
                                    ('time_format', '<=', to_date),
                                    ('time_format', 'not in', except_date)],
                          order="create_date desc")
        if ids:
            res = {}
            for obj in self.read(cr, uid, ids, ['user_id']):
                res.update({
                    obj['user_id'][0]: obj['user_id']
                })
            res = res.values()
            res.sort(key=lambda tup: tup[1])
        return res
    
    def thong_ke(self, cr, uid, from_date, context={}):
        res = {}
        from_date, to_date = self.get_from_date_to_date(cr, uid, from_date, context=context)
        #get except date        
        except_date = self.get_except_date(cr, uid, from_date, to_date)
        #get data
        num_of_date = self._num_of_date - len(except_date)
        ids = self.search(cr, uid, [('time_format', '>=', from_date),
                                    ('time_format', '<=', to_date),
                                    ('time_format', 'not in', except_date)])
        data = {}
        data_log = {}
        for obj in self.read(cr, uid, ids, ['time_format', 'user_id', 
                                            'diff_abs', 'diff_percent', 'diff_trend']):
            if not data_log.get(obj['time_format']):
                data_log.update({obj['time_format']: {}})
            if not data_log.get(obj['time_format'], {}).get(obj['user_id'][0]):
                data_log[obj['time_format']].update({obj['user_id'][0]: True})
            else:
                continue
            
            if not data.get(obj['user_id'][0]):
                data.update({obj['user_id'][0]: {
                    'diff_abs': 0,
                    'diff_percent': 0,
                    'diff_trend': 0,
                    'n': 0
                }})
            data[obj['user_id'][0]].update({
                'diff_abs': data[obj['user_id'][0]].get('diff_abs', 0) + obj['diff_abs'],
                'diff_percent': data[obj['user_id'][0]].get('diff_percent', 0) + obj['diff_percent'],
                'diff_trend': data[obj['user_id'][0]].get('diff_trend', 0) + int(obj['diff_trend']),
                'count': data[obj['user_id'][0]].get('count', 0) + 1,
                'n': num_of_date
            })
        #standard index
        for user_id in data.copy():
            data[user_id].update({
                'diff_abs': round(data[user_id].get('diff_abs') / data[user_id].get('count'), 2),
                'diff_percent': round(data[user_id].get('diff_percent') / data[user_id].get('count'), 2),
                'diff_trend': round(1.0 * data[user_id].get('diff_trend') * data[user_id].get('n') / data[user_id].get('count'), 2),
            })
        res = data
        #return
        return res
    
    def thong_ke_chi_tiet(self, cr, uid, from_date, context={}):
        res = {}
        ids = self.search(cr, uid, [('time_format', '=', from_date)])
        if ids:
            for obj in self.read(cr, uid, ids, ['user_id', 'high', 'low', 'trend',
                                                'diff_high_abs', 'diff_high_percent',
                                                'diff_low_abs', 'diff_low_percent', 'diff_trend']):
                if not res.get(obj['user_id'][0]):
                    res.update({
                        obj['user_id'][0]: obj
                    })
        return res
        
snc_nhan_dinh_ngay()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

