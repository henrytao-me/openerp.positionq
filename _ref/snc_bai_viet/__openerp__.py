# -*- coding: utf-8 -*-

{
    'name': 'SNC Bài Viết',
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
        'snc_article_audio.xml',
        'snc_article_fix.xml',
        'snc_article_source.xml',
        'snc_article_topic.xml',
        'snc_article.xml',
        
        'menu.xml',
        'security/security.xml',
        'security/ir.model.access.csv'     
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
