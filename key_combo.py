class Key_Combo(object):
    def __init__( self, raw_val ):
        parts = raw_val.split( '+' )
        self.keycap = parts.pop()
        self.modifiers = sorted(parts[:])


    def __str__( self ):
        return '+'.join( self.modifiers + [ self.keycap ] )
    __repr__ = __str__


    def __eq__( self, other ):
        return str( self ) == str( other )


    def __hash__( self ):
        return hash( str( self ) )


    def remap( self, keymap ):
        self.keycap = keymap[ self.keycap ]
