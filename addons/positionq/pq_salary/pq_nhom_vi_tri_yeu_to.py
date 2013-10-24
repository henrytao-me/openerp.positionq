# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode
import types
from warnings import catch_warnings

class pq_nhom_vi_tri_yeu_to(osv.osv):
    
    def func_type(self, cr, uid, ids, fields, args, context=None):
        res = {}
        flow = [['nhom_vi_tri', 'yeu_to', 'tieu_chi', 'bac'],
                ['nhom_vi_tri', 'yeu_to', 'tieu_chi'],
                ['nhom_vi_tri', 'yeu_to', 'yeu_to_2'],
                ['nhom_vi_tri', 'yeu_to']]
        for obj in self.read(cr, uid, ids, ['nhom_vi_tri', 'yeu_to', 'yeu_to_2', 'tieu_chi', 'bac']):
            value = ''
            for f in flow:
                is_flow = True
                for sf in f:
                    if not obj[sf]:
                        is_flow = False
                        break
                if is_flow == True:
                    value = '.'.join(f)
                    break
            res[obj['id']] = value
        return res
    
    def func_trong_so(self, cr, uid, ids, fields, args, context=None):
        res = {}
        for obj in self.read(cr, uid, ids, ['nhom_vi_tri', 'yeu_to']):
            value = 0
            tids = self.search(cr, uid, [('type', '=', 'nhom_vi_tri.yeu_to.yeu_to_2'),
                                         ('nhom_vi_tri', '=', obj['nhom_vi_tri'][0]),
                                         ('yeu_to', '=', obj['yeu_to'][0])],
                               order="id desc")
            for tobj in self.read(cr, uid, tids, ['nhom_vi_tri', 'yeu_to', 'yeu_to_2_trong_so']):
                value += tobj['yeu_to_2_trong_so']
            res[obj['id']] = value
        return res
    
    def func_ty_trong(self, cr, uid, ids, fields, args, context=None):
        res = {}
        bak = {}
        for obj in self.read(cr, uid, ids, ['nhom_vi_tri', 'yeu_to', 'trong_so']):
            value = 0
            value = obj['trong_so']
            total = bak.get(obj['nhom_vi_tri'][0])
            # get from bak
            if not total:
                total = 0
                tids = self.search(cr, uid, [('type', '=', 'nhom_vi_tri.yeu_to'),
                                             ('nhom_vi_tri', '=', obj['nhom_vi_tri'][0])])
                for tobj in self.read(cr, uid, tids, ['trong_so']):
                    total += tobj['trong_so']
                bak[obj['nhom_vi_tri'][0]] = total
            # process as normal
            if total == 0:
                value = 0
            else:
                value = value * 1.0 / total
            res[obj['id']] = value
        return res
    
    def func_tieu_chi_ty_trong(self, cr, uid, ids, fields, args, context=None):
        res = {}
        yeu_to_bak = {}
        tieu_chi_bak = {}
        for obj in self.read(cr, uid, ids, ['nhom_vi_tri', 
                                            'yeu_to', 
                                            'tieu_chi',
                                            'tieu_chi_trong_so']):
            value = 0
            total = tieu_chi_bak.get(''.join([str(obj['nhom_vi_tri'][0]), str(obj['yeu_to'][0])]))
            yeu_to_ty_trong = yeu_to_bak.get(''.join([str(obj['nhom_vi_tri'][0]), str(obj['yeu_to'][0])]))
            # get yeu to - ty trong
            if not yeu_to_ty_trong:
                yeu_to_ty_trong = 0
                tids = self.search(cr, uid, [('type', '=', 'nhom_vi_tri.yeu_to'),
                                            ('nhom_vi_tri', '=', obj['nhom_vi_tri'][0]),
                                            ('yeu_to', '=', obj['yeu_to'][0])])
                tobj = self.obj2dict(cr, uid, self.read(cr, uid, tids, ['nhom_vi_tri', 
                                                                        'yeu_to', 
                                                                        'ty_trong']), ['nhom_vi_tri', 
                                                                                       'yeu_to'])
                yeu_to_ty_trong = tobj.get(obj['nhom_vi_tri'][0], {}).get(obj['yeu_to'][0], {}).get('ty_trong', 0)
                yeu_to_bak[''.join([str(obj['nhom_vi_tri'][0]), str(obj['yeu_to'][0])])] = yeu_to_ty_trong 
            # get yeu to - tieu chi - tong
            if not total:
                total = 0
                tids = self.search(cr, uid, [('type', '=', 'nhom_vi_tri.yeu_to.tieu_chi'),
                                             ('nhom_vi_tri', '=', obj['nhom_vi_tri'][0]),
                                             ('yeu_to', '=', obj['yeu_to'][0])])
                for tobj in self.read(cr, uid, tids, ['tieu_chi_trong_so']):
                    total += tobj['tieu_chi_trong_so']
                tieu_chi_bak[''.join([str(obj['nhom_vi_tri'][0]), str(obj['yeu_to'][0])])] = total
            # calculate
            if total != 0:
                value = obj['tieu_chi_trong_so'] * 1.0 / total * yeu_to_ty_trong
            res[obj['id']] = value
        return res
    
    def _trong_so(self, cr, uid, ids, context=None):
        res = []
        for obj in self.read(cr, uid, ids, ['nhom_vi_tri']):
            tids = self.search(cr, uid, [('type', '=', 'nhom_vi_tri.yeu_to'),
                                         ('nhom_vi_tri', '=', obj['nhom_vi_tri'][0])])
            res = res + tids
        return res
    
    def _ty_trong(self, cr, uid, ids, context=None):
        res = {}
        for obj in self.read(cr, uid, ids, ['nhom_vi_tri']):
            for tid in self.search(cr, uid, [('type', '=', 'nhom_vi_tri.yeu_to'),
                                             ('nhom_vi_tri', '=', obj['nhom_vi_tri'][0])]):
                res[tid] = True
        return res.keys()
    
    def _tieu_chi_ty_trong(self, cr, uid, ids, context=None):
        res = {}
        for obj in self.read(cr, uid, ids, ['nhom_vi_tri', 'yeu_to']):
            for tid in self.search(cr, uid, [('type', '=', 'nhom_vi_tri.yeu_to.tieu_chi'),
                                             ('nhom_vi_tri', '=', obj['nhom_vi_tri'][0])]):
                res[tid] = True
        return res.keys()
    
    _name = 'pq.nhom.vi.tri.yeu.to'
    _description = 'Nhom vi tri - Yeu to'
    _columns = {
        'name': fields.char('Tên', size=128),
        'nhom_vi_tri': fields.many2one('pq.nhom.vi.tri', string="Nhóm vị trí", ondelete="cascade"),
        'yeu_to': fields.many2one('pq.yeu.to', string="Yếu tố", ondelete="cascade"),
        'yeu_to_2': fields.many2one('pq.yeu.to', string="Yếu tố 2", ondelete="cascade"),
        'tieu_chi': fields.many2one('pq.tieu.chi', string="Tiêu chí", ondelete="cascade"),
        'bac': fields.integer("Bậc"),
        
        'type': fields.function(func_type, method=True, string="Type", type="char", size=128, store=True),
        
        # nhom vi tri - yeu to
        'trong_so': fields.function(func_trong_so, method=True, string='Trọng số', type="float", digits=(16, 2),
                                    store={'pq.nhom.vi.tri.yeu.to': (_trong_so, ['yeu_to_2_trong_so'], 10)}),
        'ty_trong': fields.function(func_ty_trong, method=True, string='Tỷ trọng', type="float", digits=(16, 2),
                                    store={'pq.nhom.vi.tri.yeu.to': (_ty_trong, ['yeu_to_2_trong_so'], 15)}),
        
        # nhom vi tri - yeu to - yeu to 
        'yeu_to_2_trong_so': fields.float('Trọng số', digits=(16, 2)),
        
        # nhom vi tri - yeu to - tieu chi 
        'tieu_chi_trong_so': fields.float('Trọng số', digits=(16, 2)),
        'tieu_chi_ty_trong': fields.function(func_tieu_chi_ty_trong, method=True, string="Tỷ trọng", type="float", digits=(16, 2),),
        
        'create_date': fields.datetime('Ngày giờ tạo', readonly=True),
        'user_id': fields.many2one('res.users', string="Người tạo", readonly=True),
    }
    _defaults = {
        'yeu_to_2_trong_so': lambda self, cr, uid, context = None: 0,
        'tieu_chi_trong_so': lambda self, cr, uid, context = None: 0,
        'user_id': lambda self, cr, uid, context = None: uid
    }
    _sql_constraints = [
        ('_unique', 'unique(nhom_vi_tri, yeu_to, yeu_to_2, tieu_chi, bac)', 'record is unique')
    ]
    
    def auto_sync(self, cr, uid, nhom_vi_tri_id=None, yeu_to_id=None):
        if not nhom_vi_tri_id and not yeu_to_id:
            return
        elif nhom_vi_tri_id:
            yeu_to_ids = self.pool.get('pq.yeu.to').search(cr, uid, [])
            for xid in yeu_to_ids: 
                self.create(cr, uid, {'nhom_vi_tri': nhom_vi_tri_id,
                                       'yeu_to': xid})
        else: 
            nhom_vi_tri_ids = self.pool.get('pq.nhom.vi.tri').search(cr, uid, [])
            for xid in nhom_vi_tri_ids:
                self.create(cr, uid, {'nhom_vi_tri': xid,
                                      'yeu_to': yeu_to_id})
        return
    
    def obj2dict(self, cr, uid, obj, keys=[]):
        res = {}
        if len(keys) == 0:
            return res
        item = keys.pop(0)        
        for o in obj:
            if len(keys) == 0:
                res[o[item][0]] = o
            else:
                tmp = []
                for to in obj:
                    if to[item][0] == o[item][0]:
                        tmp.append(to)
                res[o[item][0]] = self.obj2dict(cr, uid, tmp[:], keys[:])
        return res
    
    def get_yeu_to_matrix(self, cr, uid, nhom_vi_tri_id):
        res = {'yeu_to': [],
               'data': {}}
        # get yeu to
        yeu_to_ids = self.pool.get('pq.yeu.to').search(cr, uid, [])
        res['yeu_to'] = self.pool.get('pq.yeu.to').read(cr, uid, yeu_to_ids, ['name'])
        res['yeu_to'].sort(key=lambda x: x['id'])
        # get yeu_to data
        ids = self.search(cr, uid, [('nhom_vi_tri', '=', nhom_vi_tri_id),
                                    ('type', '=', 'nhom_vi_tri.yeu_to')])
        tmp = self.obj2dict(cr, uid, self.read(cr, uid, ids, ['yeu_to',
                                                              'trong_so',
                                                              'ty_trong']), ['yeu_to'])
        for x in res['yeu_to']:
            res['data'][x['id']] = {'trong_so': tmp.get(x['id'], {}).get('trong_so', 0),
                                    'ty_trong': tmp.get(x['id'], {}).get('ty_trong', 0),
                                    'yeu_to': {}}
        # get yeu_to.yeu_to_2 data
        ids = self.search(cr, uid, [('nhom_vi_tri', '=', nhom_vi_tri_id),
                                    ('type', '=', 'nhom_vi_tri.yeu_to.yeu_to_2')])
        tmp = self.obj2dict(cr, uid, self.read(cr, uid, ids, ['yeu_to',
                                                              'yeu_to_2',
                                                              'yeu_to_2_trong_so']), ['yeu_to',
                                                                                      'yeu_to_2'])
        for x in res['yeu_to']:
            for y in res['yeu_to']:
                res['data'][x['id']]['yeu_to'][y['id']] = {'id': tmp.get(x['id'], {}).get(y['id'], {}).get('id', None),
                                                           'trong_so': tmp.get(x['id'], {}).get(y['id'], {}).get('yeu_to_2_trong_so', 0)}
        return res
    
    def set_yeu_to_matrix(self, cr, uid, nhom_vi_tri_id, data):
        for x in data:
            for y in data[x]['yeu_to']:
                value = 0
                if x < y:
                    try:
                        value = int(data[x]['yeu_to'][y]['trong_so'])
                    except:
                        pass
                if x > y:
                    try:
                        value = 2 - int(data[y]['yeu_to'][x]['trong_so'])
                    except: 
                        value = 2
                        pass
                if not data[x]['yeu_to'][y]['id']:
                    self.create(cr, uid, {'nhom_vi_tri': nhom_vi_tri_id,
                                         'yeu_to': x,
                                         'yeu_to_2': y,
                                         'yeu_to_2_trong_so': value})
                else:
                    self.write(cr, uid, data[x]['yeu_to'][y]['id'], {'yeu_to_2_trong_so': value})
        return
    
    def get_tieu_chi_matrix(self, cr, uid, nhom_vi_tri_id):
        res = {}
        info = {}
        # get nhom vi tri - yeu to.ty trong
        tids = self.search(cr, uid, [('type', '=', 'nhom_vi_tri.yeu_to'),
                                     ('nhom_vi_tri', '=', nhom_vi_tri_id)])
        info['yeu_to'] = self.obj2dict(cr, uid, self.read(cr, uid, tids, ['yeu_to', 
                                                                          'ty_trong']), ['yeu_to'])
        # get nhom vi tri - yeu to - tieu chi.tieu_chi_trong_so, tieu_chi_ty_trong
        tids = self.search(cr, uid, [('type', '=', 'nhom_vi_tri.yeu_to.tieu_chi'),
                                     ('nhom_vi_tri', '=', nhom_vi_tri_id)])
        info['tieu_chi'] = self.obj2dict(cr, uid, self.read(cr, uid, tids, ['yeu_to', 
                                                                            'tieu_chi', 
                                                                            'tieu_chi_trong_so', 
                                                                            'tieu_chi_ty_trong']), ['yeu_to',
                                                                                                    'tieu_chi'])
        # get yeu to tieu chi
        ids = self.pool.get('pq.tieu.chi').search(cr, uid, [])
        for obj in self.pool.get('pq.tieu.chi').read(cr, uid, ids, ['name', 'yeu_to']):
            if not res.get(obj['yeu_to'][0]):
                res[obj['yeu_to'][0]] = {'id': obj['yeu_to'][0],
                                         'name': obj['yeu_to'][1],
                                         'ty_trong': info['yeu_to'].get(obj['yeu_to'][0], {}).get('ty_trong', 0),
                                         'tieu_chi': {}}
            res[obj['yeu_to'][0]]['tieu_chi'][obj['id']] = {'_id': info['tieu_chi'].get(obj['yeu_to'][0], {}).get(obj['id'], {}).get('id', None),
                                                            'id': obj['id'],
                                                            'name': obj['name'],
                                                            'trong_so': info['tieu_chi'].get(obj['yeu_to'][0], {}).get(obj['id'], {}).get('tieu_chi_trong_so', 0),
                                                            'ty_trong': info['tieu_chi'].get(obj['yeu_to'][0], {}).get(obj['id'], {}).get('tieu_chi_ty_trong', 0)}
        return res
    
    def set_tieu_chi_matrix(self, cr, uid, nhom_vi_tri_id, data):
        # calculate yeu to
        for i in data:
            for j in data[i]['tieu_chi']:
                tieu_chi_id = data[i]['tieu_chi'][j].get('_id')
                if not data[i]['tieu_chi'][j].get('_id'):
                    tieu_chi_id = self.create(cr, uid, {'nhom_vi_tri': nhom_vi_tri_id,
                                          'yeu_to': data[i]['id'],
                                          'tieu_chi': data[i]['tieu_chi'][j]['id'],
                                          'tieu_chi_trong_so': data[i]['tieu_chi'][j]['trong_so']})
                else:
                    self.write(cr, uid, data[i]['tieu_chi'][j].get('_id', []), {'tieu_chi_trong_so': data[i]['tieu_chi'][j]['trong_so']})
        return
    
    def get_tieu_chi_bac_matrix(self, cr, uid, nhom_vi_tri_id):
        res = {}
        # get bac
        bac_info = self.pool.get('pq.config').get_info(cr, uid)
        numOfBac = bac_info.get('so_bac', 5)
        bac = []
        i = 0
        while i < numOfBac:
            i += 1
            bac.append({'id': i,
                        'name': i})
        # tieu chi - bac matrix
        res = self.get_tieu_chi_matrix(cr, uid, nhom_vi_tri_id) 
        for ytid in res:
            for tcid in res[ytid]['tieu_chi']:
                res[ytid]['tieu_chi'][tcid]['bac'] = {}
                # get bac
                fvalue = round(res[ytid]['tieu_chi'][tcid]['ty_trong'] * bac_info.get('bac_min', 100))
                lvalue = round(res[ytid]['tieu_chi'][tcid]['ty_trong'] * bac_info.get('bac_max', 1000))
                step = round((lvalue - fvalue) / len(bac))
                bac_value = {}
                for key, b in enumerate(bac):
                    if key == 0:
                        bac_value[b['id']] = fvalue
                    elif key == len(bac) - 1:
                        bac_value[b['id']] = lvalue
                    else:
                        bac_value[b['id']] = fvalue + step * key
                for b in bac:
                    res[ytid]['tieu_chi'][tcid]['bac'][b['id']] = {'name': b['name'],
                                                                   'trong_so': bac_value[b['id']]}
        res = {'bac': bac,
               'data': res}
        return res
    
    def set_tieu_chi_bac_matrix(self, cr, uid, nhom_vi_tri_id, data):
        return self.set_tieu_chi_matrix(cr, uid, nhom_vi_tri_id, data['data'])        
    
pq_nhom_vi_tri_yeu_to()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

