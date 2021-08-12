import key_combo

class Hotkey_Command(object) :
    def __init__( self, cmd, combo_str ):
        self.cmd = cmd
        self.combos = {}
        self.add( combo_str )

    def __repr__( self ):
        combos = ','.join( [ str(k) for k in self.combos.keys() ] )
        return f'{combos}'

    def add( self, raw_str ):
        combos = raw_str.split(',')
        for c in combos:
            new_combo = key_combo.Key_Combo( c )
            self.combos[ new_combo ] = None

    def __iter__( self ):
        return self.combos.keys
