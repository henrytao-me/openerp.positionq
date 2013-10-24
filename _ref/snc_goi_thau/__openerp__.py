# -*- coding: utf-8 -*-

{
    'name': 'SNC Gói Thầu',
    'version': '1.0',
    'author': "Henry Tao",
    'category': 'PTT',
    'author': 'contact@vieterp.vn',
    'website': 'http://vieterp.vn',
    'description': '',
    'depends': [
        'snc_base',
        'snc_lme',
    ],
     'update_xml': [
        'res_groups.xml',
        'snc_goi_thau_chi_tiet.xml',
        'snc_goi_thau.xml',
        'snc_vote_detail.xml',
        'snc_vote_solution.xml',
        'snc_vote.xml',
        
        'menu.xml',
        'security/security.xml',
        'security/ir.model.access.csv', 
        
        'data/ir_cron.xml' 
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
