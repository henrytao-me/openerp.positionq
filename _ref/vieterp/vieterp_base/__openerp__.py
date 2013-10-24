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
        #'vieterp_design',
        'vieterp_web',
        'vieterp_web_graph',
        'web_custom',
        'widget_custom',
        #'widget_poll',
    ],    
    'update_xml': [
        
        # Data
        'data/ir_config_parameter.xml',
        'data/res_company.xml',
        'data/ir_cron.xml',
        
        # Views
        'vieterp_tmp.xml',
        'res_company.xml',
        'currency_rate_update.xml',
        
        # All menus
        'menu.xml',
        
        # Security        
        'security/res_groups.xml',
        'security/security.xml',
        'security/ir.model.access.csv',        
    ],
    'installable': True,
    'auto_install': True,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
