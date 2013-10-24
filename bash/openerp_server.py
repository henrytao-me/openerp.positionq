#!/usr/bin/env python
import sys
import os
from sys import platform as _platform

def load_helper():
    ls = {
        '--db_host': 'Database host',
        '--db_port': 'Database port',
        '--db_user': 'Database username',
        '--db_password': 'Database password',
        '--xmlrpc-port': 'Default 8069',
        '--netrpc-port': 'Default 8070',
        '--addons_path': "List of addons want to use. Ex: --addons_path 'a, b, c, d'" 
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

user_home = ''
#
if _platform == "linux" or _platform == "linux2":
    user_home = os.getenv("HOME") + '/'
elif _platform == "darwin":
    user_home = "/Volumes/iMac/"
elif _platform == "win32":
    user_home = 'C:\\'
#
openerp_path = os.path.join(user_home, 'workspace', 'github', 'positionq')
addons_path = os.path.join(openerp_path, 'addons')
launcher_path = os.path.join(openerp_path, 'openerp-server')

if __name__ == '__main__':
    ls = {
        '--db_host': 'localhost',
        '--db_port': '5432',
        '--db_user': 'openerp',
        '--db_password': 'openerp',
        '--xmlrpc-port': '8069',
        '--netrpc-port': '8070',
        '--addons-path': ','.join([
            os.path.join(addons_path, 'vieterp'),
            os.path.join(addons_path, 'positionq')     
        ])
    }
    # load helper
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
    if ls.get('--addons-path', '') == '':
        ls.pop('--addons-path')
    #
    args = [launcher_path]
    for key in ls:
        args.append(key + '=' + ls.get(key, ''))
    #
    sys.argv = args
    sys.path.append(openerp_path)
    
    
    #
    import openerp
    openerp.cli.main()    
    # end

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
