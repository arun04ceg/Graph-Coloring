import sys
import copy

def parse_file(filename):
    in_file = open(filename)
    first = True
    complete = True
    vertex_info = {}
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
        neighbours_new = set(line[1:])
        neighbours = vertex_info.setdefault(vertex_name, set())
        neighbours.update(neighbours_new)
        len_neighbours = len(neighbours)
        for each_neighbour in neighbours_new:
            neighbours = vertex_info.setdefault(each_neighbour, set())
            neighbours.add(vertex_name)
        if len_neighbours != num_vertices - 1:
            complete = False
        uncolored_vertices_set.update(neighbours_new)
    in_file.close()
    return vertex_info, uncolored_vertices_set, complete

def coloring(vertex_info, uncolored_vertices_set):
    color_map = {}
    color_count = 1
    while uncolored_vertices_set:
        L = copy.copy(uncolored_vertices_set)
        while(L):
            max_vertex = pick_max_vertex(L, color_map, vertex_info)
            color_map[max_vertex] = color_count
            L.remove(max_vertex)
            L.difference_update(vertex_info[max_vertex])
            uncolored_vertices_set.remove(max_vertex)
        color_count += 1
    return color_map, color_count
        
def pick_max_vertex(vertices, color_map, vertex_info):
    max_uncolored_neighbours, max_vertex = -1, "Dummy"
    for each_vertex in vertices:
        neighbours = vertex_info[each_vertex]
        num_uncolored_neighbours = len(neighbours.difference(color_map))
        if num_uncolored_neighbours > max_uncolored_neighbours:
            max_uncolored_neighbours = num_uncolored_neighbours
            max_vertex = each_vertex
    return max_vertex

def cleanup_line(line):
    line = line.strip()
    return line 

def RLF(filename):
    vertex_info, uncolored_vertices_set, complete = parse_file(filename)
    if complete:
        return len(uncolored_vertices_set), len(uncolored_vertices_set)
        sys.exit(2)
    color_map, color_count = coloring(vertex_info, uncolored_vertices_set)
    return color_count -1, len(vertex_info)

if __name__ == "__main__":
    print RLF(sys.argv[1]) 
