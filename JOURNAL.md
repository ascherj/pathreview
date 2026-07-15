## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/80

**Issue title:** DELETE /profiles/{profile_id} doesn't cascade to delete associated reviews and embeddings

**Tier:** [ ] Tier 1  [x] Tier 2  [ ] Tier 3

**Problem summary:**
When a profile is deleted via `DELETE /profiles/{profile_id}`, the vector store embeddings tied to that profile's ingested sources are never cleaned up. The DB side is actually already handled — `profile_service.delete_profile()` explicitly deletes the profile's `Review` and `IngestedSource` rows, and both ORM cascade and FK `ON DELETE CASCADE` are configured on those models. The real gap is in `core/services/profile_service.py`: it never calls into `rag/retriever/vector_store.py` to remove the corresponding Chroma collection (`profile_{profile_id}`), so embeddings are orphaned in the vector store after a profile is deleted. A successful fix adds vector-store cleanup to the delete path (likely a new `delete_collection` method on `VectorStore`, wired into `delete_profile()`), with tests covering the deletion.

**Branch name:** fix/80-delete-remaining-records

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger
