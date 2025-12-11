import json
import os
from typing import List, Dict
from .schema import Study, Condition, Drug, Outcome, Edge, CTKGData

class CTKGParser:
    def __init__(self):
        pass

    def parse_studies(self, studies: List[Dict]) -> CTKGData:
        data = CTKGData()
        
        for study_json in studies:
            protocol = study_json.get("protocolSection", {})
            
            # Study Node
            ident = protocol.get("identificationModule", {})
            nct_id = ident.get("nctId")
            if not nct_id:
                continue
                
            study = Study(
                id=nct_id,
                properties={
                    "title": ident.get("briefTitle", ""),
                    "phase": str(protocol.get("designModule", {}).get("phases", [])),
                    "study_type": protocol.get("designModule", {}).get("studyType", "")
                }
            )
            data.nodes.append(study)
            
            # Conditions
            conditions = protocol.get("conditionsModule", {}).get("conditions", [])
            for cond_name in conditions:
                cond_id = f"COND:{cond_name.upper().replace(' ', '_')}"
                condition = Condition(id=cond_id, properties={"name": cond_name})
                data.nodes.append(condition)
                
                # Edge: Study -> Condition
                data.edges.append(Edge(
                    source_id=study.id,
                    target_id=condition.id,
                    type="STUDIES_CONDITION"
                ))
                
            # Interventions (Drugs)
            interventions = protocol.get("armsInterventionsModule", {}).get("interventions", [])
            for interv in interventions:
                if interv.get("type") == "Drug":
                    drug_name = interv.get("name", "")
                    drug_id = f"DRUG:{drug_name.upper().replace(' ', '_')}"
                    drug = Drug(id=drug_id, properties={"name": drug_name})
                    data.nodes.append(drug)
                    
                    # Edge: Study -> Drug
                    data.edges.append(Edge(
                        source_id=study.id,
                        target_id=drug.id,
                        type="USES_DRUG"
                    ))
            
            # Outcomes
            outcomes = protocol.get("outcomesModule", {}).get("primaryOutcomes", [])
            for i, out in enumerate(outcomes):
                out_measure = out.get("measure", "")
                out_id = f"OUTCOME:{nct_id}:{i}"
                outcome = Outcome(
                    id=out_id,
                    properties={
                        "measure": out_measure,
                        "description": out.get("description", "")
                    }
                )
                data.nodes.append(outcome)
                
                # Edge: Study -> Outcome
                data.edges.append(Edge(
                    source_id=study.id,
                    target_id=outcome.id,
                    type="HAS_OUTCOME"
                ))
                
        return data

if __name__ == "__main__":
    # Test parser
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    input_file = os.path.join(base_dir, "data", "ctkg", "studies_raw.json")
    
    with open(input_file, "r") as f:
        studies = json.load(f)
        
    parser = CTKGParser()
    data = parser.parse_studies(studies)
    
    print(f"Parsed {len(data.nodes)} nodes and {len(data.edges)} edges")
    # Deduplicate nodes by ID
    unique_nodes = {n.id: n for n in data.nodes}
    print(f"Unique nodes: {len(unique_nodes)}")
