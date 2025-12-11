import os
import json
from backend.patient.fhir_parser import FHIRParser
from backend.ctkg.importer import FalkorDBImporter

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    input_file = os.path.join(base_dir, "data", "patient", "sample_patient.json")
    output_dir = os.path.join(base_dir, "data", "patient", "import")
    
    with open(input_file, "r") as f:
        bundle = json.load(f)
        
    parser = FHIRParser()
    data = parser.parse_bundle(bundle)
    
    importer = FalkorDBImporter(output_dir)
    importer.generate_csvs(data)
