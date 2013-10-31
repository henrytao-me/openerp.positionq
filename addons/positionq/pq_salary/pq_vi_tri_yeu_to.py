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

class pq_vi_tri_yeu_to(osv.osv):
    
    def func_type(self, cr, uid, ids, fields, args, context=None):
        res = {}
        flow = [['vi_tri', 'yeu_to', 'tieu_chi', 'tcc1', 'tcc2'],
                ['vi_tri', 'yeu_to', 'tieu_chi', 'tcc1'],
                ['vi_tri', 'yeu_to', 'tieu_chi'],
                ['vi_tri', 'yeu_to']]
        for obj in self.read(cr, uid, ids, ['vi_tri', 'yeu_to', 'tieu_chi', 'tcc1', 'tcc2']):
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
#     
#     def func_diem(self, cr, uid, ids, fields, args, context=None):
#         res = {}
#         for obj in self.read(cr, uid, ids, ['name']):
#             res[obj['id']] = 0
#         return res
#     
#     def func_tieu_chi_trong_so(self, cr, uid, ids, fields, args, context=None):
#         res = {}
#         for obj in self.read(cr, uid, ids, ['name', 'type', 'vi_tri', 'yeu_to', 'tieu_chi']):
#             value = {'tieu_chi_trong_so': 0,
#                      'tieu_chi_muc_do': 0,
#                      'tieu_chi_diem': 0}
#             if obj['type'] == 'vi_tri.yeu_to.tieu_chi':
#                 tids = self.search(cr, uid, [('type', '=', 'vi_tri.yeu_to.tieu_chi.tcc1'),
#                                              ('vi_tri', '=', obj['vi_tri'][0]),
#                                              ('yeu_to', '=', obj['yeu_to'][0]),
#                                              ('tieu_chi', '=', obj['tieu_chi'][0])])
#                 for tobj in self.read(cr, uid, tids, ['tieu_chi_tcc1_trong_so']):
#                     value['tieu_chi_trong_so'] += tobj['tieu_chi_tcc1_trong_so']
#             res[obj['id']] = value
#         return res
#     
#     def func_tieu_chi_tcc1_trong_so(self, cr, uid, ids, fields, args, context=None):
#         res = {}
#         # get tcc1
#         tcc1 = {}
#         for obj in self.pool.get('pq.tcc1').read(cr, uid, self.pool.get('pq.tcc1').search(cr, uid, []), ['method']):
#             tcc1[obj['id']] = obj
#             
#         # get tcc2
#         tcc2 = {}
#         for obj in self.pool.get('pq.tcc2').read(cr, uid, self.pool.get('pq.tcc2').search(cr, uid, []), ['trong_so']):
#             tcc2[obj['id']] = obj
#         
#         # start
#         for obj in self.read(cr, uid, ids, ['name', 'type', 'vi_tri', 'yeu_to', 'tieu_chi', 'tcc1']):
#             value = 0
#             if obj['type'] == 'vi_tri.yeu_to.tieu_chi.tcc1':
#                 # get depend tcc2
#                 tids = self.search(cr, uid, [('type', '=', 'vi_tri.yeu_to.tieu_chi.tcc1.tcc2'),
#                                              ('vi_tri', '=', obj['vi_tri'][0]),
#                                              ('yeu_to', '=', obj['yeu_to'][0]),
#                                              ('tieu_chi', '=', obj['tieu_chi'][0]),
#                                              ('tcc1', '=', obj['tcc1'][0])])
#                 for tobj in self.read(cr, uid, tids, ['tcc2', 'tieu_chi_tcc1_trong_so']):
#                     if tcc1[obj['tcc1'][0]]['method'] == 10:
#                         value += tobj['tieu_chi_tcc1_trong_so'] * tcc2[tobj['tcc2'][0]]['trong_so']
#                     if tcc1[obj['tcc1'][0]]['method'] == 20:
#                         if value < (tobj['tieu_chi_tcc1_trong_so'] * tcc2[tobj['tcc2'][0]]['trong_so']):
#                             value = tobj['tieu_chi_tcc1_trong_so'] * tcc2[tobj['tcc2'][0]]['trong_so']                    
#             res[obj['id']] = value
#         return res
#     
    _name = 'pq.vi.tri.yeu.to'
    _description = 'Nhom vi tri - Yeu to'
    _columns = {
        'name': fields.char('Tên', size=128),
        'vi_tri': fields.many2one('pq.vi.tri', string="Vị trí", ondelete="cascade"),
        'yeu_to': fields.many2one('pq.yeu.to', string="Yếu tố", ondelete="cascade"),
        'tieu_chi': fields.many2one('pq.tieu.chi', string="Tiêu chí", ondelete="cascade"),
        'tcc1': fields.many2one('pq.tcc1', string="Tiêu chí cấp 1", ondelete="cascade"),
        'tcc2': fields.many2one('pq.tcc2', string="Tiêu chí cấp 2", ondelete="cascade"),
        
        'type': fields.function(func_type, method=True, string="Type", type="char", size=128, store=True),
        
#         # vi tri - yeu to
#         'diem': fields.function(func_diem, method=True, string="Điểm", type="float", digits=(16,2)),
#         
#         # vi tri - yeu to - tieu chi
#         'tieu_chi_trong_so': fields.function(func_tieu_chi_trong_so, string="Trọng số", type="float", digits=(16,2), multi=True),
#         'tieu_chi_muc_do': fields.function(func_tieu_chi_trong_so, string="Mức độ", type="float", digits=(16,2), multi=True),
#         'tieu_chi_diem': fields.function(func_tieu_chi_trong_so, string="Điểm", type="float", digits=(16,2), multi=True),
#         
#         # vi tri - yeu to - tieu chi - tcc1
#         'tieu_chi_tcc1_trong_so': fields.function(func_tieu_chi_tcc1_trong_so, string="Trọng số", type="float", digits=(16,2)),
        
        # vi tri - yeu to - tieu chi - tcc1 - tcc2
        'tieu_chi_tcc1_tcc2_trong_so': fields.float('Trọng số', digits=(16,2)), 
        
        'create_date': fields.datetime('Ngày giờ tạo', readonly=True),
        'user_id': fields.many2one('res.users', string="Người tạo", readonly=True),
    }
    _defaults = {
        'tieu_chi_tcc1_tcc2_trong_so': lambda self, cr, uid, context = None: 0,
        'user_id': lambda self, cr, uid, context = None: uid
    }
    _sql_constraints = [
        ('_unique', 'unique(vi_tri, yeu_to, tieu_chi, tcc1, tcc2)', 'record is unique')
    ]
    
    def auto_sync(self, cr, uid, vi_tri_id=None, yeu_to_id=None):
        if not vi_tri_id and not yeu_to_id:
            return
        elif vi_tri_id:
            yeu_to_ids = self.pool.get('pq.yeu.to').search(cr, uid, [])
            for xid in yeu_to_ids: 
                self.create(cr, uid, {'vi_tri': vi_tri_id,
                                       'yeu_to': xid})
        else: 
            vi_tri_ids = self.pool.get('pq.vi.tri').search(cr, uid, [])
            for xid in vi_tri_ids:
                self.create(cr, uid, {'vi_tri': xid,
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
    
    def get_matrix(self, cr, uid, bo_phan_id=None, nhom_vi_tri_id=None):
        res = {'bo_phan': [],
               'nhom_vi_tri': [],
               'vi_tri': [],
               'yeu_to': [],
               'matrix': {}}
        
        # get info
        bac_info = self.pool.get('pq.config').get_info(cr, uid)
        numOfBac = bac_info.get('so_bac', 5)
        
        # filter by bo_phan & nhom_vi_tri
        res['bo_phan'] = self.pool.get('pq.bo.phan').read(cr, uid, self.pool.get('pq.bo.phan').search(cr, uid, []), ['name'])
        res['nhom_vi_tri'] = self.pool.get('pq.nhom.vi.tri').read(cr, uid, self.pool.get('pq.nhom.vi.tri').search(cr, uid, []), ['name'])
        args = []
        bo_phan_id = 1
        if bo_phan_id:
            args.append(('bo_phan', '=', bo_phan_id))
        if nhom_vi_tri_id:
            args.append(('nhom_vi_tri', '=', nhom_vi_tri_id))
        
        # get vi_tri
        ids = self.pool.get('pq.vi.tri').search(cr, uid, args)
        res['vi_tri'] = self.pool.get('pq.vi.tri').read(cr, uid, ids, ['name', 'bo_phan', 'nhom_vi_tri'])
        
        # get yeu_to
        ids = self.pool.get('pq.yeu.to').search(cr, uid, [])
        yeu_to = self.pool.get('pq.yeu.to').read(cr, uid, ids, ['name'])
        
        # get tieu_chi
        ids = self.pool.get('pq.tieu.chi').search(cr, uid, [])
        tieu_chi = {}
        for obj in self.pool.get('pq.tieu.chi').read(cr, uid, ids, ['name', 'yeu_to', 'method', 'trong_so']):
            tieu_chi.setdefault(obj['yeu_to'][0], [])
            tieu_chi[obj['yeu_to'][0]].append(obj)
        
        # get tcc1
        ids = self.pool.get('pq.tcc1').search(cr, uid, [])
        tcc1 = {}
        for obj in self.pool.get('pq.tcc1').read(cr, uid, ids, ['name', 'tieu_chi', 'method']):
            tcc1.setdefault(obj['tieu_chi'][0], [])
            tcc1[obj['tieu_chi'][0]].append(obj)
        
        # get tcc2
        ids = self.pool.get('pq.tcc2').search(cr, uid, [])
        tcc2 = {}
        for obj in self.pool.get('pq.tcc2').read(cr, uid, ids, ['name', 'tcc1', 'trong_so']):
            tcc2.setdefault(obj['tcc1'][0], [])
            tcc2[obj['tcc1'][0]].append(obj)
        
        # get res yeu_to
        for a in yeu_to:
             a['tieu_chi'] = tieu_chi.get(a['id'], [])
             y = 0
             for b in a['tieu_chi']:
                 b['tcc1'] = tcc1.get(b['id'], [])
                 x = 0
                 for c in b['tcc1']:
                     c['tcc2'] = tcc2.get(c['id'], [])
                     c['len'] = len(c['tcc2'])
                     x += c['len'] 
                 b['len'] = x
                 y += b['len']
             a['len'] = y
        res['yeu_to'] = yeu_to
        
        # level_tieu_chi_tcc1_tcc2
        level_tieu_chi_tcc1_tcc2 = {}
        ids = self.search(cr, uid, [('type', '=', 'vi_tri.yeu_to.tieu_chi.tcc1.tcc2')])
        for obj in self.read(cr, uid, ids, ['vi_tri',
                                            'yeu_to',
                                            'tieu_chi',
                                            'tcc1',
                                            'tcc2',
                                            'tieu_chi_tcc1_tcc2_trong_so']):
            a = obj['vi_tri'][0]
            b = obj['yeu_to'][0]
            c = obj['tieu_chi'][0]
            d = obj['tcc1'][0]
            e = obj['tcc2'][0]
            
            level_tieu_chi_tcc1_tcc2.setdefault(a, {})
            level_tieu_chi_tcc1_tcc2[a].setdefault(b, {})
            level_tieu_chi_tcc1_tcc2[a][b].setdefault(c, {})
            level_tieu_chi_tcc1_tcc2[a][b][c].setdefault(d, {})
            level_tieu_chi_tcc1_tcc2[a][b][c][d][e] = obj
        
        # set matrix value
        matrix = {}
        for vi_tri in res['vi_tri']:
            a = vi_tri['id']
            matrix[a] = {'yeu_to': {}}
            for yeu_to in res['yeu_to']:
                b = yeu_to['id']    
                matrix[a]['yeu_to'][b] = {'tieu_chi': {}}            
                for tieu_chi in yeu_to['tieu_chi']:
                    c = tieu_chi['id']
                    matrix[a]['yeu_to'][b]['tieu_chi'][c] = {'tcc1': {},
                                                             'trong_so': 0,
                                                             'muc_do': 0,
                                                             'diem': 0}
                    for tcc1 in tieu_chi['tcc1']:
                        d = tcc1['id']
                        matrix[a]['yeu_to'][b]['tieu_chi'][c]['tcc1'][d] = {'tcc2': {},
                                                                            'method': tcc1['method'],
                                                                            'value': 0,
                                                                            'trong_so': 0}
                        for tcc2 in tcc1['tcc2']:
                            e = tcc2['id']
                            value = level_tieu_chi_tcc1_tcc2.get(a, {}).get(b, {}).get(c, {}).get(d, {}).get(e, {}).get('tieu_chi_tcc1_tcc2_trong_so', 0)
                            matrix[a]['yeu_to'][b]['tieu_chi'][c]['tcc1'][d]['tcc2'][e] = {'id': level_tieu_chi_tcc1_tcc2.get(a, {}).get(b, {}).get(c, {}).get(d, {}).get(e, {}).get('id', None),
                                                                                           'value': value > 0,
                                                                                           'trong_so': 0}
                            if value > 0:
                                matrix[a]['yeu_to'][b]['tieu_chi'][c]['tcc1'][d]['value'] = e
                            
                            # init tcc2 trong_so
                            if value > 0:
                                matrix[a]['yeu_to'][b]['tieu_chi'][c]['tcc1'][d]['tcc2'][e]['trong_so'] = tcc2['trong_so']
                            
                                # init tcc1 trong_so 
                                if tcc1['method'] == 10:    # sum
                                    matrix[a]['yeu_to'][b]['tieu_chi'][c]['tcc1'][d]['trong_so'] += matrix[a]['yeu_to'][b]['tieu_chi'][c]['tcc1'][d]['tcc2'][e]['trong_so']
                                if tcc1['method'] == 20:    # max
                                    matrix[a]['yeu_to'][b]['tieu_chi'][c]['tcc1'][d]['trong_so'] = matrix[a]['yeu_to'][b]['tieu_chi'][c]['tcc1'][d]['tcc2'][e]['trong_so']
                        
                        # init tieu_chi trong_so
                        matrix[a]['yeu_to'][b]['tieu_chi'][c]['trong_so'] += matrix[a]['yeu_to'][b]['tieu_chi'][c]['tcc1'][d]['trong_so']
                    
        # tieu_chi trong_so standard
        for yeu_to in res['yeu_to']:
            b = yeu_to['id']    
            for tieu_chi in yeu_to['tieu_chi']:
                c = tieu_chi['id']
                if tieu_chi['method'] == 20:
                    tieu_chi['trong_so'] = 0
                for vi_tri in res['vi_tri']:
                    a = vi_tri['id']
                    if tieu_chi['method'] == 20:
                        if tieu_chi['trong_so'] < matrix[a]['yeu_to'][b]['tieu_chi'][c]['trong_so']:
                            tieu_chi['trong_so'] = matrix[a]['yeu_to'][b]['tieu_chi'][c]['trong_so']
        
        yeu_to_danh_gia = {}
        
        # tieu_chi muc_do / diem
        for yeu_to in res['yeu_to']:
            b = yeu_to['id']    
            for tieu_chi in yeu_to['tieu_chi']:
                c = tieu_chi['id']
                for vi_tri in res['vi_tri']:
                    a = vi_tri['id']
                    # get nhom vi tri info
                    if not yeu_to_danh_gia.get(vi_tri['nhom_vi_tri'][0]):
                        yeu_to_danh_gia[vi_tri['nhom_vi_tri'][0]] = self.pool.get('pq.nhom.vi.tri.yeu.to').get_tieu_chi_bac_matrix(cr, uid, vi_tri['nhom_vi_tri'][0])
                    # get muc_do
                    muc_do = 1
                    i = 1
                    while i <= numOfBac:
                        if matrix[a]['yeu_to'][b]['tieu_chi'][c]['trong_so'] <= ((tieu_chi['trong_so'] / numOfBac) * i):
                            muc_do = i
                            break
                        i += 1
                    matrix[a]['yeu_to'][b]['tieu_chi'][c]['muc_do'] = muc_do
                    # get diem
                    diem = yeu_to_danh_gia.get(vi_tri['nhom_vi_tri'][0],{}).get('data',{}).get(b,{}).get('tieu_chi',{}).get(c,{}).get('bac',{}).get(muc_do,{}).get('trong_so',0)
                    matrix[a]['yeu_to'][b]['tieu_chi'][c]['diem'] = diem
        
        # vi_tri diem
        for vi_tri in res['vi_tri']:
            a = vi_tri['id']
            matrix[a]['diem'] = 0
            for yeu_to in res['yeu_to']:
                b = yeu_to['id']    
                for tieu_chi in yeu_to['tieu_chi']:
                    c = tieu_chi['id']
                    matrix[a]['diem'] += matrix[a]['yeu_to'][b]['tieu_chi'][c]['diem']
        
        res['matrix'] = matrix
        return res
    
    def set_matrix(self, cr, uid, matrix):
        for a in matrix:
            vi_tri = matrix[a]
            for b in vi_tri['yeu_to']:
                yeu_to = vi_tri['yeu_to'][b]
                for c in yeu_to['tieu_chi']:
                    tieu_chi = yeu_to['tieu_chi'][c]
                    for d in tieu_chi['tcc1']:
                        tcc1 = tieu_chi['tcc1'][d]
                        for e in tcc1['tcc2']:
                            tcc2 = tcc1['tcc2'][e]
                            value = 0
                            # tong
                            if tcc1['method'] == 10:
                                if tcc2['value'] == True:
                                    value = 1
                                pass
                            # max
                            if tcc1['method'] == 20:
                                if int(tcc1['value']) == int(e):
                                    value = 1
                            # update
                            if not tcc2.get('id'):
                                self.create(cr, uid, {'vi_tri': a,
                                                      'yeu_to': b,
                                                      'tieu_chi': c,
                                                      'tcc1': d,
                                                      'tcc2': e,
                                                      'tieu_chi_tcc1_tcc2_trong_so': value})
                            else:
                                self.write(cr, uid, tcc2.get('id'), {'tieu_chi_tcc1_tcc2_trong_so': value})
        return 
        
pq_vi_tri_yeu_to()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
