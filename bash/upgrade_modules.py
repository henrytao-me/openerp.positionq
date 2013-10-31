#!/usr/bin/python


from libs import oorpc
from libs.oorpc import OpenObjectRPC
import getpass
import sys

def load_helper():
    ls = {
        '--host': 'localhost',
        '--port': '8069',
        '--db_name': 'positionq',
        '--password': 'a',
        '--modules': 'pq_base, vieterp_base'
    }
    #
    import argparse
    parser = argparse.ArgumentParser(description='Start server arguments...')
    #
    keys = ls.keys()
    keys.sort()
    for key in keys:
        parser.add_argument(key, help=ls.get(key, ''))        
    #    
    args = parser.parse_args()
    exit()

module_model = 'ir.module.module'
module_upgrade_model = 'base.module.upgrade'


def search_modules_ids_by_name(oorpc, module_name):
    args = [('name', '=', module_name)]
    return oorpc.search(module_model, args) or None

def upgrade_modules(oorpc, modules_ids):
    to_be_installed_ids = []
    for module in oorpc.execute(module_model, 'read', modules_ids, ['state', 'name']):
        if module['state'] == 'uninstalled':
            print 'Marking module [%s] to be installed ...' % (module['name'])
            oorpc.execute(module_model, 'button_install', [module['id']])
            to_be_installed_ids.append(module['id'])
            modules_ids.remove(module['id'])
    print 'Marking modules to be upgraded ...'
    oorpc.execute(module_model, 'button_upgrade', modules_ids)

    ids_module = oorpc.search(module_model, [('state', 'in', ('to upgrade', 'to install'))])
    print 'Upgrading modules ...'
    oorpc.execute(module_upgrade_model, 'upgrade_module', modules_ids + to_be_installed_ids)

    print 'Starting post objects ...'
    oorpc.execute(module_upgrade_model, 'config', [], {'ids_module': ids_module})


def run(host, port, db_name, password, modules):
    print '>>> UPGRADE-MODULES IN PROGRESS ...'
    print '---'

    if not password:
        password = getpass.getpass('Password: ')
    username = 'admin'
    oorpc = OpenObjectRPC(host, db_name, username, password, port)
    modules_ids = []
    modules_names = []

    print 'Updating module list ...'
    oorpc.execute(module_model, 'update_list')

    for module_name in modules:
        if module_name not in modules_names:
            print 'Searching for module [%s] ...' % (module_name,)
            ids = search_modules_ids_by_name(oorpc, module_name)
            if not ids:
                print 'WARNING: this module was not found!'
            else:
                modules_names.append(module_name)
                modules_ids.extend(ids)
    modules_ids = list(set(modules_ids))
    upgrade_modules(oorpc, modules_ids)

    print '---'
    print '>>> UPGRADE-MODULES ENDED.'

if __name__ == '__main__':
    ls = {
        '--host': 'localhost',
        '--port': '8069',
        '--db_name': 'demo',
        '--password': 'a',
        '--modules': 'pq_base, vieterp_base'
    }
    #load helper
    if '--help' in sys.argv:
        load_helper()
        sys.exit()
    #
    keys = ls.keys()
    for arg in sys.argv:
        tmp = arg.split('=')
        if tmp[0] in keys:
            ls.update({tmp[0]: tmp[1]})        
    #
    ls.update({'--modules': ls.get('--modules', '').replace(' ', '').split(',')})
    #
    run(ls.get('--host'), ls.get('--port'), ls.get('--db_name'), 
        ls.get('--password'), ls.get('--modules'))
    #end


