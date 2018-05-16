import mdl
from display import *
from matrix import *
from draw import *


def sanitize(command):
    if (command[0] == "rotate" or command[0] =="save" or command == "display"):
        return command
    ret = [command[0]]
    i = 1
    while i < len(command):
        if isinstance(command[i], float):
            ret.append(command[i])
        i+=1
    return tuple(ret)



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
    polygons = new_matrix()
    ident( polygons )

    systems = [ [x[:] for x in polygons] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    polygons = []
    step_3d = 30

    edges = []

    p = mdl.parseFile(filename)
    
    if p:
        (commands, symbols) = p
        for each in commands:
            each  = sanitize(each)
            if each[0] == "sphere":
                add_sphere(polygons,
                           float(each[1]), float(each[2]), float(each[3]),
                           float(each[4]), step_3d)
                matrix_mult( systems[-1], polygons )
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                polygons = []
            elif each[0] == "torus":
                add_torus(polygons,
                      float(each[1]), float(each[2]), float(each[3]),
                      float(each[4]), float(each[5]), step_3d)
                matrix_mult( systems[-1], polygons )
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                polygons = []
            elif each[0] == "box":

                add_box(polygons,
                    float(each[1]), float(each[2]), float(each[3]),
                    float(each[4]), float(each[5]), float(each[6]))
                matrix_mult( systems[-1], polygons )
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                polygons = []
            elif each[0] == "line":
                add_edge( edges,
                      float(each[1]), float(each[2]), float(each[3]),
                      float(each[4]), float(each[5]), float(each[6]) )
                matrix_mult( systems[-1], edges )
                draw_lines(edges, screen, zbuffer, color)
                edges = []
            elif each[0] == "move":
                t = make_translate(float(each[1]), float(each[2]), float(each[3]))
                matrix_mult( systems[-1], t )
                systems[-1] = [ x[:] for x in t]
            elif each[0] == "scale":
                t = make_scale(float(each[1]), float(each[2]), float(each[3]))
                matrix_mult( systems[-1], t )
                systems[-1] = [ x[:] for x in t]
            elif each[0] == "rotate":
                theta = float(each[2]) * (math.pi / 180)
                if each[1] == 'x':
                    t = make_rotX(theta)
                elif each[1] == 'y':
                    t = make_rotY(theta)
                else:
                    t = make_rotZ(theta)
                matrix_mult( systems[-1], t )
                systems[-1] = [ x[:] for x in t]
            elif each[0] == "push":
                systems.append( [x[:] for x in systems[-1]] )
            elif each[0] == "pop":
                systems.pop()
            elif each[0] == "save":
                save_extension(screen, each[1]+each[2])
            elif each[0] == "display":
                display(screen)

    else:
        print "Parsing failed."
        return
