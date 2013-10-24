# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.osv.fields import datetime as datetime_field
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from unidecode import unidecode

class snc_vote(osv.osv):
#    ###################################################################
    
    def function_title(self, cr, uid, ids, fields, args, context=None):
        res = {}
        utils = self.pool.get('vieterp.utils')
        for obj in self.read(cr, uid, ids, ['name', 'code_title', 'code', 
                                            'vote_date_title', 'vote_date']):
            vote_date = ''
            try:
                vote_date = utils.get_date_format_from_date(cr, uid, obj['vote_date'])
            except:
                pass
            title = ' '.join([obj['name'] or '', 
                              obj['code_title'] or '', 
                              obj['code'] or '', 
                              obj['vote_date_title'] or '', 
                              vote_date or ''])
            title = title.strip()            
            res[obj['id']] = title
        return res
    
    def function_close_price(self, cr, uid, ids, fields, args, context=None):
        res = {}
        obj_vote_detail = self.pool.get('snc.vote.detail')
        for obj in self.read(cr, uid, ids, ['vote_detail_ids', 'state']):            
            if obj['state'] != 'closed':
                res[obj['id']] = 0
                continue
            close_price = 0
            #get last vote by user
            vote_by_u = obj_vote_detail.get_vote_detail(cr, uid, obj['id'], is_dict = True)
            for user_id in vote_by_u.keys():
                value = vote_by_u[user_id].get('value')
                if value == False:
                    vote_by_u.pop(user_id)
                if vote_by_u.get(user_id):
                    vote_by_u[user_id].update({
                        'value': value[1] 
                    })
            #count vote
            vote_value = {}
            vote_count = 0
            for user_id in vote_by_u:
                if not vote_value.get(vote_by_u[user_id].get('value')):
                    vote_value.update({
                        vote_by_u[user_id].get('value'): 0
                    })
                value = vote_value.get(vote_by_u[user_id].get('value')) 
                vote_value.update({
                    vote_by_u[user_id].get('value'): value + 1
                })
                vote_count += 1
            #calculate vote percent
            percent_vote = {};
            min_vote = 60
            
            tmp = 0;
            for key, value in sorted(vote_value.items(), key=lambda x: x[0]):
                percent_vote[key] = value + tmp
                tmp += value
                
            ket_qua = 0
            for key, value in percent_vote.items():
                if float(value) / float(vote_count) * 100 >= min_vote:
                    if(ket_qua > key or ket_qua == 0):
                        ket_qua = key
            #return close_price
            close_price = float(ket_qua)
            res[obj['id']] = close_price 
        return res
    
    def function_hieu_luc(self, cr, uid, ids, fields, args, context=None):
        res = {}
        now = datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)        
        for obj in self.read(cr, uid, ids, ['close_date'], context=context):
            res[obj['id']] = obj['close_date'] > now 
        return res
    
    def function_get_lme(self, cr, uid, ids, fields, args, context=None):
        res = {}
        for obj in self.read(cr, uid, ids, ['create_date']):
            vals = 0
            lme = self.pool.get('snc.lme').get_info(cr, uid, type="ngay", arg="last", 
                                                    from_date_time=obj['create_date'])
            if lme: 
                vals = lme.get('last')
            res[obj['id']] = vals
        return res
               
    ###################################################################      
    _name = 'snc.vote'
    _description = 'Bo phieu'
    _inherit = ['mail.thread']
    _columns = {        
        'name': fields.char('Tiêu đề', size=128, required=True),        
        'code_title': fields.char('Mã', size=64),
        'code': fields.char('Mã', size=64),        
        'vote_date_title': fields.char('Ngày bỏ phiếu', size=64),
        'vote_date': fields.date('Ngày bỏ phiếu'),
        'title': fields.function(function_title, method=True, type="char", size=256, string="Tiêu đề",
                    store={
                        'snc.vote': (lambda self, cr, uid, ids, *args: ids, ['name', 
                                                                             'code_title',
                                                                             'code',
                                                                             'vote_date_title',
                                                                             'vote_date'], 5)
                    }),
        
        'close_date':fields.datetime('Thời gian đóng'),
        'close_price': fields.function(function_close_price, method=True, type="float", digits=(16,2),
                                       string='Giá đóng',
                                       store={
                                            'snc.vote': (lambda self, cr, uid, ids, *args: ids, ['state'], 5)
                                       }),
                
        'hieu_luc': fields.function(function_hieu_luc, method=True, type="boolean",
                                    string = 'Hiệu lực'),
        
        'state': fields.selection([('draft', _('Soạn thảo')),
                                   ('open', _('Đang mở')),
                                   ('canceled', _('Đã hủy')),
                                   ('closed', _('Đã đóng')),                                   
                                   ], string='Trạng thái'),
                
        'lme': fields.function(function_get_lme, method=True, type="float", digits=(16,2), string="LME",
                               store={
                                    'snc.vote': (lambda self, cr, uid, ids, *args: ids, ['code'], 5),
                               }),
        
        'vote_solution_ids': fields.one2many('snc.vote.solution', 'vote_id', string='Phương án bỏ phiếu'),
        
        'vote_detail_ids': fields.one2many('snc.vote.detail', 'vote_id', string='Chi tiết bỏ phiếu'),
        
        'create_date': fields.datetime('Ngày giờ tạo', readonly=True),
        'user_id': fields.many2one('res.users', string='Người bỏ phiếu', required=True),
    }
    _defaults = {
        'state': lambda *x: 'draft',
        'vote_date': lambda *x: datetime.now().strftime(DEFAULT_SERVER_DATE_FORMAT),
        'user_id': lambda self, cr, uid, context=None: uid,
    }
    _order = 'vote_date desc, code desc, create_date desc'
    
    def dashboard_view(self, cr, uid, args=None, context=None):
        res = {
            'code': '-',
            'vote_date': '-',
            'state': '-',
            'close_date': '-',
            'close_price': '-',
            'vote_users': '-'        
        }
        ids = self.search(cr, uid, ['|', ('state', '=', 'closed'),
                                    ('state', '=', 'open')], limit=1)
        if ids:
            info = self.read(cr, uid, ids[0], ['code', 'vote_date', 'state', 
                                               'close_date', 'close_price', 'vote_detail_ids'])
            res.update({
                'code': info['code'],
                'vote_date': info['vote_date'],
                'state': info['state'],
                'close_date': self.pool.get('vieterp.utils').get_datetime_format_from_datetime(cr, uid, info['close_date'], DEFAULT_SERVER_DATETIME_FORMAT),
                'close_price': info['close_price']
            })
            #get vote_users
            user_log = {}
            vote_users = {}
            for obj in self.pool.get('snc.vote.detail').read(cr, uid, info.get('vote_detail_ids', []), ['user_id']):
                if not user_log.get(obj['user_id'][0]):
                    user_log.update({obj['user_id'][0]: True})
                    vote_users.update({obj['user_id'][1]: True})                
            vote_users = vote_users.keys()
            vote_users = ', '.join(vote_users)
            res.update({'vote_users': vote_users})
        return res 
    
    
    def schedule_close_date_event(self, cr, uid):
        ids = self.search(cr, uid, [('state', '=', 'open'), 
                                    ('close_date', '<=', datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT))])
        if ids:
            self.write(cr, uid, ids, {'state': 'closed'})
            
    def write(self, cr, uid, ids, vals, context=None):
        if vals.get('state', '') == 'open':
            new_ids = []
            for obj in self.read(cr, uid, ids, ['hieu_luc']):
                 if obj['hieu_luc'] == True:
                     new_ids.append(obj['id'])
            ids = new_ids
        res = super(snc_vote, self).write(cr, uid, ids, vals, context=context)
        self.schedule_close_date_event(cr, uid)        
        return res
    
    def copy(self, cr, uid, id, default=None, context=None):
        #override duplicate button
        if context is None:
            context = {}
        context = context.copy()
        cp = self.copy_data(cr, uid, id, default, context)
        cp_list = ['name','code_title','code','vote_date_title','vote_date','close_date']
        data = {}
        for i in cp_list:
            data[i] = cp.get(i, None)        
        #code
        code = data.get('code', '0')
        try:
            data.update({
                'code': int(code) + 1
            })
        except:
            pass
        #vote_date
        vote_date = data.get('vote_date', '')
        try:
            if vote_date and vote_date != '':
                data.update({
                    'vote_date': datetime.now().strftime(DEFAULT_SERVER_DATE_FORMAT)
                })
        except:
            pass
        #close_date
        data.update({
            'close_date': datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        })        
        #create new snc_vote
        new_id = self.create(cr, uid, data, context)
        #update solution
        obj_solution = self.pool.get('snc.vote.solution')
        solution = self.read(cr, uid, id, ['vote_solution_ids'])
        for vote_solution_id in solution['vote_solution_ids']:  
            solution = obj_solution.copy_data(cr, uid, vote_solution_id)
            if solution['r_value'] < 0:
                solution['vote_id'] = new_id
                solution.pop('user_id')
                obj_solution.create(cr, uid, solution, context)                
        #
        self.copy_translations(cr, uid, id, new_id, context)
        return new_id
    
    def poll_read(self, cr, uid, id, context=None):
        res = {}
        hoz_cols = []
        ver_cols = []        
        data = []
        
        hoz_cols_id = []
        ver_cols_id = []
        
        if id == False:
            return res
        
        #get vote data
        vote_data = self.read(cr, uid, id, ['state'])
        
        #get default vote solution => put to hoz_cols
        solution_ids = self.pool.get('snc.vote.solution').search(cr, uid, [('r_value', '<', 0),
                                                                  ('vote_id', '=', id)])
        if solution_ids:
            for obj in self.pool.get('snc.vote.solution').read(cr, uid, solution_ids, ['name']):
                hoz_cols.append(obj['name'])
                hoz_cols_id.append(obj['id'])
        hoz_cols.append('Giá đề xuất')
        hoz_cols_id.append(0)
        #get vote_detail
        vote_detail = self.pool.get('snc.vote.detail').get_vote_detail(cr, uid, id, is_dict = True)
        #get voted user => put to ver_cols
        tmp = vote_detail.values()
        tmp.sort(key = lambda x: x['create_date'])
        for obj in tmp:
            ver_cols.append(obj['user_id'][1])
            ver_cols_id.append(obj['user_id'][0])
        #get data
        for user_id in ver_cols_id:
            #get readonly
            readonly = True if vote_data.get('state', '') != 'open' or user_id != uid else False
            #
            obj = vote_detail.get(user_id)
            if obj['value'] == False:
                    obj['value'] = (-1, '')
            #list solution
            row = []
            for hoz_id in hoz_cols_id:
                if obj['value'][0] == hoz_id:
                    row.append({
                        'ver_id': user_id,
                        'hoz_id': hoz_id,                
                        'value': True,
                        'type': 'radio',
                        'readonly': readonly
                    })
                elif hoz_id == 0:
                    row.append({
                        'ver_id': user_id,
                        'hoz_id': hoz_id,                
                        'value': obj['value'][1] if obj['value_type'] == False else '',
                        'type': 'textbox',
                        'readonly': readonly
                    })
                else:
                    row.append({
                        'ver_id': user_id,
                        'hoz_id': hoz_id,                
                        'value': None,
                        'type': 'radio',
                        'readonly': readonly
                    })
            data.append(row)
        res.update({
            'hoz_cols': hoz_cols,
            'ver_cols': ver_cols,
            'data': data
        })        
        return res
    
    def poll_add(self, cr, uid, id, context=None):
        if id == False:
            return False
        
        #get vote data
        vote_data = self.read(cr, uid, id, ['state'])
        if vote_data.get('state', '') != 'open':
            return False
        
        obj_vote_detail = self.pool.get('snc.vote.detail')
        obj_vote_detail.create(cr, uid, {
            'vote_id': id,
            'user_id': uid
        })
        return True
    
    def poll_save(self, cr, uid, id, data, context=None):
        if id == False:
            return False
        
        #get vote data
        vote_data = self.read(cr, uid, id, ['state'])
        if vote_data.get('state', '') != 'open':
            return False
        
        obj_vote_detail = self.pool.get('snc.vote.detail')
        for record in data:
            vote_detail_ids = obj_vote_detail.search(cr, uid, [('vote_id', '=', id), 
                                                                   ('user_id', '=', uid)], 
                                                         order="create_date desc", limit=1)
            if vote_detail_ids:
                if record['hoz_id'] != '0':
                    obj_vote_detail.write(cr, uid, vote_detail_ids, {
                        'value': record['hoz_id'] 
                    })
                else:   
                    obj_solution = self.pool.get('snc.vote.solution')
                    value = 0
                    try:
                        value = float(record['value'])
                    except:
                        pass
                    new_solution_id = obj_solution.create(cr, uid, {
                        'vote_id': id,
                        'user_id': uid,
                        'r_value': value
                    })
                    obj_vote_detail.write(cr, uid, vote_detail_ids, {
                        'value': new_solution_id 
                    })
                    print record
        return True
    
snc_vote()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

