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
    print """%!PS-Adobe-3.0
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
    gsave()
    setlinewidth(0.02*MM)
    for i in range(0,4+1):
        newpath()
        moveto(i*pw, 0)
        lineto(i*pw, 4*ph)
        moveto(0,    i*ph)
        lineto(4*pw, i*ph)
        stroke()
    grestore()

    # Bottom part of timeline:
    moveto(PART1_XMAX*pw, PART1_Y*ph)
    ymid = (PART1_Y + PART2_MINY) / 2
    timeline_curve_to_y(PART1_XMAX*pw, PART1_Y*ph, 1500,2000, -1, ymid*ph, scale)
    curve_on_to_y("dummy:dyears", 1, PART2_MINY*ph)
    curve_to_y(PART1_XMAX*pw-200*YEAR*scale, PART2_MINY*ph,
                        200*YEAR*scale, 1,
                        (PART2_MINY+PART2_DELTAY*0.5)*ph)
    curve_on_to_y("dummy:dyears", -1, (PART2_MINY+PART2_DELTAY)*ph)
    curve_to_y(PART1_XMAX*pw-200*YEAR*scale, (PART2_MINY+PART2_DELTAY)*ph,
                        300*YEAR*scale, -1,
                        (PART2_MINY+PART2_DELTAY*1.5)*ph)
    curve_on_to_y("dummy:dyears", 1, (PART2_MINY+PART2_DELTAY*2)*ph)
    stroke()
    for i in range(0,5+1):
        draw_tick((3+0.75)*pw - 100*i*YEAR*scale, 0.5*ph, YEAR_TICK, 0)

    # Far wall outline:
    depth = 40*100*cm
    far_wall_width = 50*80*cm
    far_wall_height = 50*40*cm
    floor_z = (40-100)*cm
    rect3d((95*cm,floor_z, depth), (0,far_wall_height, 0), (-far_wall_width,0, 0))
    stroke()
    # moveto(5*cm,40*cm)
    # rlineto(80*cm,0)
    # rlineto(0,40*cm)
    # rlineto(-80*cm,0)
    # rlineto(0,-40*cm)
    # stroke()

    # Into-depth wall:
    near_wall_depth = 10*cm
    # - Corner:
    moveto3d(95*cm,40*cm, 0)
    lineto3d(95*cm,40*cm, near_wall_depth)
    stroke()
    # rect3d((95*cm,40*cm, 0), (0,20*cm, 0), (0,0, depth))
    rect3d((95*cm,floor_z, 0), (0,300*cm, 0), (0,0, depth))
    # moveto(85*cm,40*cm)
    # rlineto(10*cm,0)
    # rlineto(0,20*cm)
    # rlineto(-10*cm,0)
    # rlineto(0,-20*cm)
    # stroke()

    # Near wall top:
    rect3d((95*cm,40*cm, 0), (-100*cm, 0, 0), (0,0, near_wall_depth))


    rect3d((95*cm,40*cm, 0), (0,20*cm, 0), (0,0, depth))
    rect3d((95*cm,40*cm, 0), (0,100*cm, 0), (0,0, depth))

    rect3d((95*cm,40*cm, depth), (0,20*cm, 0), (-far_wall_width,0, 0))
    # moveto3d(95*cm,40*cm, 0)
    # lineto3d(95*cm,40*cm, 10*100*cm)
    # moveto3d(95*cm,60*cm, 0)
    # lineto3d(95*cm,60*cm, 10*100*cm)
    # rlineto(10*cm,0)
    # rlineto(0,20*cm)
    # rlineto(-10*cm,0)
    # rlineto(0,-20*cm)
    stroke()

    # Vanishing point and lines thereto:
    # moveto(84.75*cm, 45*cm)
    # lineto(95*cm,40*cm)

    # moveto(84.75*cm, 45*cm)
    # lineto(95*cm,60*cm)

    # moveto(84.75*cm, 45*cm)
    # lineto(95*cm,80*cm)

    # moveto(84.75*cm, 45*cm)
    # lineto(95*cm,0*cm)

    # moveto(84.75*cm, 45*cm)
    # lineto(0*cm,0*cm)

    # moveto(84.75*cm, 45*cm)
    # lineto(0*cm,40*cm)

    # moveto(84.75*cm, 45*cm)
    # lineto(0*cm,45*cm)
    # stroke()

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

def gsave(): print "save\n"
def grestore(): print "restore\n"



def textover(s): print "(%s) center show" % s
def draw_tick(x,y, ticksize, dir):
    rad_dir = dir / 180.0 * pi
    xsz = ticksize*sin(rad_dir)
    ysz = ticksize*cos(rad_dir)
    moveto(x-xsz,y-ysz)
    rlineto(2*xsz, 2*ysz)
    # moveto(nowx-i*YEAR, nowy-ticksize)
    # lineto(nowx-i*YEAR, nowy+ticksize)


#========== 3D graphics: ========================================
SCALE = 1/4.0
CM = SCALE/2.54*72
def vanishing_point():
    return (84.75*CM, 45*CM)
def near_plane_depth(): return 80*CM
def convert3d(x,y,z):
    (x0,y0) = (x,y)
    # Depth=0 is the near plane.
    (vx,vy) = vanishing_point();
    npz = near_plane_depth()
    x -= vx; y -= vy
    d = 1 + z/npz
    x /= d; y /= d
    x += vx; y += vy
    print "%% %s -> %s" % ((x0,y0,z), (x,y))
    return (x,y)
def moveto3d(x,y,z):
    (x,y) = convert3d(x,y,z)
    moveto(x,y)
def lineto3d(x,y,z):
    (x,y) = convert3d(x,y,z)
    lineto(x,y)

def rect3d(p, v1,v2):
    (x,y,z) = p
    (dx1,dy1,dz1) = v1
    (dx2,dy2,dz2) = v2
    moveto3d(x,y,z)
    lineto3d(x+dx1, y+dy1, z+dz1)
    lineto3d(x+dx1+dx2, y+dy1+dy2, z+dz1+dz2)
    lineto3d(x+dx2, y+dy2, z+dz2)
    lineto3d(x,y,z)
#================================================================


def size(x): print "%.3f " % (x)
def coord(x,y): print "%.2f %.2f " % (x,y)

def timeline_curve_to_y(x0,y0, t0, t1, xdir, ytarget, scale):
    curve_to_y(x0,y0, (t1-t0)*YEAR*scale, xdir, ytarget)

# A      B    C D     (x0,y0)=A
# -------+.......     |CE| = radius = |BC|
#          \  :       arclen(BE) = BD
#            +E       |BD| = 1/2*pi*radius = 1/2*pi*radius
#                     |CD| = |BD|-|BC| = (1/2*pi-1)*radius
def curve_to_y(x0,y0, length, xdir, ytarget):
    radius = abs(ytarget-y0)
    xD = x0 + xdir*length
    # Waypoint = C
    xC = xD - xdir*(pi/2-1)*radius
    yC = y0
    # Target = E
    xE = xC
    yE = ytarget
    arct(xC, yC, xE, yE, radius)
    gstate.curx = xE; gstate.cury = yE; gstate.cur_radius = radius

def curve_on_to_y(dyears, xdir, ytarget):
    # At curx, cury
    arct(gstate.curx,ytarget,
         gstate.curx + xdir * gstate.cur_radius, ytarget,
         gstate.cur_radius)
#    curve_to_y(x0,y0, dyears, -xdir, ytarget)

def ticksize_for(i):
    if i%10 != 0:  return YEAR_TICK
    if i%100 != 0: return DECADE_TICK
    return CENTURY_TICK

def fontsize_for(i):
    if i%100 != 0: return 10
    return 12

main()
