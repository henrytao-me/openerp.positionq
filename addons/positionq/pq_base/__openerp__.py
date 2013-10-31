# -*- coding: utf-8 -*-

{
    'name': 'PositionQ Base',
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
    ],
     'update_xml': [
        'security/security.xml',
        'security/ir.model.access.csv',
        
        'menu.xml',
    ],   
    'js': [
        'static/js.js',
        'static/lib/angular/angular.min.js',
        'static/lib/angular/js.js'
    ],
    'css': [
        'static/lib/angular/css.css',
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
