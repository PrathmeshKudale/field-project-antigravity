from fastapi import APIRouter
from app.retrieval.hybrid import load_demo_chunks

router = APIRouter()


@router.get("/chunks/{chunk_id}")
async def get_chunk(chunk_id: str):
    chunks = load_demo_chunks()
    for c in chunks:
        if c["id"] == chunk_id:
            return c
    return {"detail": "Chunk not found"}
