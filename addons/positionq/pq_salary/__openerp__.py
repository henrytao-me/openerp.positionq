# -*- coding: utf-8 -*-

{
    'name': 'PositionQ Salary',
    'version': '1.0',
    'author': "Henry Tao",
    'category': 'PositionQ',
    'author': 'hi@henrytao.me',
    'website': 'http://vieterp.vn',
    'description': '',
    'depends': [
        #OpenERP modules
        'base',

        #VietERP modules
        'vieterp_base',
        
        #PositionQ modules
        'pq_base'
    ],
     'update_xml': [
        'pq_nhom_vi_tri.xml',
        'pq_yeu_to.xml',
        'pq_tieu_chi.xml',
        'pq_bac.xml',
        'pq_tcc1.xml',
        'pq_tcc2.xml',
        'pq_vi_tri.xml',
        'pq_bo_phan.xml',
        'pq_nhom_vi_tri_yeu_to.xml',
        'pq_vi_tri_yeu_to.xml',
        'pq_config.xml',
        
        'pq_ltt.xml',
        'pq_ltt_vi_tri.xml',
        'pq_ltt_muc_do.xml',
        'pq_nhom_luong.xml',
        'pq_thang_luong.xml',
        
        'data/data_pq_ltt_vi_tri.xml',
        'data/data_pq_ltt_muc_do.xml',
        'data/data_pq_ltt.xml',
             
        'menu.xml',
    ],   
    'js': [
        'static/js.js'
    ],
    'css': [
        'static/css.css'
    ],
    'qweb': [
        'static/xml.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': 1,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
