
class Comment:
    def __init__( self, begin, end = '\n', multiline = False, continuation = None ):
        self.begin = begin
        self.end = end
        self.multiline = multiline
        self.continuation = continuation

    def match( self, string ):
        blen = len( self.begin )
        elen = len( self.end )
        inside = False
        lineBreak = False
        content = ""

        slen = len( string );
        i = 0;
        while i < slen:
            if not inside:
                if string[ i : i + blen ] == self.begin:
                    i += blen
                    inside = True
                else:
                    i += 1
            else:
                if string[ i : i + elen ] == self.end:
                    if self.multiline:
                        return content;
                    i += elen
                    content += self.end
                    lineBreak = True
                elif lineBreak:
                    if string[ i : i + len( self.continuation ) ] == self.continuation:
                        i += len( self.continuation )
                        lineBreak = False
                    else:
                        return content
                else:
                    content += string[i]
                    i += 1
        return content

haskell = ( Comment( "{- @", "-}", multiline = True ), Comment( "-- @", continuation = "--" ) )
python = ( Comment( "#@", continuation = "#" ), )
perl = python
bash = perl
c89 = ( Comment( "/*@", "*/", multiline = True ), )
c99 = c89 + ( Comment( "//@", continuation = "//" ), )
c = c99
cpp = c99
latex = ( Comment( "%@", continuation = "%" ), )
prolog = c89 + latex
