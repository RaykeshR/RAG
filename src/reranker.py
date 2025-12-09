from sentence_transformers import CrossEncoder
from langchain_core.documents import Document as LangchainDocument
from typing import List

class Reranker:
    def __init__(self, model_name="cross-encoder/ms-marco-TinyBERT-L-2"):
        self.model = CrossEncoder(model_name)

    def rerank(self, query: str, documents: List[LangchainDocument]) -> List[LangchainDocument]:
        if not documents:
            return []

        # Create pairs of (query, document_content) for the cross-encoder
        sentence_pairs = [[query, doc.page_content] for doc in documents]
        
        # Predict scores
        scores = self.model.predict(sentence_pairs)
        
        # Add scores to document metadata and sort
        for doc, score in zip(documents, scores):
            # doc.metadata['rerank_score'] = score
            doc.metadata['rerank_score'] = float(score) # Conversion explicite en float Python
        
        documents.sort(key=lambda x: x.metadata['rerank_score'], reverse=True)
        
        return documents