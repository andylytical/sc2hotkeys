#!.venv/bin/python

# also: https://github.com/andylytical/gcal-txt2csv/blob/master/txt2csv.py

import logging
# Configure logging
import logging
logger = logging.getLogger( __name__ )
# logger.setLevel( logging.ERROR )
# logger.setLevel( logging.INFO )
logger.setLevel( logging.DEBUG )
l_fmt = logging.Formatter( '%(levelname)s:%(funcName)s[%(lineno)d] %(message)s' )
l_handler = logging.StreamHandler()
l_handler.setFormatter( l_fmt )
logger.addHandler( l_handler )

import argparse
import logging
import csv
import configparser
import pathlib
import pprint

import key_combo

args = None
keymap = {
    'A': 'X',
    'B': 'Y',
    'C': 'Z',
}

def parse_cmdline():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument( 'keymap_file',
        help='Original SC2 keymap file' )
    defaults = {
        'keymap_file': 'TheCore6g_right_US_qwerty.SC2Hotkeys',
    }
    parser.set_defaults( **defaults )
    args = parser.parse_args()


def parse_keymap( keymap_file ):
    cfg = configparser.ConfigParser( interpolation=None )
    cfg.optionxform = lambda option: option #retain original case of keys
    cfg.read( keymap_file )
    return cfg


def remap_keys( cfg ):
    new_cfg = configparser.ConfigParser( interpolation=None )
    new_cfg.optionxform = lambda option: option #retain original case of keys
    for section in cfg.sections():
        new_cfg.add_section( section )
        # logger.debug( f"SECTION: '{section}'" )
        for command, value in cfg.items( section ):
            # logger.debug( f"cmd: '{command}'" )
            # unique keycombos separated by ','
            key_combos = []
            for c_str in value.split( ',' ):
                kc = key_combo.Key_Combo( c_str )
                # logger.debug( f"\tOLD {kc}" )
                kc.remap( keymap=keymap )
                key_combos.append( kc )
                # logger.debug( f"\tNEW {kc}" )
            combo_strings = ','.join( map( key_combo.Key_Combo.to_str, key_combos ) )
            # logger.debug( f"combo_strings: {combo_strings}" )
            new_cfg.set( section, command, combo_strings )
    return new_cfg


def print_cfg( cfg ):
    for section in cfg.sections():
        print( f"SECTION: '{section}'" )
        for key, value in cfg.items( section ):
            print( f"key: '{key}' value: '{value}'" )



def run():
    pp = pprint.PrettyPrinter(indent=4)
    parse_cmdline()
    cfg = parse_keymap( pathlib.Path( args.keymap_file ) )
    print_cfg( cfg )
    new_cfg = remap_keys( cfg )
    print_cfg( new_cfg )
    #write_output( cfg )


if __name__ == '__main__':
    run()
