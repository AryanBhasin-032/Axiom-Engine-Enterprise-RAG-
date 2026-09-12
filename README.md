# Axiom Engine

An advanced, decoupled three-tier Retrieval-Augmented Generation (RAG) system designed to deliver trustworthy, verifiable question-answering for high-stakes environments.

## 📌 Overview

Large Language Models (LLMs) are powerful tools for knowledge management, but standalone models suffer from hallucinations, lack of proprietary data access, and untraceable claims. Furthermore, early RAG implementations relying purely on dense vector search frequently fail to retrieve exact alphanumeric identifiers, acronyms, or rigid section numbers.

**Axiom Engine** solves this by discarding black-box AI wrappers in favor of a highly observable, custom **Hybrid Search pipeline**. By enforcing strict generation thresholds, the engine guarantees that the LLM either answers exclusively using retrieved context or triggers a strict "I don't know" fallback.

## 🏗 System Architecture

<img width="626" height="1046" alt="axiom arch" src="https://github.com/user-attachments/assets/8a315760-a1e5-48df-84b2-0d77c5d23755" />


To handle heavy machine learning inference efficiently, the system is decoupled into a strict three-tier architecture:

### 1. Frontend (Presentation Layer)
* **Tech:** Next.js Single Page Application (SPA)
* **Role:** Captures user queries and renders a dynamic split-screen citation interface. This allows users to manually cross-reference and verify the AI's claims directly against the source documents.

### 2. Backend (Application Logic)
* **Tech:** Python / FastAPI
* **Role:** Orchestrates the entire AI pipeline. 
* **Pipeline Steps:** 
  1. Chunks PDF documents.
  2. Generates embeddings using HuggingFace models.
  3. Executes hybrid search.
  4. Merges retrieval scores using Reciprocal Rank Fusion (RRF).
  5. Injects verified context into the LLM prompt.

### 3. Database (Storage Layer)
* **Tech:** PostgreSQL with `pgvector`
* **Role:** Houses relational metadata alongside high-dimensional vector embeddings and GIN indexes for lexical search.

## ⚙️ Core Methodology: Hybrid Search

Axiom Engine bridges the gap between exact keyword retrieval and semantic understanding by combining two retrieval methods:
* **Dense Vector Embeddings:** Captures the semantic meaning and context of the query.
* **Sparse BM25 Retrieval:** Ensures exact keyword matching for specific terminology, acronyms, and alphanumeric identifiers.

Evaluated using the programmatic **RAGAS** framework, Axiom Engine targets production-ready reliability metrics:
* **Faithfulness Score:** `> 0.95` (Effectively eliminating hallucinations)
* **Context Precision Score:** `> 0.85`
