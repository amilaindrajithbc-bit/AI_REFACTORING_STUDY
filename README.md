# AI Refactoring Trustworthiness Study

## Evaluating the Trustworthiness of AI-Generated Software Refactoring: A Comparative Experimental Study Using Large Language Models

---

## Abstract

Large Language Models (LLMs) are increasingly being used to automate software engineering tasks such as code generation and refactoring. Although these models can substantially improve developer productivity, the quality and trustworthiness of AI-generated refactorings remain insufficiently understood.

This research presents a comparative experimental study of three state-of-the-art LLMs—ChatGPT, Gemini, and Claude—to evaluate their effectiveness in refactoring Python source code while preserving the original functionality. The generated refactorings are assessed using established software quality metrics, including Lines of Code (LOC), Cyclomatic Complexity (CC), and Maintainability Index (MI). The objective is to identify which model produces the most maintainable and trustworthy refactored code.

---

## Research Objectives

- Evaluate the trustworthiness of AI-generated software refactoring.
- Compare the refactoring capabilities of ChatGPT, Gemini, and Claude.
- Measure software quality improvements using static analysis.
- Investigate how different LLMs influence software maintainability.
- Develop a reproducible evaluation framework for AI-assisted software refactoring.

---

## Research Methodology

Each experiment follows the same workflow:

1. Select an original Python function from an open-source repository.
2. Apply an identical refactoring prompt to all three LLMs.
3. Accept the first functionally equivalent refactoring.
4. Measure software quality using Radon.
5. Compare the results using quantitative metrics.
6. Analyse and discuss the findings.

---

## Software Quality Metrics

The following metrics are used throughout the study.

| Metric | Description |
|---------|-------------|
| LOC | Lines of Code |
| CC | Cyclomatic Complexity |
| MI | Maintainability Index |

---

## Large Language Models Evaluated

- ChatGPT
- Gemini
- Claude

---

## Tools and Technologies

- Python
- Radon
- Git
- GitHub
- Visual Studio Code
- Jupyter Notebook

---

## Repository Structure

```text
AI_REFACTORING_STUDY/
│
├── graphs/
├── metrics/
├── original_functions/
├── refactored_code/
│   ├── chatgpt/
│   ├── gemini/
│   └── claude/
├── results/
├── scripts/
│
├── AI_Refactoring_Study.ipynb
├── README.md
├── LICENSE
├── requirements.txt
└── .gitignore
```

---

## Repository Contents

- Original Python functions extracted from open-source repositories.
- AI-generated refactored implementations.
- Software quality metrics collected using Radon.
- Comparative experimental results.
- Analysis scripts used to generate metrics and visualisations.
- Figures and tables used in the dissertation.

---

## Reproducibility

To reproduce the experiments:

1. Clone this repository.
2. Install the required Python packages.
3. Execute the analysis scripts.
4. Compare the generated metrics with the reported results.

---

## Repository Status

This repository is actively maintained as part of an MSc dissertation.

Additional repositories, experiments, analyses, and visualisations will be added throughout the research.

---

## License

This repository is distributed under the MIT License.

---

## Citation

If you use this repository for academic or research purposes, please cite the associated MSc dissertation.

---

## Author

**Amila Piyasiri**

MSc Dissertation Research

Department of Computer Science