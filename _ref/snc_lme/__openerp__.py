# -*- coding: utf-8 -*-

{
    'name': 'SNC LME',
    'version': '1.0',
    'author': "Henry Tao",
    'category': 'PTT',
    'author': 'contact@vieterp.vn',
    'website': 'http://vieterp.vn',
    'description': '',
    'depends': [
        'snc_base',
    ],
     'update_xml': [
        'snc_lme_trading.xml',
        'snc_lme.xml',
#         'snc_lme_update_wizard.xml',
        'snc_truc_gia_lme.xml',
                    
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
