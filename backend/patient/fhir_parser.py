import json
from typing import List, Dict
from backend.ctkg.schema import Node, Edge, CTKGData

class FHIRParser:
    def parse_bundle(self, bundle: Dict) -> CTKGData:
        data = CTKGData()
        entries = bundle.get("entry", [])
        
        patient_id = None
        
        for entry in entries:
            resource = entry.get("resource", {})
            res_type = resource.get("resourceType")
            
            if res_type == "Patient":
                patient_id = resource.get("id")
                name = resource.get("name", [{}])[0]
                full_name = f"{name.get('given', [''])[0]} {name.get('family', '')}"
                
                patient = Node(
                    id=f"PATIENT:{patient_id}",
                    label="Patient",
                    properties={
                        "name": full_name,
                        "gender": resource.get("gender", ""),
                        "birthDate": resource.get("birthDate", "")
                    }
                )
                data.nodes.append(patient)
                
            elif res_type == "Condition":
                cond_id = resource.get("id")
                code_text = resource.get("code", {}).get("text", "")
                # Normalize condition name to match CTKG if possible
                # For now, just create a Condition node
                # In a real system, we'd map SNOMED to the same vocabulary as CTKG
                
                # Create a Condition node (or link to existing if we had a shared ID system)
                # Here we assume we link to the same Condition nodes as CTKG
                # So we generate an ID similar to CTKG: COND:NAME_UPPER
                cond_node_id = f"COND:{code_text.upper().replace(' ', '_')}"
                
                # We might not want to create the node if it should exist from CTKG, 
                # but for completeness let's create it or assume it exists.
                # Let's create an edge from Patient to Condition
                
                if patient_id:
                    data.edges.append(Edge(
                        source_id=f"PATIENT:{patient_id}",
                        target_id=cond_node_id,
                        type="HAS_CONDITION"
                    ))
                    
            elif res_type == "MedicationStatement":
                med_text = resource.get("medicationCodeableConcept", {}).get("text", "")
                # Similar logic for drugs
                drug_node_id = f"DRUG:{med_text.upper().replace(' ', '_')}"
                
                if patient_id:
                    data.edges.append(Edge(
                        source_id=f"PATIENT:{patient_id}",
                        target_id=drug_node_id,
                        type="TAKES_DRUG"
                    ))
                    
        return data

if __name__ == "__main__":
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    input_file = os.path.join(base_dir, "data", "patient", "sample_patient.json")
    
    with open(input_file, "r") as f:
        bundle = json.load(f)
        
    parser = FHIRParser()
    data = parser.parse_bundle(bundle)
    
    print(f"Parsed {len(data.nodes)} nodes and {len(data.edges)} edges")
