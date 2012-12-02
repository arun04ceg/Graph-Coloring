import sys
import copy

def parse_file(filename):
    in_file = open(filename)
    first = True
    complete = True
    vertex_info = {}
    dsat = {}
    uncolored_vertices_set = set()
    for line in in_file:
        if line.startswith("#"):
            continue
        line = cleanup_line(line)
        if first:
            num_vertices, num_edges = line.split(" ")
            num_vertices, num_edges = int(num_vertices), int(num_edges)
            first = False
            continue
        line = line.split(" ")
        vertex_name = line[0]
        new_neighbours = set(line[1:])
        num_neighbours = len(new_neighbours)
      
        neighbours = vertex_info.setdefault(vertex_name, set())
        neighbours.update(new_neighbours)
        if num_neighbours != num_vertices - 1:
            complete = False

        for each_neighbour in new_neighbours:
            neighbours = vertex_info.setdefault(each_neighbour, set())
            neighbours.add(vertex_name)

        uncolored_vertices_set.add(vertex_name)
        uncolored_vertices_set.update(new_neighbours)
        dsat[vertex_name] = num_neighbours
    in_file.close()

    max_degree, max_vertex = -1, "Dummy"
    for vertex, neighbours in vertex_info.iteritems():
        num_neighbours = len(neighbours)
        dsat[vertex_name] = num_neighbours
        if num_neighbours > max_degree:
            max_degree = num_neighbours 
            max_vertex = vertex_name
    return vertex_info, uncolored_vertices_set, complete, max_vertex, dsat, num_vertices

def coloring(vertex_info, uncolored_vertices_set, max_vertex, dsat):
    color_map = {}
    color_set = set([1])
    color_map[max_vertex] = min(color_set)
    uncolored_vertices_set.remove(max_vertex)
    update_dsat(dsat, max_vertex, vertex_info, color_map)
    while(uncolored_vertices_set):
        max_vertex = get_max_dsat_vertex(dsat, vertex_info, uncolored_vertices_set)
        neighbours = vertex_info[max_vertex]
        max_color = -1
        for each_neighbour in neighbours:
            color = color_map.get(each_neighbour, 0)
            if color > max_color:
                max_color = color
        if max_color == max(color_set):
            color_set.add(max_color + 1)
        color_map[max_vertex] = max_color + 1
        uncolored_vertices_set.remove(max_vertex)
        update_dsat(dsat, max_vertex, vertex_info, color_map)
    return color_map, max(color_set) 
       
def update_dsat(dsat, vertex, vertex_info, color_map):
    neighbours = vertex_info[vertex]
    for each_neighbour in neighbours:
        distinct_colors_set = set()
        for each_neighbour_neighbour in vertex_info[each_neighbour]:
             color = color_map.get(each_neighbour_neighbour, 0)
             if not color:
                 continue
             distinct_colors_set.add(color)
        if len(distinct_colors_set) > 0:
            dsat[each_neighbour] = len(distinct_colors_set)   

def get_max_dsat_vertex(dsat, vertex_info, uncolored_vertices_set):
    max_dsat_vertex, max_dsat_degree, max_dsat = "Dummy", -1, -1
    for vertex, dsat_val in dsat.iteritems():
        if vertex not in uncolored_vertices_set:
            continue
        if dsat_val > max_dsat:
            max_dsat = dsat_val
            max_dsat_vertex = vertex
        if dsat_val == max_dsat:
            if max_dsat_degree < len(vertex_info[vertex]):
                max_dsat_degree = len(vertex_info[vertex])
                max_dsat = dsat_val
                max_dsat_vertex = vertex
    return max_dsat_vertex

def cleanup_line(line):
    line = line.strip()
    return line 

def dsatur(filename):
    vertex_info, uncolored_vertices_set, complete, max_vertex, dsat, num_vertices = parse_file(filename)
    if complete:
        return len(uncolored_vertices_set), num_vertices
        sys.exit(2)
    color_map, color_count = coloring(vertex_info, uncolored_vertices_set, max_vertex, dsat)
    return color_count, len(vertex_info)

if __name__ == "__main__":
    print dsatur(sys.argv[1])
