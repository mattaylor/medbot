from typing import List, Dict

class VectorStore:
    def __init__(self):
        self.index = {}

    def add_texts(self, texts: List[str], metadatas: List[Dict] = None):
        # Mock implementation: just store them
        for i, text in enumerate(texts):
            meta = metadatas[i] if metadatas else {}
            self.index[text] = meta
        print(f"Added {len(texts)} texts to vector store.")

    def search(self, query: str, k: int = 5) -> List[Dict]:
        # Mock implementation: return dummy results
        print(f"Searching for: {query}")
        return [
            {"text": "Study on Metformin for Diabetes", "metadata": {"type": "study", "id": "NCT123"}},
            {"text": "Side effects of Metformin", "metadata": {"type": "drug_info", "id": "DRUG:METFORMIN"}}
        ]
