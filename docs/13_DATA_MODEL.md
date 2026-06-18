# Data Model Specification

**Project:** MedRAG
**Document Version:** 1.0
**Sprint:** 0 – Phase 4
**Status:** Draft

---

# 1. Purpose

This document defines the canonical data model for MedRAG.

Every component—including the API, ingestion pipeline, retrieval engine, vector database, evaluation framework, monitoring system, and frontend—must use these models as the authoritative contracts.

The objectives are:

* Establish consistent data contracts
* Minimize implementation ambiguity
* Support modular development
* Enable backward-compatible evolution
* Simplify testing and documentation

---

# 2. Design Principles

The data model follows these principles:

* Single source of truth
* Immutable identifiers
* Strong typing
* Explicit validation
* Version-aware schemas
* Separation of domain and transport models
* Forward-compatible evolution

---

# 3. Entity Relationship Diagram

```text
                    Document
                        │
                 1 ─────┼───── N
                        │
                     Chunk
                        │
                 1 ─────┼───── 1
                        │
                   Embedding
                        │
                        │
User Query ──► RetrievalResult
                        │
                        ▼
                    RerankedChunk
                        │
                        ▼
                     PromptContext
                        │
                        ▼
                      Answer
                        │
          ┌─────────────┼────────────┐
          ▼             ▼            ▼
      Citation     Evaluation    Trace
```

---

# 4. Entity Catalog

| Entity          | Purpose                     |
| --------------- | --------------------------- |
| Document        | Scientific paper            |
| Chunk           | Searchable unit             |
| Embedding       | Dense vector representation |
| RetrievalResult | Retrieved candidates        |
| RerankedChunk   | Final ranked context        |
| Query           | User request                |
| PromptContext   | Context sent to LLM         |
| Answer          | Generated response          |
| Citation        | Source attribution          |
| EvaluationRun   | Quality metrics             |
| ExperimentRun   | MLflow experiment           |
| Trace           | Phoenix trace               |

---

# 5. Document Entity

Represents one biomedical publication.

## Required Fields

| Field            | Type         | Description         |
| ---------------- | ------------ | ------------------- |
| document_id      | UUID         | Internal identifier |
| pmid             | String       | PubMed ID           |
| doi              | String       | DOI                 |
| title            | String       | Paper title         |
| abstract         | String       | Abstract text       |
| authors          | List[String] | Author names        |
| journal          | String       | Journal             |
| publication_date | Date         | Publication date    |
| keywords         | List[String] | Keywords            |
| source           | Enum         | PubMed / PMC        |
| language         | String       | ISO language code   |
| metadata         | Dict         | Additional metadata |
| version          | Integer      | Schema version      |

## Validation Rules

* PMID must be unique.
* DOI must follow DOI syntax.
* Title cannot be empty.
* Publication date cannot be in the future.
* Metadata must be JSON serializable.

---

# 6. Chunk Entity

Represents the smallest retrievable text unit.

## Fields

| Field           | Type    |
| --------------- | ------- |
| chunk_id        | UUID    |
| document_id     | UUID    |
| chunk_index     | Integer |
| section         | String  |
| text            | String  |
| token_count     | Integer |
| character_count | Integer |
| start_offset    | Integer |
| end_offset      | Integer |
| metadata        | Dict    |

## Constraints

* Belongs to exactly one Document.
* Chunk indices must be sequential.
* Token count must be greater than zero.

---

# 7. Embedding Entity

Represents vectorized text.

## Fields

| Field         | Type     |
| ------------- | -------- |
| embedding_id  | UUID     |
| chunk_id      | UUID     |
| model_name    | String   |
| model_version | String   |
| dimension     | Integer  |
| checksum      | String   |
| created_at    | Datetime |

## Notes

The embedding vector itself will be stored in the vector database (Qdrant). The application stores only metadata and references where appropriate.

---

# 8. Query Entity

Represents a user request.

## Fields

| Field        | Type     |
| ------------ | -------- |
| query_id     | UUID     |
| text         | String   |
| filters      | Dict     |
| timestamp    | Datetime |
| user_session | String   |
| request_id   | UUID     |

## Validation

* Query cannot be empty.
* Maximum length configurable.
* Filters must match supported metadata schema.

---

# 9. RetrievalResult Entity

Represents candidates returned by the retrieval pipeline.

## Fields

| Field        | Type    |
| ------------ | ------- |
| query_id     | UUID    |
| chunk_id     | UUID    |
| dense_score  | Float   |
| sparse_score | Float   |
| hybrid_score | Float   |
| rank         | Integer |

## Notes

This entity captures retrieval before reranking.

---

# 10. RerankedChunk Entity

Represents the final ranked context provided to the LLM.

## Fields

| Field        | Type    |
| ------------ | ------- |
| chunk_id     | UUID    |
| rerank_score | Float   |
| final_rank   | Integer |

---

# 11. PromptContext Entity

Represents the complete context assembled for answer generation.

## Fields

| Field            | Type           |
| ---------------- | -------------- |
| prompt_version   | String         |
| retrieved_chunks | List[Chunk]    |
| citations        | List[Citation] |
| token_budget     | Integer        |
| prompt_template  | String         |

---

# 12. Answer Entity

Represents an LLM-generated response.

## Fields

| Field              | Type           |
| ------------------ | -------------- |
| answer_id          | UUID           |
| query_id           | UUID           |
| model              | String         |
| prompt_version     | String         |
| answer_text        | String         |
| citations          | List[Citation] |
| generation_time_ms | Integer        |
| created_at         | Datetime       |

## Constraints

* Every answer must reference at least one citation unless no relevant evidence was found.
* Answers must never fabricate citations.

---

# 13. Citation Entity

Represents a referenced publication.

## Fields

| Field            | Type    |
| ---------------- | ------- |
| citation_id      | UUID    |
| pmid             | String  |
| doi              | String  |
| title            | String  |
| journal          | String  |
| publication_year | Integer |
| url              | String  |

---

# 14. EvaluationRun Entity

Stores automated evaluation metrics.

## Fields

| Field             | Type     |
| ----------------- | -------- |
| evaluation_id     | UUID     |
| query_id          | UUID     |
| faithfulness      | Float    |
| answer_relevancy  | Float    |
| context_precision | Float    |
| context_recall    | Float    |
| latency_ms        | Integer  |
| timestamp         | Datetime |

---

# 15. ExperimentRun Entity

Represents one tracked experiment.

## Fields

| Field           | Type     |
| --------------- | -------- |
| experiment_id   | UUID     |
| embedding_model | String   |
| reranker        | String   |
| llm             | String   |
| prompt_version  | String   |
| metrics         | Dict     |
| git_commit      | String   |
| timestamp       | Datetime |

---

# 16. Trace Entity

Stores request tracing metadata.

## Fields

| Field              | Type    |
| ------------------ | ------- |
| trace_id           | UUID    |
| request_id         | UUID    |
| retrieval_latency  | Integer |
| rerank_latency     | Integer |
| generation_latency | Integer |
| total_latency      | Integer |
| token_usage        | Integer |
| status             | Enum    |

---

# 17. Entity Lifecycles

## Document

Draft → Ingested → Processed → Chunked → Indexed → Active → Archived

## Query

Received → Retrieved → Reranked → Generated → Evaluated → Logged

## Experiment

Created → Running → Completed → Archived

---

# 18. Versioning Strategy

Every persisted entity includes:

* schema version
* created_at
* updated_at (where applicable)

Breaking schema changes require version increments and migration scripts.

---

# 19. Naming Conventions

* UUIDs for internal identifiers
* snake_case for fields
* ISO 8601 timestamps
* UTF-8 encoded text
* UTC timezone for all persisted timestamps

---

# 20. Data Validation Standards

Validation will be implemented using Pydantic v2.

Rules include:

* Required field enforcement
* Type validation
* Length constraints
* Regex validation (DOIs, PMIDs where applicable)
* Enum validation
* Cross-field consistency checks where necessary

---

# 21. Mapping Between Layers

Each entity exists in multiple representations:

| Layer        | Representation          |
| ------------ | ----------------------- |
| Domain       | Business object         |
| API          | Request/response schema |
| Storage      | Database record         |
| Vector Store | Payload metadata        |
| Evaluation   | Benchmark record        |

Mapping between these representations should occur in dedicated mapper components, avoiding leakage of infrastructure concerns into domain models.

---

# 22. Future Extensions

The model is designed to accommodate future entities such as:

* User
* Workspace
* Saved Search
* Collection
* Annotation
* Figure
* Table
* Knowledge Graph Node
* Agent Task
* Conversation History

These additions should extend the model without breaking existing contracts.

---

# 23. Summary

This data model establishes stable, versioned contracts for every major component of MedRAG. It prioritizes consistency, extensibility, and maintainability, ensuring that future implementation work across APIs, retrieval, evaluation, and monitoring is built upon a shared and well-defined foundation.
