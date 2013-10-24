{
    'name': 'VietERP Custom View',
    'version': '1.0',
    'author': "Henry Tao",
    'category': 'Vieterp',
    'author': 'hung.tq@vieterp.vn',
    'website': 'http://vieterp.vn',
    'description': """
Custom view for Vieterp.
""",
    'version': '1.0',
    'depends': ['base', 'web'],
    'js': [
        'static/src/js/js.js'
    ],
    'css': [
        'static/src/css/css.css',
    ],
    'qweb' : [
        'static/src/xml/xml.xml',
    ],
    'auto_install': False
}
