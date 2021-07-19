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
        parser.add_argument( '-k', '--keymap',
            help='''Keycap replacement map, in INI format.
                Mapping key-value pairs must be in section 'KEYMAP'.'''
                )
        parser.add_argument( 'hotkey_file',
            help='Original SC2 keymap file'
            )
        # Sane defaults
        defaults = {
            'hotkey_file': 'SC2Hotkeys/TheCore6g_right_US_qwerty.SC2Hotkeys',
            'keymap': 'test/rekey_map1',
        }
        parser.set_defaults( **defaults )
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
        cfg.read( pathlib.Path( args.keymap ) )
        rekey_map = { k: v for k,v in cfg.items( 'KEYMAP' ) }
        resources['rekey_map'] = rekey_map
    return resources['rekey_map']


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


def run():
    args = get_args()
    hk1 = parse_hotkeys( pathlib.Path( args.hotkey_file ) )
    logger.info( f"ORIGINAL" )
    if logger.isEnabledFor( logging.INFO ):
        hk1.write( sys.stdout, space_around_delimiters=False )
        print( f"--------" )
    hk2 = remap_keys( hk1 )
    logger.info( f"NEW" )
    hk2.write( sys.stdout, space_around_delimiters=False )
    if logger.isEnabledFor( logging.INFO ):
        print( f"---" )


if __name__ == '__main__':
    run()
