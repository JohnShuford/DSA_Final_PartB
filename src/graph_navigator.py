import pandas as pd
from weighted_graph import WeightedGraph
from vertex import Vertex


class Navigator:
    def __init__(self, nodes_file, connections_file):
        self.graph = WeightedGraph()
        self.node_data = {}
        self.letter_to_index = {}
        self._load_nodes(nodes_file)
        self._load_connections(connections_file)

    def _load_nodes(self, filename):
        df = pd.read_csv(filename)
        for idx, row in df.iterrows():
            vertex = Vertex(row['Node'])
            self.graph.addVertex(vertex)
            self.letter_to_index[row['Node']] = idx
            self.node_data[row['Node']] = {
                'name': row['Location'],
            }

    def _load_connections(self, filename):
        df = pd.read_csv(filename)
        for _, row in df.iterrows():
            from_idx = self.letter_to_index[row['Node_From']]
            to_idx = self.letter_to_index[row['Node_To']]
            time = row['Travel_Time_Minutes']
            risk = row['Risk_Level']
            self.graph.addEdge(from_idx, to_idx, time, risk)

    def find_route(self, start_letter, end_letter, risk = False):
        start_idx = self.letter_to_index[start_letter]
        end_idx = self.letter_to_index[end_letter]
        return self.graph.shortestPath(start_idx, end_idx, risk)
    
    def print_route_details(self, start_letter, end_letter, risk = False):
        path = self.find_route(start_letter, end_letter, risk)
        letters = self.graph.letters_instead_of_indexes(path)
        total_time = self.graph.total_time(path, risk)
        edge_time = self.graph.pathEdgetimes(path, risk)
        
        print(f"\n{'='*60}")
        if risk == True:
            print(f"Route from {start_letter} to {end_letter} with risk")
        else: 
            print(f"Route from {start_letter} to {end_letter}; no risk")
        print(f"{'='*60}")
        
        print("\nPath (Letters):")
        print(" → ".join(letters))
        
        print("\nPath (Locations):")

        first = letters[0]
        print(f" {first}: {self.node_data[first]['name']} (start)")
        for letter, v in zip(letters[1:], edge_time):
            print(f" {letter}: {self.node_data[letter]['name']} ({round(v, 1)} mins)")
        
        print(f"\nTotal Travel Time: {round(total_time, 1)} minutes")
        print(f"{'='*60}\n")