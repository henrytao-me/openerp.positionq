# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode
import math 

class snc_nhan_dinh_ngay_setup(osv.osv):
    
    def function_dcxh(self, cr, uid, ids, fields, args, context=None):
        res = {}
        for obj in self.read(cr, uid, ids, ['cal_from', 'cal_to']):
            cal_from = self.pool.get('vieterp.utils').get_this_monday(cr, uid, obj['cal_from'])
            cal_to = self.pool.get('vieterp.utils').get_this_friday(cr, uid, obj['cal_to'])            
            info = self.pool.get('snc.nhan.dinh.ngay.setup').get_info(cr, uid, ['exception'])        
            tmp_ids = self.pool.get('snc.nhan.dinh.ngay.exception').search(cr, uid, [('id', 'in', info.get('exception', [])),
                                                                                     ('date', '>=', cal_from),
                                                                                     ('date', '<=', cal_to)])
            cal_from = datetime.datetime.strptime(cal_from, DEFAULT_SERVER_DATE_FORMAT)
            cal_to = datetime.datetime.strptime(cal_to, DEFAULT_SERVER_DATE_FORMAT)
            delta = cal_to - cal_from
            res[obj['id']] = int(int(delta.days + 3) / 7) * 5 - len(tmp_ids)
        return res
    
    def float_to_time(self, val):
        res = val
        h = int(val)
        m = int((val - h) * 60)
        h = str(h) if h > 9 else '0' + str(h)
        m = str(m) if m > 9 else '0' + str(m)
        res = ':'.join([h, m])
        return res
    
    def function_time_str(self, cr, uid, ids, fields, args, context=None):
        res = {}
        for obj in self.read(cr, uid, ids, ['from_time', 'to_time']):
            #
            from_time = self.float_to_time(obj['from_time'])
            to_time = self.float_to_time(obj['to_time'])
            #
            res[obj['id']] = {
                'from_time_str': from_time,
                'to_time_str': to_time
            }
        return res
    
    _name = 'snc.nhan.dinh.ngay.setup'
    _description = 'Thiet Lap Nhan Dinh Ngay'
    _columns = {
        'name': fields.char('Name', size=64),
        
        'state': fields.selection([('close', 'Đóng'), 
                                   ('open', 'Mở'),
                                   ('auto', 'Tự động')], 'Trạng thái'),
        'from_time': fields.float('Thời gian mở', digits=(16,2)),                
        'to_time': fields.float('Thời gian đóng', digits=(16,2)),
        
        'from_time_str': fields.function(function_time_str, method=True, string="from_time", 
                                         type="char", size=16, multi="function_time_str"),
        'to_time_str': fields.function(function_time_str, method=True, string="to_time", 
                                         type="char", size=16, multi="function_time_str"),
        
        'cal_from': fields.date('Từ ngày'),
        'cal_to': fields.date('Đến ngày'),
        'dcxh': fields.function(function_dcxh, method=True, string='Điểm chuẩn xu hướng', 
                                type="float", digits=(16,2)),
        'dcbd': fields.float('Điểm chuẩn biên độ', digits=(16,2)),        
        'percent_xh': fields.float('Tỷ lệ trọng số xu hướng', digits=(16, 2)),
        'percent_bd': fields.float('Tỷ lệ trọng số biên độ', digits=(16, 2)),
        
        'exception': fields.one2many('snc.nhan.dinh.ngay.exception', 'name', string="Các ngày không nhận định"),
        'users': fields.many2many('res.users', 'snc_nhan_dinh_ngay_setup_res_users_rel', 'nid', 'uid', 'Người dùng cần tính trọng số'),
        
        'is_active': fields.boolean('Active'),
        
        'user_id': fields.many2one('res.users', string="Create user", readonly=True),
        'create_date': fields.datetime('Create date', readonly=True),        
    }
    _defaults = {
        'name': lambda *x: ' ',
        'state': lambda *x: 'auto',
        'user_id': lambda self, cr, uid, context=None: uid,        
    }
    _order = "is_active desc, create_date desc"
    
    def get_info(self, cr, uid, fields=None, context=None):
        res = {}
        ids = self.search(cr, uid, [('is_active', '=', True)],
                          order="create_date desc", limit=1)
        if ids:
            res = self.read(cr, uid, ids[0], fields)
        return res
    
    def get_users(self, cr, uid, context=None):
        res = []
        users = self.get_info(cr, uid, ['users'])
        ids = users.get('users', [])
        res = self.pool.get('res.users').read(cr, uid, ids, ['name'])
        return res
    
    def check_state_available(self, cr, uid, context=None):
        if not context:
            context = {}
        res = False
        info = self.get_info(cr, uid, ['from_time', 'to_time', 'state'])
        if not info:
            if context.get('raise', False):
                raise osv.except_osv(_('Cảnh báo!'), _('Nhận định chưa được thiết lập. Không được nhận định.'))
        else:
            #check
            if info['state'] == 'open':
                res = True
            elif info['state'] == 'auto':
                now = self.pool.get('vieterp.utils').get_now(cr, uid)
                hour = float(now.strftime('%H'))
                minute = float(now.strftime('%M'))
                t = hour + (minute / 60)
                if t >= info['from_time'] and t <= info['to_time']:
                    res = True
        #result
        if res == False:
            if context.get('raise', False):
                raise osv.except_osv(_('Cảnh báo!'), _('Nhận định đang đóng. Không được nhận định.'))        
        return res
    
    def get_state_info(self, cr, uid):
        res = {}
        info = self.get_info(cr, uid, ['from_time_str', 'to_time_str', 'state'])
        if not info:
            res = {'status': False, 'msg': 'Nhận định chưa được thiết lập.'}
        else:
            from_time = info['from_time_str']
            to_time = info['to_time_str']
             
            if info['state'] == 'close':
                res = {'status': False, 'msg': 'Nhận định đã đóng.'}
            elif info['state'] == 'open':
                res = {'status': True, 'msg': 'Nhận định đang mở.'}
            else:
                if self.check_state_available(cr, uid) == True:
                    res = {'status': True, 'msg': 'Nhận định đang mở. Từ %s đến %s.' % (from_time, to_time)}
                else:
                    res = {'status': False, 'msg': 'Nhận định đang đóng. Thời gian nhận định từ %s đến %s.' % (from_time, to_time)}
        return res
    
snc_nhan_dinh_ngay_setup()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

