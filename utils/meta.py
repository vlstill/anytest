import yaml
import os
import sys
root = os.path.dirname( os.path.dirname( os.path.abspath( __file__ ) ) )
if root not in sys.path:
    sys.path.append( root )
import utils.comments as comments

fileComments = { "hs" : comments.haskell
               , "c" : comments.c
               , "cpp" : comments.cpp
               , "py" : comments.python
               , "pl" : comments.perl
               , "pro" : comments.prolog
               , "prolog" : comments.prolog
               }


def include( base, path ):
    if base is None:
        return {}
    if path is None:
        return base

    if isinstance( base, dict ):
        while True:
            inc = base.get( "_include" )
            if inc is None:
                break
            if inc == []:
                del base[ "_include" ]
                break
            if not isinstance( inc, list ):
                inc = [ inc ]

            idict = None
            for p in path:
                full = os.path.join( p, inc[0] )
                print( full )
                if os.path.exists( full ):
                    idict = parse( full, includes = path )
            assert isinstance( idict, dict )

            base[ "_include" ] = inc[1:]
            base = dict( list( idict.items() ) + list( base.items() ) )

        for k, v in base.items():
            base[ k ] = include( v, path )
        return base

    elif isinstance( base, list ):
        return [ include( x, path ) for x in base ]

    return base


def parse( filename, comments = None, includes = None ):
    if comments is None:
        ext = os.path.splitext( filename )[1][1:]
        comments = fileComments.get( ext )

    with open( filename, "r" ) as f:
        data = f.read()
        if comments is None:
            return include( yaml.load( data ), includes )

        for c in comments:
            p = c.match( data )
            if p != "":
                return include( yaml.load( p ), includes )
    return {}


