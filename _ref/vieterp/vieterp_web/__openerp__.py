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
        
        'static/src/js/boot.js',
        'static/src/js/ipad.js',
        'static/src/js/view_form.js',
        'static/src/js/view_list_editable.js',
        'static/src/js/view_list.js',
    ],
    'css': [
        'static/src/css/base.css',
        'static/src/css/ekit.css',
        'static/src/css/view_list.css',
    ],
    'qweb': [
        'static/src/xml/base.xml',   
        'static/src/xml/view_list.xml',
    ],
    'auto_install': True,
}
