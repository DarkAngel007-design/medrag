# Evaluation Plan

**Project:** MedRAG
**Version:** 1.0

---

# 1. Purpose

Evaluation is a core component of MedRAG. Every major change should be measurable.

This document defines the evaluation methodology for retrieval, generation, and system performance.

---

# 2. Evaluation Philosophy

Every engineering change should answer:

* Did retrieval improve?
* Did answer quality improve?
* Did latency change?
* Did hallucination increase?
* Was the trade-off worthwhile?

---

# 3. Retrieval Evaluation

Metrics:

* Recall@K
* Precision@K
* MRR
* nDCG
* Hit Rate

Benchmarks will compare:

* BM25
* Dense Retrieval
* Hybrid Retrieval

---

# 4. Generation Evaluation

Primary metrics:

* Faithfulness
* Answer Relevancy
* Context Precision
* Context Recall

Framework:

* RAGAS

---

# 5. Hallucination Evaluation

Measure:

* Unsupported claims
* Fabricated citations
* Context deviation

Frameworks:

* RAGAS
* DeepEval (future)

---

# 6. Performance Evaluation

Track:

* Retrieval latency
* Generation latency
* End-to-end latency
* Throughput
* Memory usage

---

# 7. Benchmark Datasets

Primary:

* PubMedQA
* BioASQ

Secondary:

* MedMCQA
* Custom evaluation dataset

---

# 8. Human Evaluation

Review criteria:

* Medical correctness
* Citation quality
* Completeness
* Readability
* Helpfulness

---

# 9. Regression Testing

No retrieval or generation changes should be merged without confirming they do not significantly degrade existing performance.

---

# 10. Experiment Tracking

Track:

* Embedding model
* LLM
* Prompt version
* Reranker
* Retrieval configuration
* Metrics
* Git commit

Using:

* MLflow

---

# 11. Evaluation Frequency

Evaluate:

* After every major sprint
* After retrieval changes
* After prompt updates
* Before releases

---

# 12. Success Criteria

Examples:

* Faithfulness ≥ 0.90
* Context Recall ≥ 0.85
* Retrieval latency ≤ 500 ms (median)
* Test coverage ≥ 85%

Targets will evolve as the system matures.

---

# 13. Continuous Improvement

Evaluation is an iterative process.

Benchmark results should guide engineering decisions rather than intuition alone.

---

# 14. Summary

Evaluation is treated as a first-class engineering discipline. Improvements should be measurable, reproducible, and documented.
