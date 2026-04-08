import json
import os
import logging
import faiss
import numpy as np
from config import RAG_METADATA_FILE, FAISS_INDEX_FILE, RAG_TOP_K, RAG_SIMILARITY_THRESHOLD
from embeddings_utils import embed_text

logger = logging.getLogger(__name__)

class FAISSRetriever:
    def __init__(self):
        self.metadata = self.load_metadata()
        self.index = self.load_index()

        logger.info(
            "FAISSRetriever initialized | metadata_count=%s | index_loaded=%s",
            len(self.metadata),
            self.index is not None
        )



    def load_metadata(self):
        if not os.path.exists(RAG_METADATA_FILE):
            logger.warning("Retriever metadata file not found: %s", RAG_METADATA_FILE)
            return []

        with open(RAG_METADATA_FILE, "r", encoding="utf-8") as file:
            metadata = json.load(file)

            logger.info("Retriever metadata loaded successfully | metadata_count=%s", len(metadata))
            return metadata
        


    def load_index(self):
        if not os.path.exists(FAISS_INDEX_FILE):
            logger.warning("FAISS index file not found: %s", FAISS_INDEX_FILE)
            return None

        index = faiss.read_index(FAISS_INDEX_FILE)
        logger.info("FAISS index loaded successfully")
        return index



    def retrieve(self, query, top_k = RAG_TOP_K):
        logger.info(
            "retriever_stage=retrieve_start query_length=%s top_k=%s similarity_threshold=%s",
            len(query.strip()),
            top_k,
            RAG_SIMILARITY_THRESHOLD
        )

        if not self.metadata or self.index is None:
            logger.warning(
                "retriever_stage=retrieve_skipped reason=missing_metadata_or_index metadata_count=%s index_loaded=%s",
                len(self.metadata),
                self.index is not None
            )
            return []

        query_embedding = embed_text(query)
        query_vector = np.array([query_embedding], dtype="float32")

        # normalize for cosine similarity
        faiss.normalize_L2(query_vector)

        distances, indices = self.index.search(query_vector, top_k)

        logger.info(
            "retriever_stage=faiss_search_done raw_scores=%s raw_indices=%s",
            distances[0].tolist(),
            indices[0].tolist()
        )

        results = []


        for score, idx in zip(distances[0], indices[0]):
            if idx < 0 or idx >= len(self.metadata):
                logger.info(
                    "retriever_stage=chunk_skipped reason=invalid_index idx=%s score=%s",
                    idx,
                    round(float(score), 4)
                )
                continue
            
            similarity_score = float(score)
            if similarity_score < RAG_SIMILARITY_THRESHOLD:
                logger.info(
                    "retriever_stage=chunk_skipped reason=below_threshold chunk_id=%s score=%s threshold=%s",
                    self.metadata[idx]["id"],
                    round(similarity_score, 4),
                    RAG_SIMILARITY_THRESHOLD
                )
                continue 
            
            chunk = self.metadata[idx]

            results.append({
                "id": chunk["id"],
                "title": chunk["title"],
                "content": chunk["content"],
                "score": round(float(score), 4)
            })

        logger.info(
        "retriever_stage=retrieve_done returned_count=%s",
        len(results)
        )

        return results