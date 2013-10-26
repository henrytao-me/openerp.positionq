# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode
import types

class pq_vi_tri(osv.osv):
    
    def func_diem(self, cr, uid, ids, fields, args, context=None):
        res = {}
        # get pq_vi_tri_yeu_to
        vi_tri_yeu_to = self.pool.get('pq.vi.tri.yeu.to').get_matrix(cr, uid, [('id', 'in', ids)])
        # starts
        for obj in self.read(cr, uid, ids, ['name']):
            res[obj['id']] = vi_tri_yeu_to.get('matrix',{}).get(obj['id'],{}).get('diem',0)
        return res
    
    def func_tong_luong_hien_tai(self, cr, uid, ids, fields, args, context=None):
        res = {}
        for obj in self.read(cr, uid, ids, ['muc_luong_hien_tai', 'so_luong_nhan_vien']):
            value = obj['muc_luong_hien_tai'] * obj['so_luong_nhan_vien']
            res[obj['id']] = value
        return res
    
    def func_luong_diem(self, cr, uid, ids, fields, args, context=None):
        res = {}
        nhom_luong = {}
        for obj in self.read(cr, uid, ids, ['nhom_vi_tri', 'diem']):
            value = 0
            if not nhom_luong.get(obj['nhom_vi_tri'][0]):
                tids = self.pool.get('pq.nhom.luong').search(cr, uid, [('nhom_vi_tri', '=', obj['nhom_vi_tri'][0])])
                nhom_luong[obj['nhom_vi_tri'][0]] = self.pool.get('pq.nhom.luong').read(cr, uid, tids, ['min_point',
                                                                                                        'max_point',
                                                                                                        'ltt_diem'])
            for tobj in nhom_luong.get(obj['nhom_vi_tri'][0]):
                if obj['diem'] >= tobj['min_point'] and (obj['diem'] <= tobj['max_point'] or tobj['max_point'] == 0):
                    value = tobj['ltt_diem']
                    break
            res[obj['id']] = value * obj['diem']
        return res
    
    _name = 'pq.vi.tri'
    _description = 'Vi tri'
    _columns = {
        'name': fields.char('Tên vị trí', size=128, required=True),
        'bo_phan': fields.many2one('pq.bo.phan', string="Bộ phận", required=True),
        'nhom_vi_tri': fields.many2one('pq.nhom.vi.tri', string="Nhóm vị trí", required=True),
        
        'diem': fields.function(func_diem, method=True, string="Điểm", type="float", digits=(16,2)),
        
        'muc_luong_hien_tai': fields.float('Mức lương hiện tại', digits=(16,2)),
        'so_luong_nhan_vien': fields.float('Số lượng nhân viên', digits=(16,2)),
        'tong_luong_hien_tai': fields.function(func_tong_luong_hien_tai, method=True, string='Tổng lương hiện tại', 
                                               type="float", digits=(16,2)),
        
        'luong_diem': fields.function(func_luong_diem, method=True, string="Lương theo điểm", type="float", digits=(16,2)),
        
        'luong_thuc_te': fields.float('Lương thực tế', digits=(16,2)),
        
        'create_date': fields.datetime('Ngày giờ tạo', readonly=True),
        'user_id': fields.many2one('res.users', string="Người tạo",readonly=True),
    }
    _defaults = {
        'muc_luong_hien_tai': lambda *x: 0,
        'so_luong_nhan_vien': lambda *x: 0,
        'luong_thuc_te': lambda *x: 0,
        'user_id': lambda self, cr, uid, context=None: uid,
    }
    
    def create(self, cr, uid, vals, context=None):
        res = super(pq_vi_tri, self).create(cr, uid, vals, context)
        self.pool.get('pq.vi.tri.yeu.to').auto_sync(cr, uid, vi_tri_id=res)     
        return res
    
    def get_tong_ket_luong(self, cr, uid):
        res = {'vi_tri': [],
               'thang_luong': []}
        
        # vi_tri
        ids = self.search(cr, uid, [])
        vi_tri = self.read(cr, uid, ids, ['name', 'bo_phan', 'nhom_vi_tri', 
                                          'muc_luong_hien_tai', 'so_luong_nhan_vien', 'tong_luong_hien_tai', 
                                          'diem', 'luong_diem',
                                          'luong_thuc_te'])
        res['vi_tri'] = vi_tri
        
        # thang_luong
        ids = self.pool.get('pq.thang.luong').search(cr, uid, [])
        thang_luong = self.pool.get('pq.thang.luong').read(cr, uid, ids, ['name', 'ty_le'])
        res['thang_luong'] = thang_luong
        
        # tieu_chi_luong
        ids = self.pool.get('pq.tieu.chi.luong').search(cr, uid, [])
        tieu_chi_luong = self.pool.get('pq.tieu.chi.luong').read(cr, uid, ids, ['chenh_lech', 'muc_chenh_lech',
                                                                                'ty_le', 'muc_ty_le'])
        # (-2: out of index) (-1: ht) (other: muc luong) 
        for obj in tieu_chi_luong:
            # muc_chenh_lech
            a = 0
            try:
                a = int(obj['muc_chenh_lech'])
            except:
                pass
            if a > len(res['thang_luong']):
                a = -1 
            obj['muc_chenh_lech'] = a - 1
            
            # muc_ty_le
            a = 0
            try:
                a = int(obj['muc_ty_le'])
            except:
                pass
            if a > len(res['thang_luong']):
                a = -1 
            obj['muc_ty_le'] = a - 1
        
        # get result
        for vi_tri in res['vi_tri']:
            # add thang_luong to vi_tri
            vi_tri['thang_luong'] = {}
            for thang_luong in res['thang_luong']:
                vi_tri['thang_luong'][thang_luong['id']] = vi_tri['luong_diem'] * thang_luong['ty_le']
            
            # so voi muc luong hien tai
            vi_tri['ss_luong_hien_tai'] = 0
            if vi_tri['muc_luong_hien_tai'] != 0:
                vi_tri['ss_luong_hien_tai'] = vi_tri['luong_diem'] / vi_tri['muc_luong_hien_tai'] - 1
            
            # tinh luong dieu chinh
            vi_tri['luong_dieu_chinh'] = 0
            for tc_luong in tieu_chi_luong:
                _chenh_lech = tc_luong['chenh_lech']
                _muc_chenh_lech = tc_luong['muc_chenh_lech']
                _ty_le = tc_luong['ty_le']
                _muc_ty_le = tc_luong['muc_ty_le']
                
                # get muc_chenh_lech
                if _muc_chenh_lech == -1:
                    _muc_chenh_lech = vi_tri['muc_luong_hien_tai']
                elif tc_luong['muc_chenh_lech'] >= 0:
                    _muc_chenh_lech = vi_tri['thang_luong'][res['thang_luong'][_muc_chenh_lech]['id']]
                else:
                    _muc_chenh_lech = 0
                
                # get muc_ty_le
                if _muc_ty_le == -1:
                    _muc_ty_le = vi_tri['muc_luong_hien_tai']
                elif tc_luong['muc_chenh_lech'] >= 0:
                    _muc_ty_le = vi_tri['thang_luong'][res['thang_luong'][_muc_ty_le]['id']]
                else:
                    _muc_ty_le = 0
                
                if vi_tri['muc_luong_hien_tai'] > 0:
                    if (_muc_chenh_lech / vi_tri['muc_luong_hien_tai'] - 1) <= _chenh_lech:
                        vi_tri['luong_dieu_chinh'] = _ty_le * _muc_ty_le
                        break
                
            # final
            vi_tri['ss_luong_dieu_chinh'] = 0
            vi_tri['tong_luong_dieu_chinh'] = vi_tri['luong_dieu_chinh'] * vi_tri['so_luong_nhan_vien']
            
            vi_tri['ss_luong_thuc_te'] = 0
            vi_tri['tong_luong_thuc_te'] = vi_tri['luong_thuc_te'] * vi_tri['so_luong_nhan_vien']
            
            if vi_tri['muc_luong_hien_tai'] != 0:
                vi_tri['ss_luong_dieu_chinh'] = vi_tri['luong_dieu_chinh'] / vi_tri['muc_luong_hien_tai'] - 1
                vi_tri['ss_luong_thuc_te'] = vi_tri['luong_thuc_te'] / vi_tri['muc_luong_hien_tai'] - 1
        
        return res
    
    def set_tong_ket_luong(self, cr, uid, data):
        for vi_tri in data['vi_tri']:
            self.write(cr, uid, vi_tri['id'], {'luong_thuc_te': vi_tri['luong_thuc_te']})
        return
    
pq_vi_tri()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

