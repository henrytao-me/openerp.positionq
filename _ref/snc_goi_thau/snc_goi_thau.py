# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode
from lxml import etree

class snc_goi_thau(osv.osv):
    
#    def function_create_date_format(self, cr, uid, ids, fields, args, context=None):
#        if not context:
#            context = {}    
#        res = {}        
#        utils = self.pool.get('vieterp.utils')
#        for obj in self.browse(cr, uid, ids, context=context):            
#            res[obj.id] = utils.get_datetime_format_from_datetime(cr, uid, obj.create_date, context=context)
#        return res

    def function_ngay_gio_het_hieu_luc_format(self, cr, uid, ids, fields, args, context=None):
        if not context:
            context = {}    
        res = {}        
        utils = self.pool.get('vieterp.utils')
        for obj in self.read(cr, uid, ids, ['ngay_gio_het_hieu_luc'], context=context):            
            res[obj['id']] = utils.get_datetime_format_from_datetime(cr, uid, obj['ngay_gio_het_hieu_luc'], 
                                                                     context=context)
        return res

    def function_title(self, cr, uid, ids, fields, args, context=None):
        res = {}
        utils = self.pool.get('vieterp.utils')
        for obj in self.read(cr, uid, ids, ['name', 'ma_so_goi_thau_title', 'ma_so_goi_thau', 
                                            'ngay_dang_title', 'ngay_dang']):
            
            ngay_dang = ''
            try:
                ngay_dang = utils.get_date_format_from_date(cr, uid, obj['ngay_dang'])
            except:
                pass
            
            data = {
                'title': '',
                'alias': ''
            }            
            data['title'] = ' '.join([obj['name'] or '', 
                                       obj['ma_so_goi_thau_title'] or '', 
                                       obj['ma_so_goi_thau'] or '', 
                                       obj['ngay_dang_title'] or '', 
                                       ngay_dang or ''])
            data['title'] = data['title'].strip()
            data['alias'] = utils.get_alias_from_string(cr, uid, data['title'], context=context)
            res[obj['id']] = data
        return res
    
    def function_hieu_luc(self, cr, uid, ids, fields, args, context=None):
        res = {}
        now = datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)        
        for obj in self.read(cr, uid, ids, ['ngay_gio_het_hieu_luc'], context=context):
            res[obj['id']] = obj['ngay_gio_het_hieu_luc'] > now 
        return res
    
    def _get_gia_loi_snc_vote(self, cr, uid, ids, context=None):
        res = []
        obj_vote = self.pool.get('snc.vote')
        #get ngay which in ids
        ngay = {}
        for vote in obj_vote.read(cr, uid, ids, ['state', 'vote_date']):
            ngay[vote['vote_date']] = True
        ngay = ngay.keys()
        #get snc_goi_thau_id which have snc_goi_thau.ngay_dang = snc_vote.vote_date
        ids = self.pool.get('snc.goi.thau').search(cr, uid, [('ngay_dang', 'in', ngay)])
        res = ids
        return res
    
    def function_gia_loi(self, cr, uid, ids, fields, args, context=None):
        res = {}
        #get ngay dang
        ngay_dang = {}
        for obj in self.read(cr, uid, ids, ['ngay_dang']):
            ngay_dang[obj['ngay_dang']] = True
        ngay_dang = ngay_dang.keys()
        #get gia_loi by date
        gia_loi = {} 
        vote_ids = self.pool.get('snc.vote').search(cr, uid, [('vote_date', 'in', ngay_dang),
                                                              ('state', '=', 'closed')])
        
        check_date = {}
        for obj in self.pool.get('snc.vote').read(cr, uid, vote_ids, ['vote_date', 'close_price', 'create_date']):
            if not check_date.get(obj['vote_date']):
                check_date.update({obj['vote_date']: obj['create_date']})
                gia_loi[obj['vote_date']] = obj['close_price']
            if check_date.get(obj['vote_date']) < obj['create_date']:
                check_date.update({obj['vote_date']: obj['create_date']})
                gia_loi[obj['vote_date']] = obj['close_price']
        #get result
        for obj in self.read(cr, uid, ids, ['ngay_dang']):
            res[obj['id']] = gia_loi.get(obj['ngay_dang'], 0)
            if res[obj['id']] != 0:
                self.auto_post_bidding(cr, uid, obj['id'])
        return res
    
    _name = 'snc.goi.thau'
    _description = 'Goi Thau'
    _inherit = ['mail.thread']
    _columns = {
        'name': fields.char('Tiêu đề', size=256, required=True),
        'title': fields.function(function_title, method=True, type="char", size=256, string="Tiêu đề",
                    store={
                        'snc.goi.thau': (lambda self, cr, uid, ids, *args: ids, ['name', 
                                                                                 'ma_so_goi_thau_title',
                                                                                 'ma_so_goi_thau',
                                                                                 'ngay_dang_title',
                                                                                 'ngay_dang'], 5)
                    }, multi='function_title'),
        'alias': fields.function(function_title, method=True, string='Alias', type='char', size=400,                    
                    store={
                        'snc.goi.thau': (lambda self, cr, uid, ids, *args: ids, ['name', 
                                                                                 'ma_so_goi_thau_title',
                                                                                 'ma_so_goi_thau',
                                                                                 'ngay_dang_title',
                                                                                 'ngay_dang'], 10),                        
                    }, multi='function_title'),
        
        'hinh_dai_dien': fields.binary('Hình đại diện'),
        'ma_so_goi_thau_title': fields.char('Mã số gói thầu (Tiêu đề)', size=32),
        'ma_so_goi_thau': fields.char('Mã số gói thầu'),
        'ngay_dang_title': fields.char('Ngày đăng (Tiêu đề)', size=32),
        'ngay_dang': fields.date('Ngày đăng'),
        
        'create_date': fields.datetime('Ngày giờ tạo', readonly=True),
        
        'ngay_gio_het_hieu_luc': fields.datetime('Thời gian hết hiệu lực', required=True),
        'ngay_gio_het_hieu_luc_format': fields.function(function_ngay_gio_het_hieu_luc_format, method=True, 
                                            string='Thời gian hết hiệu lực', type='char', size=20),
        'hieu_luc': fields.function(function_hieu_luc, method=True, type="boolean",
                                    string = 'Hiệu lực'),
        
        'noi_dung_ngan_gon': fields.html('Nội dung ngắn gọn'),
        'noi_dung_chi_tiet': fields.html('Nội dung chi tiết', required=True),
        
        'chi_tiet_goi_thau_ids': fields.one2many('snc.goi.thau.chi.tiet', 'name', string='Chi tiết'),
        
        'gia_loi': fields.function(function_gia_loi, method=True, type='float', digits=(16, 2), 
                                   string='Giá lõi', 
                                   store={
                                        'snc.vote': (_get_gia_loi_snc_vote, ['state'], 10),
                                        'snc.goi.thau': (lambda self, cr, uid, ids, *args: ids, 
                                                         ['ngay_dang'], 15)
                                   }),
                
        'tien_te': fields.many2one('res.currency', string="Tiền tệ", required=True),
        'don_vi_tinh': fields.many2one('product.uom', string="Đơn vị tính", required=True),

        'view': fields.integer('View'),
        
        'state': fields.selection([
                                   ('draft', _('Soạn thảo')),
                                   ('auto', _('Chờ giá lõi')),
                                   ('posted', _('Đang Đăng')),
                                   ('canceled', _('Ngừng đăng')),                                   
                                   ], string='Trạng thái'),
        
        'user_id':fields.many2one('res.users', string='Người tạo', required=True),
    }
    _defaults = {
        'state': lambda *x: 'draft',
        'view': lambda *x: 0,
        'hieu_luc': lambda *x: True,   
        'user_id': lambda self, cr, uid, context=None: uid,
    }
    _order = 'create_date desc'
    
    def auto_post_bidding(self, cr, uid, id):
        if self.search(cr, uid, [('id', '=', id), ('state', '=', 'auto')]):
            self.write(cr, uid, id, {'state': 'posted'})
    
    def ui_get_data(self, cr, uid, context=None):
        res = []
        if not context:
            context = {}
        ids = []
        #check filter ids
        ids = context.get('ids', None)
        if not ids:
            ids = self.search(cr, uid, [('state', '=', 'posted')], order='create_date desc')
        #
        fields = ['title', 'hinh_dai_dien', 'alias', 'ngay_gio_het_hieu_luc', 
                                           'noi_dung_ngan_gon', 'gia_loi', 'chi_tiet_goi_thau_ids', 'view']
        if context.get('full', False) == True:
            fields.append('noi_dung_chi_tiet')
        #
        if ids:
            for bidding in self.read(cr, uid, ids, fields):
                tmp = bidding.copy()
                #get detail
                detail = []
                obj = self.pool.get('snc.goi.thau.chi.tiet')                
                for row in obj.read(cr, uid, bidding['chi_tiet_goi_thau_ids'], 
                                    ['product_id', 'tieu_chuan_ky_thuat', 'gia_dang_mang']):
                    detail.append({
                        'product_name': row['product_id'][1],
                        'tieu_chuan_ky_thuat': row['tieu_chuan_ky_thuat'],
                        'gia_dang_mang': row['gia_dang_mang']
                    })
                #
                tmp.update({'_detail': detail})      
                res.append(tmp)
        return res
    
    def ui_get_data_by_alias(self, cr, uid, alias):
        res = {}
        try:
            ids = self.search(cr, uid, [('alias', '=', alias), ('state', '=', 'posted')])
            if ids: 
                res = self.ui_get_data(cr, uid, context = {'ids': ids, 'full': True})
                res = res[0]
                #update view
                self.write(cr, uid, ids[0], {'view': res.get('view', 0) + 1})
        except:
            print '------------------------------'
            print 'ui_get_data_by_alias: error'
            print '------------------------------'
            pass
        return res
    
    def copy(self, cr, uid, id, default=None, context=None):
        #override duplicate button
        if context is None:
            context = {}
        context = context.copy()
        cp = self.copy_data(cr, uid, id, default, context)
        cp_list = ['name', 'ma_so_goi_thau_title', 'ma_so_goi_thau', 'ngay_dang_title', 'ngay_dang', 
                   'ngay_gio_het_hieu_luc', 'noi_dung_ngan_gon', 'noi_dung_chi_tiet', 
                   'tien_te', 'don_vi_tinh',
                   'chi_tiet_goi_thau_ids']
        data = {}
        for i in cp_list:
            data[i] = cp.get(i, None)        
        #ma_so_goi_thau
        ma_so_goi_thau = data.get('ma_so_goi_thau', '0')
        try:
            data.update({
                'ma_so_goi_thau': int(ma_so_goi_thau) + 1
            })
        except:
            pass
        #ngay_dang
        ngay_dang = data.get('ngay_dang', '')
        try:
            if ngay_dang and ngay_dang != '':
                data.update({
                    'ngay_dang': datetime.now().strftime(DEFAULT_SERVER_DATE_FORMAT)
                })
        except:
            pass
        #ngay_gio_het_hieu_luc
        data.update({
            'ngay_gio_het_hieu_luc': datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        })
        #
        new_id = self.create(cr, uid, data, context)
        self.copy_translations(cr, uid, id, new_id, context)
        return new_id
    
snc_goi_thau()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

