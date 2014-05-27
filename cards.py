#!/usr/bin/python-2.6

from psutil import ps_header, ps_trailer, setlinewidth, moveto, coord, size, rlineto, stroke, textover
from sys import stderr

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

# Categories:
CATEGORY = {
    'DISC': {'color': 'setDISCcolor'},
    'INV' : {'color': 'setINVcolor'},
    'NAT' : {'color': 'setNATcolor'},
    'HIST': {'color': 'setHISTcolor'},
    'TRAV': {'color': 'setTRAVcolor'},
    'ART' : {'color': 'setARTcolor'}
}


def main(data_filename):
    defs="""
    /relpoint { <<>> begin
    % Input: dx dy
    /dy exch def
    /dx exch def
    currentpoint
    % ... x y
    dy add exch
    dx add exch
    % ... x+dx y+dy
    end } bind def

    /roundbox { <<>> begin
    % Input: w h r
    /r exch def
    /h2 exch 2 div def
    /w2 exch 2 div def
    /nw2 0 w2 sub def
    /nh2 0 h2 sub def
    /savepoint {/sx 2 index def /sy 1 index def} bind def
    /pushpoint {sx sy} bind def

    % Sketch:
    %
    % 6...5...4
    % :       :
    % 7       3
    % :       :
    % 0...1...2

     w2 0 rmoveto                          % p1
     w2   0 relpoint  w2  h2 relpoint savepoint r arct % p1-p2-p3
    pushpoint lineto
      0  h2 relpoint nw2  h2 relpoint savepoint r arct % p3-p4-p5
    pushpoint lineto
    nw2   0 relpoint nw2 nh2 relpoint savepoint r arct % p5-p6-p7
    pushpoint lineto
    0   nh2 relpoint  w2 nh2 relpoint savepoint r arct % p7-p8-p9
    pushpoint lineto
    closepath
    end } bind def

    /setDISCcolor {1.0 0.85 0  setrgbcolor} bind def  % Yellow
    /setINVcolor  {0.4 0.4 0.8 setrgbcolor} bind def  % Blue
    /setNATcolor  {0.1 0.8 0.1 setrgbcolor} bind def  % Green
    /setHISTcolor {0.8 0.0 0.0 setrgbcolor} bind def  % Red
    /setTRAVcolor {0.6 0.2 0.6 setrgbcolor} bind def  % Purple
    /setARTcolor  {0.7 0.3 0.0 setrgbcolor} bind def  % Brown
    """
    ps_header(1, defs)
    #cards_test_page()
    cards_page(data_filename)
    ps_trailer()

def cards_test_page():
    coord(10*MM, 10*MM); print "translate"
    print "12 SelectFontSize"

    setlinewidth(2*MM)
    moveto(0,0)
    coord(30*MM, 40*MM)
    size(5*MM)
    print "roundbox stroke"

    # Yellow-orange:
    print("1.0 0.85 0 setrgbcolor")
    moveto(40*MM,0)
    coord(30*MM, 40*MM)
    size(5*MM)
    print "roundbox stroke"
    moveto((40+15)*MM, (40+3)*MM); textover("Discovery")

    # Blue:
    print("0.4 0.4 0.8 setrgbcolor")
    moveto(80*MM,0)
    coord(30*MM, 40*MM)
    size(5*MM)
    print "roundbox stroke"
    moveto((80+15)*MM, (40+3)*MM); textover("Invention")

    # Green:
    print("0.1 0.8 0.1 setrgbcolor")
    moveto(120*MM,0)
    coord(30*MM, 40*MM)
    size(5*MM)
    print "roundbox stroke"
    moveto((120+15)*MM, (40+3)*MM); textover("Nature")

    # Red:
    print("0.8 0.0 0.0 setrgbcolor")
    moveto(160*MM,0)
    coord(30*MM, 40*MM)
    size(5*MM)
    print "roundbox stroke"
    moveto((160+15)*MM, (40+3)*MM); textover("Event")

    # Purple:
    print("0.6 0.2 0.6 setrgbcolor")
    moveto(200*MM,0)
    coord(30*MM, 40*MM)
    size(5*MM)
    print "roundbox stroke"
    moveto((200+15)*MM, (40+3)*MM); textover("Travel")

    # Brown:
    print("0.7 0.3 0.0 setrgbcolor")
    moveto(240*MM,0)
    coord(30*MM, 40*MM)
    size(5*MM)
    print "roundbox stroke"
    moveto((240+15)*MM, (40+3)*MM); textover("Artefact")

def cards_page(data_filename):
    with open(data_filename) as f:
        for line in f:
            line = line.strip()
            if (line=="") or (line[0] == "#"):
                continue
                #print "Skipping <%s>" % (line,)
            #print "line: %s (first: <%s>)" % (line,line[0])
            toks = line.split(":", 4)
            #print "toks: %s" % (toks,)
            toks = map(lambda x: x.strip(), toks)
            print "toks2: %s" % (toks,)
            if len(toks)<4:
                stderr.write("Format error: <%s>\n" % (line,))
                exit(1)
            catname = toks[0]
            year = toks[1]
            img  = toks[2]
            text = toks[3]
            if not CATEGORY.has_key(catname):
                stderr.write("Unknown category: <%s>\n" % (catname,))
                exit(1)
            category = CATEGORY[catname]

main("cards.dat")
