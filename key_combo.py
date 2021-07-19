import pprint
class Key_Combo(object):
    def __init__( self, raw_val ):
        self._str = raw_val
        parts = self._str.split( '+' )
        self.keycap = parts.pop()
        self.modifiers = parts[:]

    def __repr__( self ):
        mods = '+'.join( self.modifiers )
        return f"<Key_Combo [({mods}) ({self.keycap})]>"
        # return f"<Key_Combo [{self.to_str()}]>"

    def to_str( self ):
        return '+'.join( self.modifiers + [self.keycap] )

    def remap( self, keymap ):
        self.keycap = keymap[ self.keycap ]
