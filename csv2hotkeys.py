#!.venv/bin/python

# Configure logging
import logging
logger = logging.getLogger( __name__ )
logger.setLevel( logging.ERROR )
l_fmt = logging.Formatter( '%(levelname)s:%(funcName)s[%(lineno)d] %(message)s' )
l_handler = logging.StreamHandler()
l_handler.setFormatter( l_fmt )
logger.addHandler( l_handler )

# Python standard library imports
import argparse
import configparser
import csv
import logging
import pathlib
import pprint
import sys

# Local imports
import hotkey_command

# Hash to hold module level data
resources = {}

def get_args():
    if 'args' not in resources:
        # parse cmdline args
        desc = '''Swap significant keycap in existing SC2Hotkeys file.
            Modifier keys (eg: Control, Shift, Alt) are retained.'''
        parser = argparse.ArgumentParser( description=desc )
        parser.add_argument( '--debug', '-d', action='store_true' )
        parser.add_argument( '--verbose', '-v', action='store_true' )
        parser.add_argument( '-C', '--commandcodes',
            help='''CSV file mapping Units+Actions to CommandCodes.'''
            )
        parser.add_argument( '-c', '--commands',
            help='''CSV file mapping Units+Actions to individual keycap letters.'''
            )
        parser.add_argument( '-K', '--hotkeycodes',
            help='''CSV file mapping Units+Actions to CommandCodes.'''
            )
        parser.add_argument( '-k', '--hotkeys',
            help=( '''CSV file mapping Camera and ControlGroup actions '''
                   '''to keycap letter plus modifier.''' )
            )
        args = parser.parse_args()
        resources['args'] = args
        # Post processing
        if args.verbose:
            logger.setLevel( logging.INFO )
        if args.debug:
            logger.setLevel( logging.DEBUG )
    return resources[ 'args' ]


def get_command_codes():
    ''' Map of
        [Unit-Name][Action] -> Command/Unit
    '''
    if 'command_codes' not in resources:
        code_map = {}
        args = get_args()
        f = pathlib.Path( args.commandcodes )
        with f.open() as fh:
            csvreader = csv.DictReader( fh )
            for row in csvreader:
                cmd_code = row['cmd_code']
                unit_code = row['unit_code']
                # cmd_str is cmd_code/unit_code (no slash if unit_code is null)
                cmd_parts = [ cmd_code ]
                if unit_code:
                    cmd_parts.append( unit_code )
                hk_command = '/'.join( cmd_parts )
                # 'Unit' defaults to 'unit_code' (if Unit is null)
                # If 'Unit' is multiple names split by a slash (/), 
                # then create an entry for each one
                # Same for 'Action' and 'cmd_code' relationship
                actions = [cmd_code] # default
                if row['Action']:
                    actions = row['Action'].split('/') # override
                units = [unit_code] # default
                if row['Unit']:
                    units = row['Unit'].split('/') # override
                for unit_name in units:
                    code_map.setdefault( unit_name, {} )
                    for action_name in actions:
                        old_cmd = code_map[unit_name].setdefault( action_name, hk_command )
                        if hk_command != old_cmd:
                            raise UserWarning(
                                (f"attempt to replace '{old_cmd}'"
                                f" with '{hk_command}'"
                                f" for unit='{unit_name}' action='{action_name}'"
                                f" at line '{csvreader.line_num}'")
                            )
        resources['command_codes'] = code_map
    return resources['command_codes']


def get_commands( code_map ):
    args = get_args()
    f = pathlib.Path( args.commands )
    pp = pprint.PrettyPrinter( sort_dicts=False )
    hotkeys = {}
    with f.open() as fh:
        csvreader = csv.DictReader( fh )
        hdrs_raw = csvreader.fieldnames
        headers = [x for x in hdrs_raw if x] # remove empty strings from list
        #pp.pprint( ['HEADERS', headers] )
        keycaps = headers[2:] #remove 'Race', 'Unit' from list
        pp.pprint( ['KEYCAPS', keycaps] )
        for row in csvreader:
            if row['Race'] == 'comment':
                continue
            unit = row['Unit']
            for k in keycaps:
                # skip empty cells (no action defined)
                if len( row[k] ) < 1:
                    continue
                for action in row[k].split('/'):
                    try:
                        cmd = code_map[unit][action]
                    except KeyError as err:
                        # If not found as unit + action, try empty string as unit
                        print(f"{csvreader.line_num} UNIT '{unit}' : ACTION '{action}' ... n/a trying null unit")
                        cmd = code_map[''][action]
                    print(f"{csvreader.line_num} UNIT '{unit}' : ACTION '{action}' => '{cmd}'")
                    new_hk = hotkey_command.Hotkey_Command( cmd, k )
                    hotkeys.setdefault( cmd, new_hk ).add( k )
    return( hotkeys )




def parse_hotkeys( hotkey_file ):
    cfg = configparser.ConfigParser( interpolation=None )
    cfg.optionxform = lambda option: option #retain original key case
    cfg.read( hotkey_file )
    return cfg


def run():
    args = get_args()
    logger.debug( [ 'ARGS', pprint.pformat( args ) ] )
    code_map = get_command_codes()
    #pprint.pprint( code_map )
    cmd_map = get_commands( code_map=code_map )
    print( '[Commands]' )
    for k,v in cmd_map.items():
        print( f'{k}={v}' )
    

if __name__ == '__main__':
    run()
