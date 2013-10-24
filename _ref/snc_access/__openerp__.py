# -*- coding: utf-8 -*-

{
    'name': 'SNC Quản Lý Quyền',
    'version': '1.0',
    'author': "Henry Tao",
    'category': 'SNC',
    'author': 'contact@vieterp.vn',
    'website': 'http://vieterp.vn',
    'description': '',
    'depends': [
        'snc_base',
    ],
     'update_xml': [
        'res_groups.xml',
        'res_users.xml',
        
        'menu.xml',
        'security/security.xml',     
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
