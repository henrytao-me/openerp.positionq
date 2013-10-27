# -*- coding: utf-8 -*-

{
    'name': 'VietERP Base',
    'version': '1.0',
    'author': "Henry Tao",
    'category': 'Vieterp',
    'author': 'hung.tq@vieterp.vn',
    'website': 'http://vieterp.vn',
    'depends': [
        # OpenERP modules
        'base',
        'web_shortcuts',
        # VietERP modules
        'vieterp_web',
        'vieterp_custom'
    ],    
    'update_xml': [
        # All menus
        'menu.xml',
    ],
    'installable': True,
    'auto_install': True,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
