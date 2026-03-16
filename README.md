# StarCoder-12B Domain Adaptation Pipeline

A high-performance MLOps pipeline for extracting, filtering, and synthesizing high-quality instructional data for the C programming language to fine-tune StarCoder-12B.

---

## 🚀 Project Overview
This project addresses the challenge of domain-specific LLM adaptation by building a robust "Data Factory." We leverage static analysis and asynchronous generation to transform raw, noisy code from **The Stack V2** into high-fidelity, instruction-tuned datasets.



## 🛠 Technical Architecture
The pipeline is structured into three distinct stages:

1. **Structural Mining (Tree-Sitter):** We utilize AST (Abstract Syntax Tree) parsing via Tree-Sitter to identify functional boundaries, complexity, and structural integrity in C source code.
2. **Quality Gatekeeping (Clang):** Integration of the **Clang Static Analyzer** performs automated type-checking and compilation verification, ensuring the training corpus only contains "correct" code.
3. **Synthetic Instruction Generation (vLLM + AsyncIO):** An asynchronous worker pool orchestrates `vLLM` inference to execute custom instruction patterns:
    * **I -> R:** Instruction to Response.
    * **S -> C:** Code Snippet to Concepts.
    * **C -> I:** Concepts to Instruction generation.

## ⚙️ Key Technologies
* **LLM Inference:** `vLLM` with PagedAttention for high-throughput generation.
* **Static Analysis:** `Tree-Sitter` (AST parsing) and `Clang` (Semantic validation).
* **Distributed Training:** `DeepSpeed ZeRO-3` for memory-efficient parameter sharding.
* **Data Pipeline:** `AsyncIO` for concurrency, `boto3` for streaming public datasets.
* **Versioning:** `Hugging Face Hub` for dataset management.

## 🏗 Pipeline Workflow
```mermaid
graph TD
    A[Raw Source Code] --> B{Tree-Sitter Parser}
    B --> C[AST Filter]
    C --> D{Clang Analyzer}
    D --> E[Validated Snippets]
    E --> F[Async vLLM Generator]
    F --> G[Few-Shot Verification Loop]
    G --> H[Fine-Tuned StarCoder-12B]
