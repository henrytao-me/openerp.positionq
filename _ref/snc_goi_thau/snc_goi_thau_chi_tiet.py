# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode

class snc_goi_thau_chi_tiet(osv.osv):

    def function_get_value(self, cr, uid, ids, fields, args, context=None):
        _res = {}
        #get tham so
        _tham_so = self.pool.get('snc.tham.so').get_tham_so(cr, uid)
        if _tham_so:
            for _tham_so_data in _tham_so:
                expression = _tham_so_data + ' = ' + str(_tham_so[_tham_so_data])
                exec expression
        #begin get value from formula
        for _obj in self.read(cr, uid, ids, ['name', 'gia_goi_thau_cong_thuc', 
                                            'gia_dang_mang_cong_thuc'], context=context):
            gia_loi = 0
            gia_goi_thau = 0
            gia_dang_mang = 0      
            try:
                gia_loi = self.pool.get('snc.goi.thau').read(cr, uid, _obj['name'][0], ['gia_loi'])['gia_loi']
                exec 'gia_goi_thau' + ' = ' + _obj['gia_goi_thau_cong_thuc']
                exec 'gia_dang_mang' + '=' + _obj['gia_dang_mang_cong_thuc']
            except Exception, e:
                logging.error(str(e))
            _res[_obj['id']] = {
                'gia_goi_thau': gia_goi_thau,
                'gia_dang_mang': gia_dang_mang
            }
        return _res
    
    def function_get_tieu_chuan_ky_thuat(self, cr, uid, ids, fields, args, context=None):
        res = {}
        obj_product = self.pool.get('product.product')
        for obj in self.read(cr, uid, ids, ['product_id']):
            product = obj_product.read(cr, uid, obj['product_id'][0], ['tieu_chuan_ky_thuat_id'])
            res[obj['id']] = product['tieu_chuan_ky_thuat_id'][1]
        return res
    
    _name = 'snc.goi.thau.chi.tiet'
    _description = 'Chi Tiet Goi Thau'
    _columns = {
        'name': fields.many2one('snc.goi.thau', string='Gói thầu'),
        'product_id': fields.many2one('product.product', string='Sản phẩm', required=True),
        'tieu_chuan_ky_thuat': fields.function(function_get_tieu_chuan_ky_thuat, type="char", size="256",
                                               string="Tiêu chuẩn kỹ thuật"),
        
        'gia_goi_thau_cong_thuc': fields.char('Giá gói thầu (công thức)', size=128),
        'gia_dang_mang_cong_thuc': fields.char('Giá đăng mạng (công thức)', size=128),
        
        'gia_goi_thau': fields.function(function_get_value, type="float", digits=(16,2), multi=True, 
                                        string='Giá gói thầu'),
        'gia_dang_mang': fields.function(function_get_value, type="float", digits=(16,2), multi=True,
                                        string='Giá đăng mạng'),
        'user_id':fields.many2one('res.users', string='Người tạo', required=True),
    }
    _defaults = {
        'user_id': lambda self, cr, uid, context=None: uid,
    }
    
snc_goi_thau_chi_tiet()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

