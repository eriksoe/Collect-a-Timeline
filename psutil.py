PWIDTH=842
PHEIGHT=596
MM = 360/127.0


def ps_header(page_count=1, prolog=""):
    print """%!PS-Adobe-3.0
%%Creator: Timeline drawing script
%%Title: Timeline-all
%%Pages: """+("%d".format(page_count))+"""
%%LanguageLevel: 3
%%Orientation: Landscape
%%DocumentMedia: a4 595 842 80 () ()
%%EndComments
%%BeginProlog
/mm {360 mul 127 div} def
/center {dup stringwidth pop -2 div 0 rmoveto} def
"""+prolog+"""
%%EndProlog
%%BeginSetup
%%Feature: *Resolution 300dpi
%%PaperSize: a4
  % A4, rotated 90 degrees ACW
  << /PageSize [595 842] /Orientation 3 >> setpagedevice
  90 rotate 0 -595 translate

/TheFont /Helvetica findfont def
/SelectFontSize {1 dict begin /sz exch def TheFont sz scalefont setfont end} def
%%EndSetup
"""

def ps_trailer():
    print "%%EOF"

class GState:
    def __init__(self):
        self.curx=0
        self.cury=0
        self.cur_radius=0


gstate = GState()


def size(x): print "%.3f " % (x)
def coord(x,y): print "%.2f %.2f " % (x,y)

def start_page(name,nr): print "%%%%Page: %s %d\n" % (name,nr)
def end_page(): print "showpage\n\n"

def setlinewidth(lw): size(lw); print "setlinewidth "
def newpath(): print "newpath "
def moveto(x,y): coord(x,y); print "moveto "
def lineto(x,y): coord(x,y); print "lineto "
def rlineto(x,y): coord(x,y); print "rlineto "
def arct(x1,y1,x2,y2, r): coord(x1,y1); coord(x2,y2); size(r); print "arct "
def stroke(): print "stroke\n"

def textover(s): print "(%s) center show" % s
