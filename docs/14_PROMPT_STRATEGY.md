# Prompt Strategy

**Project:** MedRAG
**Version:** 1.0
**Sprint:** 0 – Phase 6
**Status:** Draft

---

# 1. Purpose

This document defines the prompt engineering strategy for MedRAG.

Prompt engineering is treated as a first-class software engineering discipline. Prompts are versioned, evaluated, documented, and improved through measurable experimentation rather than ad hoc changes.

Objectives:

* Ensure evidence-grounded generation
* Reduce hallucinations
* Improve answer consistency
* Enable reproducible prompt experiments
* Support safe prompt evolution

---

# 2. Guiding Principles

Every prompt should:

* Ground responses in retrieved evidence.
* Prioritize factual correctness over completeness.
* Explicitly acknowledge uncertainty.
* Avoid unsupported medical claims.
* Produce transparent citations.
* Be deterministic where practical.
* Be modular and reusable.

---

# 3. Prompt Architecture

Each generation request is composed of multiple sections.

```text
System Prompt
        │
User Question
        │
Retrieved Context
        │
Citation Instructions
        │
Output Format Instructions
```

Prompt assembly is handled by dedicated builder components rather than manually concatenated strings.

---

# 4. Prompt Types

## 4.1 System Prompt

Defines the model's role and behavioral constraints.

Responsibilities:

* Identity
* Scope
* Safety
* Evidence requirements
* Citation policy
* Style guidelines

---

## 4.2 User Prompt

Represents the user's natural language question.

No preprocessing beyond validation and normalization should alter the user's intent.

---

## 4.3 Context Prompt

Contains retrieved chunks selected by the retrieval pipeline.

Rules:

* Preserve original wording.
* Maintain chunk ordering.
* Include metadata references.
* Avoid duplicate chunks.

---

## 4.4 Citation Prompt

Defines how references should be presented.

Requirements:

* Every factual statement should be traceable to retrieved evidence where applicable.
* Citations should correspond only to retrieved documents.
* Never fabricate references.

---

## 4.5 Output Prompt

Specifies the required response structure.

Example sections:

* Direct Answer
* Supporting Evidence
* Key Takeaways
* References
* Limitations (when applicable)

---

# 5. Prompt Templates

Prompt templates should be stored externally rather than hardcoded in application logic.

Recommended directory:

```text
prompts/
├── system/
├── generation/
├── retrieval/
├── evaluation/
└── templates/
```

Each template should include metadata such as version, author, creation date, and intended use.

---

# 6. Prompt Versioning

Every prompt template must include:

| Field        | Description        |
| ------------ | ------------------ |
| Prompt ID    | Unique identifier  |
| Version      | Semantic version   |
| Author       | Creator            |
| Created At   | Timestamp          |
| Last Updated | Timestamp          |
| Description  | Purpose            |
| Changelog    | Summary of changes |

Prompt versions should be referenced in experiment logs and evaluation records.

---

# 7. Context Packing Strategy

The prompt builder is responsible for assembling context efficiently.

Goals:

* Maximize relevant evidence.
* Minimize redundancy.
* Respect model context limits.
* Preserve document ordering where beneficial.

Strategies may include:

* Top-K retrieval
* Section-aware ordering
* Deduplication
* Token budgeting
* Metadata inclusion

---

# 8. Token Budgeting

The prompt builder should allocate context based on a configurable token budget.

Suggested allocation:

| Component           | Approximate Share |
| ------------------- | ----------------- |
| System Prompt       | 10%               |
| User Query          | 5%                |
| Retrieved Context   | 75%               |
| Output Instructions | 10%               |

Actual allocation should adapt to model context windows.

---

# 9. Hallucination Mitigation

Prompt instructions should encourage the model to:

* Base answers only on supplied evidence.
* State when evidence is insufficient.
* Avoid speculation.
* Avoid introducing unsupported facts.
* Preserve distinctions between evidence and inference.

The model should prefer "I cannot determine this from the retrieved evidence" over guessing.

---

# 10. Citation Policy

Every generated answer should:

* Reference retrieved documents only.
* Preserve document identifiers where possible.
* Avoid fabricated citations.
* Associate references with the relevant statements.

Citation formatting should remain consistent across the application.

---

# 11. Response Structure

Default responses should follow a structured format.

Recommended sections:

1. Direct Answer
2. Supporting Evidence
3. References
4. Notes or Limitations (if applicable)

This structure may evolve based on user feedback and evaluation results.

---

# 12. Prompt Evaluation

Prompt changes should be evaluated using:

* Faithfulness
* Answer Relevancy
* Context Precision
* Context Recall
* Human review
* Hallucination rate
* Latency impact

Prompt modifications should not be merged without measurable evaluation where feasible.

---

# 13. Experimentation Strategy

Prompt experiments should vary one factor at a time.

Examples:

* Citation wording
* Context ordering
* Instruction phrasing
* Output formatting
* Token allocation

This enables attribution of observed performance changes.

---

# 14. Prompt Testing

Prompt templates should undergo:

* Syntax validation
* Variable substitution validation
* Snapshot testing
* Regression testing
* Evaluation benchmarking

Broken templates should fail automated checks.

---

# 15. Prompt Registry

A centralized registry should maintain active prompt templates.

Each prompt should have:

* Active status
* Deprecation status
* Successor version (if applicable)

Deprecated prompts remain available for experiment reproducibility.

---

# 16. Safety Considerations

Prompt instructions should reinforce that the system:

* Does not provide medical diagnosis.
* Does not replace professional medical advice.
* Should acknowledge uncertainty.
* Must not fabricate evidence.
* Must remain within the scope of retrieved biomedical literature.

---

# 17. Future Enhancements

Potential future capabilities include:

* Adaptive prompts based on query type
* Dynamic context selection
* Multi-step prompting
* Tool-assisted reasoning
* Multi-agent prompt orchestration
* User-configurable response styles

These features should integrate without breaking existing prompt interfaces.

---

# 18. Summary

Prompt engineering in MedRAG is treated as a disciplined engineering practice. Templates are versioned, evaluated, and maintained with the same rigor as application code, ensuring that improvements in answer quality are measurable, reproducible, and reversible.
