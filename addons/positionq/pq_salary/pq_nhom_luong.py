# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode
import types

class pq_nhom_luong(osv.osv):
    
    def func_diem_chuan(self, cr, uid, ids, fields, args, context=None):
        res = {}
        nhom_vi_tri_diem = {}        
        for obj in self.read(cr, uid, ids, ['name', 'nhom_vi_tri', 'min_point', 'max_point', 
                                            'method', 'custom_point', 'ltt_vi_tri', 'ltt_muc_do']):
            value = {'diem_chuan': 0,
                     'ltt_chuan': 0,
                     'ltt_diem': 0}
            init_diem_chuan = False
            
            # get diem_chuan
            if obj['method'] == 30:
                value['diem_chuan'] = obj['custom_point']
            else:
                if not nhom_vi_tri_diem.get(obj['nhom_vi_tri'][0]):
                    tids = self.pool.get('pq.vi.tri').search(cr, uid, [('nhom_vi_tri', '=', obj['nhom_vi_tri'][0])])
                    nhom_vi_tri_diem[obj['nhom_vi_tri'][0]] = self.pool.get('pq.vi.tri').read(cr, uid, tids, ['diem'])
                for vi_tri in nhom_vi_tri_diem.get(obj['nhom_vi_tri'][0]):
                    # nhom luong check
                    if vi_tri['diem'] < obj['min_point']:
                        continue
                    if vi_tri['diem'] > obj['max_point'] and obj['max_point'] > 0:
                        continue
                    # max / min
                    if init_diem_chuan == False:
                        init_diem_chuan = True
                        value['diem_chuan'] = vi_tri['diem']
                    if obj['method'] == 10 and value['diem_chuan'] > vi_tri['diem']:
                        value['diem_chuan'] = vi_tri['diem']
                    if obj['method'] == 20 and value['diem_chuan'] < vi_tri['diem']:
                        value['diem_chuan'] = vi_tri['diem']
            
            # get ltt_chuan
            tids = self.pool.get('pq.ltt').search(cr, uid, [('ltt_vi_tri', '=', obj.get('ltt_vi_tri', (None, None))[0]),
                                                            ('ltt_muc_do', '=', obj.get('ltt_muc_do', (None, None))[0])])
            if tids: 
               value['ltt_chuan'] = self.pool.get('pq.ltt').read(cr, uid, tids[0], ['luong'])['luong']
            
            # get ltt_diem
            if value['diem_chuan'] != 0:
                value['ltt_diem'] = value['ltt_chuan'] / value['diem_chuan'] 
            
            res[obj['id']] = value
        return res
    
    _name = 'pq.nhom.luong'
    _description = 'Nhom Luong'
    _columns = {
        'name': fields.char('Tên nhóm', size=128),
        'nhom_vi_tri': fields.many2one('pq.nhom.vi.tri', string="Nhóm vị trí"),
        
        'min_point': fields.float('Điểm thấp nhất', digits=(16,2)),
        'max_point': fields.float('Điểm cao nhất', digits=(16,2)),
        
        'method': fields.selection([(10, 'Min'), (20, 'Max'), (30, 'Custom')], 'Phương pháp'),
        'custom_point': fields.float('Điểm được chọn'),
        'diem_chuan': fields.function(func_diem_chuan, method=True, string="Điểm chuẩn", type="float", digits=(16,2), multi=True),
        
        'ltt_vi_tri': fields.many2one('pq.ltt.vi.tri', string="Vị trí công việc"),
        'ltt_muc_do': fields.many2one('pq.ltt.muc.do', string="Mức độ"),
        'ltt_chuan': fields.function(func_diem_chuan, method=True, string="Lương thị trường", type="float", digits=(16,2), multi=True),
        
        'ltt_diem': fields.function(func_diem_chuan, method=True, string="Lương trung bình / điểm", type="float", digits=(16,2), multi=True), 
        
        'create_date': fields.datetime('Ngày giờ tạo', readonly=True),
        'user_id': fields.many2one('res.users', string="Người tạo", readonly=True),
    }
    _defaults = {
        'min_point': lambda *x: 0,
        'max_point': lambda *x: 0,
        'method': lambda *x: 10,
        'custom_point': lambda *x: 0,
        'user_id': lambda self, cr, uid, context = None: uid,
    }
    _sql_constraints = [
        
    ]
    
pq_nhom_luong()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

