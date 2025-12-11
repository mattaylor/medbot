from backend.graph.updater import GraphUpdater
from backend.rag.vector_store import VectorStore
from backend.rag.llm import LLMClient

class RAGEngine:
    def __init__(self):
        self.updater = GraphUpdater()
        self.vector_store = VectorStore()
        self.llm = LLMClient()

    def query(self, text: str, patient_id: str = None) -> str:
        # 1. Retrieve relevant context from Vector Store
        context_docs = self.vector_store.search(text)
        context_str = "\n".join([d["text"] for d in context_docs])
        
        # 2. Construct prompt
        prompt = f"Context:\n{context_str}\n\nPatient ID: {patient_id}\nQuery: {text}\n\nAnswer:"
        
        # 3. Generate response
        response = self.llm.generate(prompt)
        return response

    def update_patient(self, patient_id: str, data: dict) -> str:
        update_type = data.get("type")
        if update_type == "observation":
            return self.updater.add_observation(patient_id, data.get("text"), data.get("date"))
        elif update_type == "adverse_event":
            return self.updater.add_adverse_event(patient_id, data.get("event"), data.get("drug_id"))
        elif update_type == "phq9":
            return self.updater.process_phq9(patient_id, int(data.get("score", 0)))
        else:
            return f"Unknown update type: {update_type}"
