#!/usr/bin/python-2.6

from math import pi, sin, cos

PWIDTH=842
PHEIGHT=596
MM = 360/127.0
YEAR = 2*MM
YEAR_TICK = 1*MM
DECADE_TICK = 1.75*MM
CENTURY_TICK = 2.5*MM

# Timeline geometry:
PART1_Y = 0.5
PART1_XMAX = 3.8
PART2_MINY = 1.2
PART2_DELTAY = 0.3

def main():
    ps_header()
    #page1()
    page2()
    ps_trailer()

def ps_header():
    print """
%!PS-Adobe-3.0
%%Creator: Timeline drawing script
%%Title: Timeline-all
%%Pages: 2
%%LanguageLevel: 3
%%Orientation: Landscape
%%DocumentMedia: a4 595 842 80 () ()
%%EndComments
%%BeginProlog
/mm {360 mul 127 div} def
/center {dup stringwidth pop -2 div 0 rmoveto} def
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


# %!PS-Adobe-3.0
# %%Creator: Timeline drawing script
# %%Title: Timeline-all
# %%LanguageLevel: 2
# %%Pages: 1
# %%PageOrder: Ascend
# %%BoundingBox: 0 0 842 596
# %%Orientation: Landscape
# %%PageOrientation: Landscape
# %%EndComments

# %%BeginProlog
# /mm {360 mul 127 div} def
# /center {dup stringwidth pop -2 div 0 rmoveto} def
# %%EndProlog

# %%BeginSetup
# %%Feature: *Resolution 300dpi
# %%PaperSize: a4

# /TheFont /Helvetica findfont def
# /SelectFontSize {1 dict begin /sz exch def TheFont sz scalefont setfont end} def
# %%EndSetup
#     """

def ps_trailer():
    print "%%EOF"

def page1():
    nowx = 0.9 * PWIDTH
    nowy = 0.5 * PHEIGHT

    thenx = nowx - 100*YEAR
    theny = nowy

    start_page("A1",1)

    setlinewidth(0.5*MM)
    newpath()
    moveto(nowx,nowy)
    lineto(thenx,theny)
    coord(thenx,theny+100); print "100 270 90 arcn\n";
    stroke()

    newpath()
    moveto(nowx,nowy+200)
    lineto(thenx,theny+200)
    stroke()

    newpath()
    setlinewidth(0.1*MM)
    for i in range(0,100+1):
        ticksize = ticksize_for(i)
        draw_tick(nowx-i*YEAR, nowy, ticksize, 0)
    stroke()

    for i in range(0,100+1, 10):
        fontsize = fontsize_for(i)
        print "%d SelectFontSize" % fontsize
        moveto(nowx-i*YEAR, nowy+CENTURY_TICK)
        textover(2000-i)
    stroke()

    end_page()


def page2():
    start_page("Overview",2)

    # individual page size:
    scale = 1/4.0
    cm = scale/2.54*72
    pw = 27.5 * cm #scale*PWIDTH
    ph = 20.0 * cm #scale*PHEIGHT

    # Paper sheet grid:
    for i in range(0,4+1):
        newpath()
        moveto(i*pw, 0)
        lineto(i*pw, 4*ph)
        moveto(0,    i*ph)
        lineto(4*pw, i*ph)
        stroke()

    # Bottom part of timeline:
    moveto(PART1_XMAX*pw, PART1_Y*ph)
    ymid = (PART1_Y + PART2_MINY) / 2
    timeline_curve_to_y(PART1_XMAX*pw, PART1_Y*ph, (2000-1500)*scale, -1, ymid*ph)
    timeline_curve_on_to_y("dummy:dyears", 1, PART2_MINY*ph)
#    lineto(PART1_XMAX*pw-200*YEAR*scale, PART2_MINY*ph)
    timeline_curve_to_y(PART1_XMAX*pw-200*YEAR*scale, PART2_MINY*ph,
                        200*scale, 1,
                        (PART2_MINY+PART2_DELTAY*0.5)*ph)
    timeline_curve_on_to_y("dummy:dyears", -1, (PART2_MINY+PART2_DELTAY)*ph)
    timeline_curve_to_y(PART1_XMAX*pw-200*YEAR*scale, (PART2_MINY+PART2_DELTAY)*ph,
                        300*scale, -1,
                        (PART2_MINY+PART2_DELTAY*1.5)*ph)
    timeline_curve_on_to_y("dummy:dyears", 1, (PART2_MINY+PART2_DELTAY*2)*ph)
    stroke()
    for i in range(0,5+1):
        draw_tick((3+0.75)*pw - 100*i*YEAR*scale, 0.5*ph, YEAR_TICK, 0)

    # Far wall outline:
    moveto(5*cm,40*cm)
    rlineto(80*cm,0)
    rlineto(0,40*cm)
    rlineto(-80*cm,0)
    rlineto(0,-40*cm)
    stroke()

    # Into-depth wall:
    moveto(85*cm,40*cm)
    rlineto(10*cm,0)
    rlineto(0,20*cm)
    rlineto(-10*cm,0)
    rlineto(0,-20*cm)
    stroke()

    # Vanishing point and lines thereto:
    moveto(84.75*cm, 45*cm)
    lineto(95*cm,40*cm)

    moveto(84.75*cm, 45*cm)
    lineto(95*cm,60*cm)

    moveto(84.75*cm, 45*cm)
    lineto(95*cm,80*cm)

    moveto(84.75*cm, 45*cm)
    lineto(95*cm,0*cm)

    moveto(84.75*cm, 45*cm)
    lineto(0*cm,0*cm)

    moveto(84.75*cm, 45*cm)
    lineto(0*cm,40*cm)

    moveto(84.75*cm, 45*cm)
    lineto(0*cm,45*cm)
    stroke()

    end_page()

class GState:
    def __init__(self):
        self.curx=0
        self.cury=0
        self.cur_radius=0


gstate = GState()

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
def draw_tick(x,y, ticksize, dir):
    rad_dir = dir / 180.0 * pi
    xsz = ticksize*sin(rad_dir)
    ysz = ticksize*cos(rad_dir)
    moveto(x-xsz,y-ysz)
    rlineto(2*xsz, 2*ysz)
    # moveto(nowx-i*YEAR, nowy-ticksize)
    # lineto(nowx-i*YEAR, nowy+ticksize)


def size(x): print "%.3f " % (x)
def coord(x,y): print "%.2f %.2f " % (x,y)

# A      B    C D     (x0,y0)=A
# -------+.......     |CE| = radius = |BC|
#          \  :       arclen(BE) = BD
#            +E       |BD| = 1/2*pi*radius = 1/2*pi*radius
#                     |CD| = |BD|-|BC| = (1/2*pi-1)*radius
def timeline_curve_to_y(x0,y0, dyears, xdir, ytarget):
    radius = abs(ytarget-y0)
    xD = x0 + xdir*dyears*YEAR
    # Waypoint = C
    xC = xD - xdir*(pi/2-1)*radius
    yC = y0
    # Target = E
    xE = xC
    yE = ytarget
    arct(xC, yC, xE, yE, radius)
    gstate.curx = xE; gstate.cury = yE; gstate.cur_radius = radius

def timeline_curve_on_to_y(dyears, xdir, ytarget):
    # At curx, cury
    arct(gstate.curx,ytarget,
         gstate.curx + xdir * gstate.cur_radius, ytarget,
         gstate.cur_radius)
#    timeline_curve_to_y(x0,y0, dyears, -xdir, ytarget)

def ticksize_for(i):
    if i%10 != 0:  return YEAR_TICK
    if i%100 != 0: return DECADE_TICK
    return CENTURY_TICK

def fontsize_for(i):
    if i%100 != 0: return 10
    return 12

main()
