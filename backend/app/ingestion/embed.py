import numpy as np


class Embedder:
    """Interface for embedding generation."""
    def embed_text(self, text: str) -> list[float]:
        # Local deterministic hash-based embedding for zero-cost replay mode
        np.random.seed(abs(hash(text)) % (2**32))
        vec = np.random.randn(768).astype(float)
        norm = np.linalg.norm(vec)
        return (vec / norm).tolist() if norm > 0 else vec.tolist()


embedder = Embedder()
