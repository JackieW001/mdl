import mdl
from display import *
from matrix import *
from draw import *

stack = []


def run(filename):
    """
    This function runs an mdl script
    """
    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [0,
              255,
              255]]
    areflect = [0.1,
                0.1,
                0.1]
    dreflect = [0.5,
                0.5,
                0.5]
    sreflect = [0.5,
                0.5,
                0.5]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    systems = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    polygons = []
    step_3d = 20

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
        for tup in commands:
            line = tup[0]
            if line == 'sphere':
                #print 'SPHERE\t' + str(tup)
                add_sphere(polygons,
                       float(tup[1]), float(tup[2]), float(tup[3]),
                       float(tup[4]), step_3d)
                matrix_mult( systems[-1], polygons )
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                polygons = []

            elif line == 'torus':
                #print 'TORUS\t' + str(tup)
                add_torus(polygons,
                          float(tup[1]), float(tup[2]), float(tup[3]),
                          float(tup[4]), float(tup[5]), step_3d)
                matrix_mult( systems[-1], polygons )
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                polygons = []

            elif line == 'box':
                #print 'BOX\t' + str(tup)
                add_box(polygons,
                        float(tup[1]), float(tup[2]), float(tup[3]),
                        float(tup[4]), float(tup[5]), float(tup[6]))
                matrix_mult( systems[-1], polygons )
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                polygons = []
                
            elif line == 'circle':
                #print 'CIRCLE\t' + str(tup)
                add_circle(edges,
                           float(tup[1]), float(tup[2]), float(tup[3]),
                           float(tup[4]), step)
                matrix_mult( systems[-1], edges )
                draw_lines(edges, screen, zbuffer, color)
                edges = []
                
            elif line == 'hermite' or line == 'bezier':
                #print 'curve\t' + line + ": " + str(tup)
                add_curve(edges,
                          float(tup[1]), float(tup[2]),
                          float(tup[3]), float(tup[4]),
                          float(tup[5]), float(tup[6]),
                          float(tup[7]), float(tup[8]),
                          step, line)
                matrix_mult( systems[-1], edges )
                draw_lines(edges, screen, zbuffer, color)
                edges = []
                
            elif line == 'line':
                #print 'LINE\t' + str(tup)
                
                add_edge( edges,
                          float(tup[1]), float(tup[2]), float(tup[3]),
                          float(tup[4]), float(tup[5]), float(tup[6]) )
                matrix_mult( systems[-1], edges )
                draw_lines(eges, screen, zbuffer, color)
                edges = []
                
            elif line == 'scale':
                #print 'SCALE\t' + str(tup)
                t = make_scale(float(tup[0]), float(tup[1]), float(tup[2]))
                matrix_mult( systems[-1], t )
                systems[-1] = [ x[:] for x in t]
                
            elif line == 'move':
                #print 'MOVE\t' + str(tup)
                t = make_translate(float(tup[1]), float(tup[2]), float(tup[3]))
                matrix_mult( systems[-1], t )
                systems[-1] = [ x[:] for x in t]
                
            elif line == 'rotate':
                #print 'ROTATE\t' + str(tup)
                theta = float(tup[2]) * (math.pi / 180)
                if tup[1] == 'x':
                    t = make_rotX(theta)
                elif tup[1] == 'y':
                    t = make_rotY(theta)
                else:
                    t = make_rotZ(theta)
                matrix_mult( systems[-1], t )
                systems[-1] = [ x[:] for x in t]
                    
            elif line == 'push':
                systems.append( [x[:] for x in systems[-1]] )
                
            elif line == 'pop':
                systems.pop()
                
            elif line == 'display' or line == 'save':
                if line == 'display':
                    display(screen)
                else:
                    save_extension(screen, tup[1]+str(tup[2]))
                
    else:
        print "Parsing failed."
        return
