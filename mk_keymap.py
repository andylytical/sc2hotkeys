#!.venv/bin/python

# also: https://github.com/andylytical/gcal-txt2csv/blob/master/txt2csv.py

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
import key_combo

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
        parser.add_argument( '-k', '--keymap_file',
            help='''Keycap replacement map, in INI format.
                Mapping key-value pairs must be in section 'KEYMAP'.'''
                )
        parser.add_argument( '-o', '--overrides_file',
            help='''Direct assignments. Added last, will override anything
                previously set.'''
                )
        parser.add_argument( 'hotkey_file',
            help='Original SC2 hotkeys file'
            )
        # # Sane defaults
        # defaults = {
        #     'hotkey_file': 'SC2Hotkeys/TheCore6g_right_US_qwerty.SC2Hotkeys',
        #     'keymap': 'test/rekey_map1',
        # }
        # parser.set_defaults( **defaults )
        args = parser.parse_args()
        resources['args'] = args
        # Post processing
        if args.verbose:
            logger.setLevel( logging.INFO )
        if args.debug:
            logger.setLevel( logging.DEBUG )
    return resources[ 'args' ]


def get_rekey_map():
    if 'rekey_map' not in resources:
        args = get_args()
        cfg = configparser.ConfigParser( interpolation=None )
        cfg.optionxform = lambda option: option #retain original key case
        cfg.read( pathlib.Path( args.keymap_file ) )
        rekey_map = { k: v for k,v in cfg.items( 'KEYMAP' ) }
        resources['rekey_map'] = rekey_map
    return resources['rekey_map']

def get_override_cfg():
    if 'override_cfg' not in resources:
        args = get_args()
        cfg = configparser.ConfigParser( interpolation=None )
        cfg.optionxform = lambda option: option #retain original key case
        cfg.read( pathlib.Path( args.overrides_file ) )
        resources['override_cfg'] = cfg
    return resources['override_cfg']


def parse_hotkeys( hotkey_file ):
    cfg = configparser.ConfigParser( interpolation=None )
    cfg.optionxform = lambda option: option #retain original key case
    cfg.read( hotkey_file )
    return cfg


def remap_keys( cfg ):
    rekey_map = get_rekey_map()
    new_cfg = configparser.ConfigParser( interpolation=None )
    new_cfg.optionxform = lambda option: option #retain original case of keys
    for section in cfg.sections():
        new_cfg.add_section( section )
        logger.debug( f"SECTION: '{section}'" )
        for command, value in cfg.items( section ):
            logger.debug( f"cmd: '{command}'" )
            # unique keycombos separated by ','
            key_combos = []
            for c_str in value.split( ',' ):
                kc = key_combo.Key_Combo( c_str )
                logger.debug( f"\tOLD {kc}" )
                kc.remap( keymap=rekey_map )
                key_combos.append( kc )
                logger.debug( f"\tNEW {kc}" )
            new_hk = ','.join( map( key_combo.Key_Combo.to_str, key_combos ) )
            logger.debug( f"new new_hk: {new_hk}" )
            new_cfg.set( section, command, new_hk )
    return new_cfg


def add_overrides( cfg ):
    override_cfg = get_override_cfg()
    for section in override_cfg.sections():
        logger.debug( f"OVERRIDE: processing section '{section}'" )
        for command, value in override_cfg.items( section ):
            if logger.isEnabledFor( logging.DEBUG ):
                oldsetting = cfg.get( section, command )
                logger.debug( f"OVERRIDE: '{command}' =  '{oldsetting}' -> '{value}" )
            cfg.set( section, command, value )


def run():
    args = get_args()
    logger.debug( [ 'ARGS', pprint.pformat( args ) ] )
    hk1 = parse_hotkeys( pathlib.Path( args.hotkey_file ) )

    # REKEY
    hk2 = hk1
    if args.keymap_file :
        hk2 = remap_keys( hk1 )
        if logger.isEnabledFor( logging.INFO ):
            logger.info( f"AFTER REKEY" )
            print( f"---" )

    # OVERRIDE
    if args.overrides_file :
        add_overrides( hk2 )

    # PRINT FINAL CONFIG
    hk2.write( sys.stdout, space_around_delimiters=False )
    

if __name__ == '__main__':
    run()
