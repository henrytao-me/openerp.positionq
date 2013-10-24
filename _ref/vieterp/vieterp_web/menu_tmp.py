#############################################
# disable tmp Menu
#############################################
import operator 
from openerp.addons.web import http as openerpweb
from openerp.addons.web.controllers import main as addons_web_controllers_main

@openerpweb.jsonrequest
def load(self, req):
    """ Loads all menu items (all applications and their sub-menus).

    :param req: A request object, with an OpenERP session attribute
    :type req: < session -> OpenERPSession >
    :return: the menu root
    :rtype: dict('children': menu_nodes)
    """
    Menus = req.session.model('ir.ui.menu')

    fields = ['name', 'sequence', 'parent_id', 'action']
    menu_root_ids = self.get_user_roots(req)
    menu_roots = Menus.read(menu_root_ids, fields, req.context) if menu_root_ids else []
    menu_root = {
        'id': False,
        'name': 'root',
        'parent_id': [-1, ''],
        'children': menu_roots,
        'all_menu_ids': menu_root_ids,
    }
    if not menu_roots:
        return menu_root

    # menus are loaded fully unlike a regular tree view, cause there are a
    # limited number of items (752 when all 6.1 addons are installed)
    menu_ids = Menus.search([('id', 'child_of', menu_root_ids)], 0, False, False, req.context)
    menu_items = Menus.read(menu_ids, fields, req.context)
    
    ####################################  
    import ast
    for menu_item in menu_items:
        if menu_item['action']:
            menu_item['res_model'] = menu_item['action'].split(',')[1]
            res_model_id = int(menu_item['res_model'])
            #ref to act_window
            act = req.session.model('ir.actions.act_window')
            #print act
            tmp = act.read([res_model_id], ['name', 'res_model'], req.context)
            for a in tmp:
                menu_item['res_model'] = a['res_model']
                break                                
            #output to res_model
            #menu_item['res_model'] = tmp[0]['res_model']
        else:
            menu_item['res_model'] = False
        #check menu first id
#         try:
#                 
#             if menu_item['action']:
#                 _act_name = menu_item['action'].split(',')[0]
#                 _act_id = int(menu_item['action'].split(',')[1])            
#                 if _act_name == 'ir.actions.act_window':
#                     act = req.session.model('ir.actions.act_window').read(_act_id, ['domain', 
#                                                                                     'context', 
#                                                                                     'res_model'])
#                     _domain = ast.literal_eval(act.get('domain') or '[]')
#                     _context = ast.literal_eval(act.get('context') or '{}')
#                     model_data_id = req.session.model(act['res_model']).search(_domain, 0, 1, None, _context)
#                     if model_data_id:
#                         menu_item['first_id'] = model_data_id[0]
#         except:
#             pass
    ####################################
    
    # adds roots at the end of the sequence, so that they will overwrite
    # equivalent menu items from full menu read when put into id:item
    # mapping, resulting in children being correctly set on the roots.
    menu_items.extend(menu_roots)
    menu_root['all_menu_ids'] = menu_ids # includes menu_root_ids!

    # make a tree using parent_id
    menu_items_map = dict(
        (menu_item["id"], menu_item) for menu_item in menu_items)
    for menu_item in menu_items:
        if menu_item['parent_id']:
            parent = menu_item['parent_id'][0]
        else:
            parent = False
        if parent in menu_items_map:
            menu_items_map[parent].setdefault(
                'children', []).append(menu_item)

    # sort by sequence a tree using parent_id
    for menu_item in menu_items:
        menu_item.setdefault('children', []).sort(
            key=operator.itemgetter('sequence'))

    return menu_root

addons_web_controllers_main.Menu.load = load