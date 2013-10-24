{
    'name': 'VietERP Web Graph',
    'version': '1.0',
    'author': "Henry Tao",
    'category': 'Vieterp',
    'author': 'hung.tq@vieterp.vn',
    'website': 'http://vieterp.vn',
    'description': """
View Graph for Vieterp.
""",
    'version': '1.0',
    'depends': ['web', 'web_graph'],
    'js': [
        'static/src/js/graph.js'
    ],
    'css': [
        'static/src/css/css.css',
    ],
    'qweb' : [
        'static/src/xml/xml.xml'
    ],
    'auto_install': False
}
