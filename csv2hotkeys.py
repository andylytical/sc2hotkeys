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
import csv
import pathlib
import pprint

# pretty printer config
pp = pprint.PrettyPrinter( sort_dicts=False )

# Hash to hold module level data
resources = {}

def get_args():
    if 'args' not in resources:
        # parse cmdline args
        desc = '''
            Generate starcraft hotkey file from CSV files.
            CSV files are exported from the planning spreadsheet.
            '''
        parser = argparse.ArgumentParser( description=desc )
        parser.add_argument( '--debug', '-d', action='store_true' )
        parser.add_argument( '--verbose', '-v', action='store_true' )
        parser.add_argument( '-C', '--commandcodes',
            help='CSV file mapping Units+Actions to CommandCodes.'
            )
        parser.add_argument( '-c', '--commands',
            help='CSV file mapping Units+Actions to individual keycap letters.'
            )
        parser.add_argument( '-K', '--hotkeycodes',
            help='CSV file mapping Units+Actions to CommandCodes.'
            )
        parser.add_argument( '-k', '--hotkeys',
            help='''
                CSV file mapping Camera and ControlGroup actions
                to keycap letter plus modifier.
                '''
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
    if 'command_codes' not in resources:
        code_map = {}
        args = get_args()
        f = pathlib.Path( args.commandcodes )
        resources['command_codes'] = parse_code_map( f )
    return resources['command_codes']


def get_hotkey_codes():
    if 'hotkey_codes' not in resources:
        code_map = {}
        args = get_args()
        f = pathlib.Path( args.hotkeycodes )
        code_map = parse_code_map( f )
        # code_map is a two-layer hash, but hotkey codes doesn't use Unit,
        # so the entire hash is embedded in key <empty-string>
        resources['hotkey_codes'] = code_map['']
    return resources['hotkey_codes']

def parse_code_map( fn ):
    ''' Create map of [Unit][Command] -> Command Code/Unit Code
    '''
    code_map = {}
    with fn.open() as fh:
        csvreader = csv.DictReader( fh )
        for row in csvreader:
            cmd_code = row['Command Code']
            unit_code = row['Unit Code']
            # new_cmd is cmd_code/unit_code (no slash if unit_code is null)
            if unit_code:
                new_cmd = f'{cmd_code}/{unit_code}'
            else:
                new_cmd = f'{cmd_code}'
            # 'Unit' defaults to 'unit_code' (if Unit is null)
            # 'Unit' can be multiple elements split by a slash (/),
            #   in which case, create an entry for each one
            # Same for 'Command' and 'cmd_code' relationship
            units = [ unit_code ] # default
            if row['Unit']:
                units = row['Unit'].split('/') # override unit_code
            commands = [ cmd_code ] # default
            if row['Command']:
                commands = row['Command'].split('/') # override cmd_code
            for unit in units:
                for command in commands:
                    old_cmd = code_map.setdefault(unit,{}).setdefault(command,new_cmd)
                    if new_cmd != old_cmd:
                        raise UserWarning(
                            (f"attempt to replace '{old_cmd}'"
                            f" with '{new_cmd}'"
                            f" for Unit='{unit}' command='{command}'"
                            f" at line '{csvreader.line_num}'")
                        )
    return code_map


def get_commands( code_map ):
    ''' Parse csv of Units + Commands
    '''
    args = get_args()
    f = pathlib.Path( args.commands )
    commands = {}
    with f.open() as fh:
        csvreader = csv.DictReader( fh )
        ignore_headers = ('', 'Race', 'Unit')
        keycaps = [ x for x in csvreader.fieldnames if x not in ignore_headers ]
        dumpvar( keycaps, 'KEYCAPS' )
        for row in csvreader:
            if row['Race'] == 'comment':
                continue
            unit = row['Unit']
            for k in keycaps:
                if len( row[k] ) < 1:
                    continue # skip empty cells (no action defined)
                for action in row[k].split('/'):
                    try:
                        cmd = code_map[unit][action]
                    except KeyError as err:
                        # If not found as unit + action, try empty string as unit
                        logger.debug(f"{csvreader.line_num} UNIT '{unit}' : ACTION '{action}' ... n/a trying null unit")
                        cmd = code_map[''][action]
                    logger.debug(f"{csvreader.line_num} UNIT '{unit}' : ACTION '{action}' => '{cmd}'")
                    commands.setdefault( cmd, [] ).append( k )
    return( commands )


def get_hotkeys( code_map ):
    '''Parse csv (from spreadsheet) of ControlGroups and Cameras
    '''
    args = get_args()
    f = pathlib.Path( args.hotkeys )
    hotkeys = {}
    with f.open() as fh:
        csvreader = csv.DictReader( fh )
        ignore_headers = ('Key','Comment','')
        modifiers = [ h for h in csvreader.fieldnames if h not in ignore_headers ]
        dumpvar( modifiers, 'MODIFIERS' )
        for row in csvreader:
            # dumpvar( row, 'ROW' )
            keycap = row['Key']
            for mod in modifiers:
                action = row[mod]
                if len(action) < 1:
                    continue
                if mod == 'None':
                    new_combo = f'{keycap}'
                else:
                    new_combo = '+'.join( [ mod, keycap ] )
                logger.debug( f"{csvreader.line_num} ACTION '{action}' COMBO '{new_combo}'" )
                cmd = code_map[ action ]
                hotkeys.setdefault( cmd, [] ).append( new_combo )
    return hotkeys


def print_keymap( keymap, title=None ):
    if title:
        print( f'[{title}]')
    else:
        raise UserWarning( 'print_hotkey_commands: missing title' )
    # for k,v in keymap.items():
    for k in sorted( keymap.keys() ):
        combostrings = ','.join( set( keymap[k] ) ) # set will ensure no duplicates
        print( f'{k}={combostrings}' )
    print()


def print_settings():
    settings = { 'AllowSetConflicts': '1' }
    print_keymap( settings, title='Settings' )


def dumpvar( var, title='UNKNOWN' ):
    logger.debug( '%s\n%s', title, pp.pformat( var ) )

def run():
    args = get_args()
    logger.debug( 'ARGS' )
    logger.debug( pp.pformat( args ) )

    # Settings
    print_settings()

    # Commands - Units and Buildings
    codemap = get_command_codes()
    dumpvar( codemap, 'COMMAND CODES' )
    commandmap = get_commands( codemap )
    dumpvar( commandmap, 'COMMANDS' )
    print_keymap( commandmap, title='Commands' )

    # Hotkeys - Cameras and Control Groups
    codemap = get_hotkey_codes()
    dumpvar( codemap, 'HOTKEY CODES' )
    hotkeymap = get_hotkeys( codemap )
    dumpvar( hotkeymap, 'HOTKEYS' )
    print_keymap( hotkeymap, title='Hotkeys' )


if __name__ == '__main__':
    run()
