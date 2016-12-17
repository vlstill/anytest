import os
import sys
import importlib
root = os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) )
if root not in sys.path:
    sys.path.append( root )
import utils.meta as meta

class LoaderError ( Exception ):

    def __init__( self, message ):
        self.message = message

def load( filename, searchPath = [] ):
    oldpath = sys.path
    try:
        sys.path.extend( searchPath )
        importlib.invalidate_caches() # ensure that files change after this is loaded work

        filedir = os.path.dirname( os.path.abspath( filename ) )
        inc = searchPath + [ os.path.join( root, "include" ) ]
        if os.path.isabs( filename ):
            inc.insert( 0, filedir )
        elif os.path.exists( filename ):
            inc.insert( 0, os.path.curdir )
        else:
            for p in inc:
                if os.path.exists( os.path.join( p, filename ) ):
                    filename = os.path.join( p, filename )
                    break

        if not os.path.exists( filename ):
            raise LoaderError( "File not found: " + filename )
        settings = meta.parse( filename, includes = inc )
        
        if "eval" not in settings:
            raise LoaderError( "Evaluator not set: missing 'eval' field in test settings." )

    finally:
        sys.path = oldpath

