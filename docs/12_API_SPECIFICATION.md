# API Specification

**Project:** MedRAG
**Document Version:** 1.0
**Sprint:** 0 – Phase 5
**Status:** Draft

---

# 1. Purpose

This document defines the external API contract for MedRAG.

The API is designed following RESTful principles with OpenAPI compatibility and serves as the authoritative specification for backend implementation.

Objectives:

* Stable API contracts
* Consistent request/response formats
* Versioned endpoints
* Predictable error handling
* Easy frontend integration
* Future extensibility

---

# 2. API Design Principles

The API follows these principles:

* Resource-oriented design
* Stateless communication
* JSON payloads
* Explicit versioning
* Strong validation
* Consistent error responses
* Idempotent operations where applicable
* Backward compatibility within major versions

---

# 3. Base URL

```text
/api/v1
```

Future versions:

```text
/api/v2
```

Versioning will be URL-based to simplify client compatibility.

---

# 4. Authentication Strategy

## MVP

No authentication required.

## Future

Support:

* API Keys
* OAuth2
* JWT
* Role-Based Access Control (RBAC)

Authentication middleware should be introduced without changing endpoint semantics.

---

# 5. Standard Response Format

## Success Response

```json
{
  "success": true,
  "data": {},
  "metadata": {},
  "timestamp": "2026-06-18T12:00:00Z"
}
```

## Error Response

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid query.",
    "details": {}
  },
  "timestamp": "2026-06-18T12:00:00Z"
}
```

---

# 6. Health Endpoints

## GET /health

Purpose:

Health check.

Response:

* status
* uptime
* version

---

## GET /ready

Purpose:

Readiness probe.

Checks:

* Qdrant
* LLM provider
* MLflow
* Phoenix

---

## GET /live

Purpose:

Liveness probe for orchestration platforms.

---

# 7. Document Endpoints

## POST /documents/ingest

Starts document ingestion.

Request:

```json
{
  "source": "pubmed",
  "query": "diabetes",
  "max_results": 500
}
```

Response:

```json
{
  "job_id": "uuid",
  "status": "queued"
}
```

---

## GET /documents/{document_id}

Returns metadata for a document.

---

## GET /documents

Supports:

* pagination
* journal filter
* year filter
* keyword filter
* author filter

---

## DELETE /documents/{document_id}

Administrative endpoint.

Marks a document for removal from indexes.

---

# 8. Retrieval Endpoints

## POST /retrieval/search

Purpose:

Retrieve relevant chunks without generation.

Request:

```json
{
  "query": "What are GLP-1 receptor agonists?",
  "top_k": 10,
  "filters": {
    "year": 2025
  }
}
```

Response:

* retrieved chunks
* retrieval scores
* metadata

---

# 9. Generation Endpoints

## POST /generation/answer

Purpose:

Generate an evidence-grounded answer.

Request:

```json
{
  "query": "What are the latest EGFR inhibitors?",
  "top_k": 10
}
```

Response:

```json
{
  "answer": "...",
  "citations": [],
  "retrieved_chunks": [],
  "generation_time_ms": 2150
}
```

---

## POST /generation/stream

Future endpoint.

Supports Server-Sent Events (SSE) for streaming responses.

---

# 10. Evaluation Endpoints

## POST /evaluation/run

Runs evaluation on supplied data.

Request:

* question
* reference answer
* generated answer
* retrieved context

Response:

* RAGAS metrics
* latency
* evaluation ID

---

## GET /evaluation/{evaluation_id}

Returns stored evaluation results.

---

# 11. Experiment Endpoints

## GET /experiments

Returns tracked MLflow experiments.

---

## GET /experiments/{experiment_id}

Returns experiment metadata.

---

# 12. Monitoring Endpoints

## GET /monitoring/traces

Returns recent traces.

---

## GET /monitoring/metrics

Returns:

* latency
* throughput
* token usage
* request counts

---

# 13. Administration Endpoints

## POST /admin/reindex

Starts full reindex.

---

## POST /admin/rebuild-embeddings

Regenerates embeddings.

---

## POST /admin/rebuild-bm25

Rebuilds lexical index.

---

## GET /admin/status

Returns system status.

---

# 14. Pagination

All list endpoints follow:

```json
{
  "items": [],
  "page": 1,
  "page_size": 20,
  "total_items": 542,
  "total_pages": 28
}
```

---

# 15. Filtering

Supported filters:

* publication year
* journal
* author
* keyword
* source
* language

Filters should be composable.

---

# 16. Sorting

Supported sorting:

* relevance
* publication date
* citation count (future)
* journal
* title

---

# 17. Error Codes

| Code                  | Meaning              |
| --------------------- | -------------------- |
| VALIDATION_ERROR      | Invalid request      |
| DOCUMENT_NOT_FOUND    | Unknown document     |
| QUERY_TOO_LONG        | Query exceeds limits |
| RETRIEVAL_FAILED      | Retrieval error      |
| GENERATION_FAILED     | LLM failure          |
| EVALUATION_FAILED     | Evaluation error     |
| INTERNAL_SERVER_ERROR | Unexpected exception |

Errors should be stable across API versions.

---

# 18. Rate Limiting

Future implementation:

Default:

* 60 requests/minute

Administrative endpoints:

* Lower limits

Health endpoints:

* No limit

---

# 19. API Versioning Policy

Breaking changes require:

* New API version
* Migration guide
* Deprecation period

Minor additions should remain backward compatible.

---

# 20. OpenAPI Standards

The backend should automatically expose:

* `/docs`
* `/redoc`
* `/openapi.json`

Descriptions must include:

* request examples
* response examples
* validation rules

---

# 21. Status Codes

| Code | Meaning             |
| ---- | ------------------- |
| 200  | Success             |
| 201  | Created             |
| 202  | Accepted            |
| 204  | No Content          |
| 400  | Bad Request         |
| 404  | Not Found           |
| 409  | Conflict            |
| 422  | Validation Error    |
| 429  | Too Many Requests   |
| 500  | Internal Error      |
| 503  | Service Unavailable |

---

# 22. API Evolution Strategy

Future enhancements include:

* GraphQL gateway
* gRPC internal services
* Streaming APIs
* Batch retrieval endpoints
* Webhooks
* Multi-user support

The API should evolve without breaking existing clients whenever possible.

---

# 23. Endpoint Summary

| Domain         | Endpoints |
| -------------- | --------- |
| Health         | 3         |
| Documents      | 4         |
| Retrieval      | 1         |
| Generation     | 2         |
| Evaluation     | 2         |
| Experiments    | 2         |
| Monitoring     | 2         |
| Administration | 4         |

Total planned endpoints: **20**

---

# 24. Summary

The MedRAG API is designed as a stable, versioned contract between clients and the backend. It emphasizes consistency, observability, and extensibility while remaining straightforward to implement using FastAPI and OpenAPI tooling.
