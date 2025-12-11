import csv
import os
from typing import List
from .schema import Node, Edge, CTKGData
from .parser import CTKGParser
import json

class FalkorDBImporter:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_csvs(self, data: CTKGData):
        # Group nodes by label
        nodes_by_label = {}
        for node in data.nodes:
            if node.label not in nodes_by_label:
                nodes_by_label[node.label] = []
            nodes_by_label[node.label].append(node)

        # Write Node CSVs
        for label, nodes in nodes_by_label.items():
            if not nodes:
                continue
            
            # Determine all property keys
            prop_keys = set()
            for node in nodes:
                prop_keys.update(node.properties.keys())
            prop_keys = sorted(list(prop_keys))
            
            filename = os.path.join(self.output_dir, f"{label}.csv")
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                # Header: :ID, prop1, prop2, ..., :LABEL
                header = [":ID"] + prop_keys + [":LABEL"]
                writer.writerow(header)
                
                for node in nodes:
                    row = [node.id] + [node.properties.get(k, "") for k in prop_keys] + [label]
                    writer.writerow(row)
            print(f"Generated {filename} with {len(nodes)} nodes")

        # Write Edge CSV
        # For simplicity, putting all edges in one file, or group by type
        # FalkorDB loader often prefers separate files per relationship type if properties differ
        edges_by_type = {}
        for edge in data.edges:
            if edge.type not in edges_by_type:
                edges_by_type[edge.type] = []
            edges_by_type[edge.type].append(edge)
            
        for rel_type, edges in edges_by_type.items():
            filename = os.path.join(self.output_dir, f"REL_{rel_type}.csv")
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                # Header: :START_ID, :END_ID, :TYPE
                # Add properties if needed
                header = [":START_ID", ":END_ID", ":TYPE"]
                writer.writerow(header)
                
                for edge in edges:
                    row = [edge.source_id, edge.target_id, rel_type]
                    writer.writerow(row)
            print(f"Generated {filename} with {len(edges)} edges")

if __name__ == "__main__":
    # Test importer
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    input_file = os.path.join(base_dir, "data", "ctkg", "studies_raw.json")
    output_dir = os.path.join(base_dir, "data", "ctkg", "import")
    
    with open(input_file, "r") as f:
        studies = json.load(f)
        
    parser = CTKGParser()
    data = parser.parse_studies(studies)
    
    importer = FalkorDBImporter(output_dir)
    importer.generate_csvs(data)
