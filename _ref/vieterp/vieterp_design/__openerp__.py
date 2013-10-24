# -*- coding: utf-8 -*-

{
    'name': 'VietERP Design',
    'version': '1.0',
    'author': "Henry Tao",
    'category': 'vieterp',
    'author': 'contact@vieterp.vn',
    'website': 'http://vieterp.vn',
    'description': '',
    'depends': [
        'base'
    ],
     'update_xml': [
        'act_window.xml',
        'ir_model.xml',
        'ir_ui_menu.xml',
        'ir_ui_view.xml',
        
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
        'static/xml.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': 1,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
