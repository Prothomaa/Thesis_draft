class DirectedGraph:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

    def get_neighbors(self, node):
        return [edge[1] for edge in self.edges if edge[0] == node]

    def get_edge_weight(self, edge):
        return edge[2]

    def add_edge(self, edge):
        self.edges.append(edge)

    def remove_edge(self, edge):
        self.edges.remove(edge)

    def contract_cycle(self, cycle):
        new_node = cycle[0]
        for node in cycle[1:]:
            new_edges = [(new_node, neighbor, self.get_edge_weight((node, neighbor))) for neighbor in self.get_neighbors(node) if (node, neighbor) in self.edges]
            self.edges.extend(new_edges)
            self.remove_edge((node, neighbor))
            for neighbor in self.get_neighbors(node) :
                if (node, neighbor) in self.edges:
                    self.nodes.remove(node)

    def expand_contracted_cycles(self):
        for cycle in self.get_contracted_cycles():
            new_node = cycle[0]
            for node in cycle[1:]:
                self.add_edge((new_node, node, self.get_edge_weight((node, new_node))))

    def get_contracted_cycles(self):
        contracted_cycles = []
        for node in self.nodes:
            cycle = self.find_cycle(node)
            if cycle:
                contracted_cycles.append(cycle)
        return contracted_cycles

    def find_cycle(self, node):
        visited = set()
        stack = [node]
        while stack:
            current_node = stack.pop()
            if current_node in visited:
                return [current_node]
            visited.add(current_node)
            for neighbor in self.get_neighbors(current_node):
                if (current_node, neighbor) in self.edges:
                    stack.append(neighbor)
        return None

def find_maximum_spanning_tree(graph):
    maximum_spanning_tree = []
    while graph.nodes:
        current_node = graph.nodes[0]
        heaviest_edge = None
        for neighbor in graph.get_neighbors(current_node):
            edge = (current_node, neighbor, graph.get_edge_weight((current_node, neighbor)))
            if heaviest_edge is None or heaviest_edge[2] < edge[2]:
                heaviest_edge = edge
        maximum_spanning_tree.append(heaviest_edge)
        graph.remove_edge(heaviest_edge)
        contracted_cycle = graph.find_cycle(current_node)
        if contracted_cycle:
            graph.contract_cycle(contracted_cycle)
    return maximum_spanning_tree

# Example usage:

graph = DirectedGraph(["A", "B", "C", "D"], [("A", "B", 10), ("A", "C", 15), ("B", "C", 20), ("C", "D", 20)])

maximum_spanning_tree = find_maximum_spanning_tree(graph)

print(maximum_spanning_tree)