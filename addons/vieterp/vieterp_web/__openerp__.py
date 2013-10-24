{
    'name': "VietERP Web",
    'version': '1.0',
    'author': "Henry Tao",
    'category': 'Vieterp',
    'author': 'hung.tq@vieterp.vn',
    'website': 'http://vieterp.vn',
    'description': """
    VietERP Web for VietERP
    """,
    'depends': ['base', 'web'],
    'js': [
        'static/lib/ekit/ekit.js',
        
        'static/src/js/ipad.js',
    ],
    'css': [
        'static/src/css/base.css',
        'static/src/css/ekit.css',
    ],
    'qweb': [
    ],
    'auto_install': False,
}
