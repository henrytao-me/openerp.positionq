# -*- coding: utf-8 -*-

{
    'name': 'VietERP Permission',
    'version': '1.0',
    'category': 'Vieterp',
    'description': 'Access right for single user only. We will support group permission in the next version.',
    'author': 'Henry Tao',
    'website': 'http://vieterp.vn',
    'depends': [
        
        # OpenERP modules
        'base',        
        
        # VietERP modules
        'vieterp_base',
        
    ],
     'update_xml': [
        'res_users.xml',
        'v_groups.xml',
        'v_objects.xml',
        'v_access.xml',
        'ir_model.xml',
        
#        'res_groups.xml',        
#        'ir_model_depend.xml',
#        'ir_model_depend_detail.xml',        
#        'ir_model_access.xml',
        
        'menu.xml',
        
        'scheduler/scheduler.xml'
    ],
    'qweb': [
        'static/xml.xml'
    ],
    'js': [
        'static/js.js'
    ],
    'css': [
        'static/css.css'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': 2,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
