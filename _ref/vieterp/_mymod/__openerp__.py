# -*- coding: utf-8 -*-

{
    'name': 'MyMod',
    'version': '1.0',
    'author': "Henry Tao",
    'category': 'VietERP',
    'author': 'contact@vieterp.vn',
    'website': 'http://vieterp.vn',
    'description': '',
    'depends': [
        #OpenERP modules
        'base',
        
        #VietERP modules
        'vieterp_base',
    ],
     'update_xml': [        
        'mymod_workflow.xml',
        'mymod.xml',        
        
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
