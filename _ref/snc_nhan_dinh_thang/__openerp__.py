# -*- coding: utf-8 -*-

{
    'name': 'SNC Nhận Định Tuần',
    'version': '1.0',
    'author': "Henry Tao",
    'category': 'PTT',
    'author': 'contact@vieterp.vn',
    'website': 'http://vieterp.vn',
    'description': '',
    'depends': [
        'snc_base',
#         'snc_lme'
    ],
     'update_xml': [
        'res_groups.xml',
        'snc_nhan_dinh_tuan_exception.xml',
        'snc_nhan_dinh_tuan_setup.xml',
        'snc_nhan_dinh_tuan_thong_ke.xml',
        'snc_nhan_dinh_tuan_trong_so.xml',
        'snc_nhan_dinh_tuan.xml',
        
        'menu.xml',
        'security/security.xml',
        'security/ir.model.access.csv',  
    ],   
    'js': [
        'static/js.js'
    ],
    'css': [
        'static/css.css'
    ],
    'qweb': [
        'static/xml.xml',
        'static/snc_nhan_dinh_tuan/xml.xml',
        'static/snc_nhan_dinh_tuan_thong_ke/xml.xml',
        'static/snc_nhan_dinh_tuan_trong_so/xml.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': 1,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
