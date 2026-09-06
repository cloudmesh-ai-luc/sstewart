Samaira Stewart



## Project Proposal – 911 Text Message Analysis and Cloud-Based Emergency Triage System

|                          |                                                               |
|--------------------------|-----------------------------------------------------------------------|
| **Course:**              | Cloud Computing, DevOps, and AI | 
| **Team Members**         | -*Sam*
| **Contact**              | stewartsamaira4@gmail.com 
| **Instructor**           | Gregor von Laszewski |
| **Date**                 | *Sept. 6 2026* |

---

### 1. Project Overview

This project proposes the development of a cloud-based application that simulates a text-to-911 emergency communication service. It will allow users to submit emergency text messages through a web-based interface. The messages will then be securely transmitted to a backend service and stored in a cloud-hosted database where authorized admin can retrieve, review, and manage incoming emergency messages.

In addition to storing and displaying messages, the system will analyze the content of each message and assign a suggested priority level based on keywords and phrases often associated with emergency situations. For example, messages containing terms such as "shooting," "fire," "unconscious," "not breathing," or "trapped" may receive a higher preliminary priority than messages describing less immediately life-threatening situations.

The purpose of the system is to demonstrate how cloud computing, databases, APIs, and automated text analysis can be combined to support emergency communication and response workflows.

**Disclaimer:**

This application is strictly for educational purposes. It will not connect to actual 911 infrastructure or dispatch emergency services. Priority classifications will assist admins but will not replace human judgement.


### 2. Problem Statement (150‑250 words)  

**Problem:**  Modern AI‑enabled applications often need to switch between different large language models (LLMs)
– e.g., a fast, low‑cost model for routine queries and a larger, more creative model for brainstorming.
Currently our lab uses a single LLM deployed on a VM; swapping models requires manual re‑configuration and downtime.  

**Proposed solution:**  Deploy **three containerised LLM back‑ends** (e.g., OpenAI GPT‑3.5‑Turbo,
Llama‑2‑7B, and a locally‑hosted Mistral‑7B) on **AWS ECS Fargate** (or Azure Container Instances).
Build a **REST‑ful “LLM‑Chooser” service** that receives a request, inspects a lightweight meta‑parameter (`mode=fast|creative|balanced`),
and forwards the prompt to the appropriate model.  The service will be **exposed via OpenWebUI** for a web UI, while a
**VS Code CLI extension** (`llm-select`) lets developers invoke the chooser directly from the
terminal (`llm-select --mode creative "Write a poem"`).  A small **Python SDK** (`llm_client.py`) provides
programmatic access for downstream scripts.  

**Benefits:**  

- Zero‑downtime model switching – users simply change the `mode` flag.  
- Cost‑aware routing – the fast mode uses the cheapest model, saving ~ 40 % on API spend.  
- Dev‑friendly interface – VS Code CLI + Python SDK streamline experimentation.  
- Hands‑on experience with IaC (Terraform), CI/CD (GitHub Actions), container orchestration, and model serving.  

---

### 3. Objectives & Success Criteria  

| # | Objective | Success Metric |
|---|-----------|----------------|
| 1 | Deploy three LLM containers on a managed serverless container platform. | All three containers reachable via internal DNS; health‑check ≤ 2 % failure rate. |
| 2 | Implement the LLM‑Chooser micro‑service with a deterministic routing rule. | 100 % of test requests routed to the correct model according to `mode`. |
| 3 | Provide VS Code CLI (`llm-select`) and Python SDK (`llm_client.py`). | CLI and SDK pass unit tests; documentation covers 5 common use‑cases. |
| 4 | Set up CI/CD pipeline that automatically builds Docker images, runs tests, and deploys to staging on every push. | 2‑minute pipeline run, 0 failed builds for 3 consecutive commits. |
| 5 | Demonstrate cost reduction compared with the single‑model baseline. | Average API cost per 1 k tokens ≤ $0.025 (≈ 40 % lower). |

---

### 4. Scope  

| In‑Scope | Out‑Of‑Scope |
|----------|--------------|
| • Containerising three LLMs (OpenAI API, Llama‑2, Mistral) | Training new models |
| • LLM‑Chooser service (REST API) | • Enterprise‑grade SLA / 99.9 % uptime guarantee |
| • VS Code CLI extension & Python SDK | • Full multi‑region deployment |
| • IaC (Terraform), CI/CD (GitHub Actions) | • Data‑privacy compliance beyond class‑level demonstration |
| • Documentation, demo video | • Production‑scale monitoring dashboards (only basic CloudWatch metrics) |

* Which LLMs to chose will be determined based on the resource capabilities.
  
---

### 5. Technical Approach  

#### 5.1 Cloud Architecture  

| Component | Service (AWS example) | Notes |
|-----------|-----------------------|-------|
| **Container Host** | ECS Fargate (or Azure Container Instances) | Serverless, pay‑per‑use, no VM management |
| **LLM Back‑ends** | - GPT‑3.5‑Turbo (via OpenAI API) <br> - Llama‑2‑7B (Docker image from HuggingFace) <br> - Mistral‑7B (Docker image) | Each exposed on internal port 8000‑8002 |
| **LLM‑Chooser** | ECS Service → API Gateway (public) | Stateless Flask/FastAPI app |
| **OpenWebUI** | Separate ECS Service behind same API GW | Connects to chooser via `/choose` endpoint |
| **CI/CD** | GitHub Actions → Terraform → ECS Deploy | Automated on merge to `main` |
| **Observability** | CloudWatch Logs & Metrics | Basic latency & error rate alerts |

*Diagram placeholder:*  
Insert a simple block diagram (Client → API GW → LLM‑Chooser → {GPT, Llama‑2, Mistral}). You can draw it in draw.io and embed as PNG.

#### 5.2 DevOps Pipeline  

| Stage | Tool | What it does |
|-------|------|--------------|
| **Source** | GitHub | Branch‑policy: `main` protected, PR must pass checks |
| **Build** | Docker Build (GitHub Actions) | Build three images (llm‑chooser, openwebui, python‑sdk) |
| **Test** | PyTest, Bandit, Flake8 | Unit tests for routing logic, security scan |
| **Deploy** | Terraform + ECS Deploy Action | Update task definitions, roll out to **staging** first, then **prod** |
| **Post‑Deploy** | Smoke test script | Calls `/healthz` on each service, reports success/failure |

#### 5.3 AI / Model Serving  

```python
# Sample code – see the execution block below for a runnable demo
def route_prompt(prompt: str, mode: str) -> str:
    """
    Very simple routing rule:
    - 'fast'      → OpenAI GPT‑3.5‑Turbo (cheapest, lowest latency)
    - 'creative'  → Llama‑2‑7B (more parameters)
    - 'balanced'  → Mistral‑7B (mid‑ground)
    """
    # mapping of mode → endpoint URL (in reality you would load from env vars)
    endpoints = {
        "fast": "http://llm-gpt:8000/completions",
        "creative": "http://llm-llama:8001/completions",
        "balanced": "http://llm-mistral:8002/completions",
    }
    url = endpoints.get(mode, endpoints["balanced"])
    # Here we would `requests.post(url, json={"prompt": prompt})`
    # For demo we just return the chosen URL.
    return f"Routing to {url}"
```

The **Python SDK** (`llm_client.py`) will expose a single function `ask(prompt, mode="balanced")` that 
internally calls the chooser service, handles retries, and returns the model response.

#### 5.4 VS Code CLI Extension  

*Command*: `llm-select --mode <fast|creative|balanced> "<prompt>"`  

The extension will invoke the Python SDK under the hood and print the model’s answer directly in the terminal.

#### 5.5 Security  

- **IAM**: least‑privilege role for ECS task execution.  
- **Secrets**: OpenAI API key stored in AWS Secrets Manager; injected as env‑var at runtime.  
- **Network**: LLM containers run in a private subnet; only the chooser has a public endpoint.  
- **TLS**: API Gateway enforces HTTPS.

---

### 6. Project Plan & Timeline  

| Phase | Tasks | Start | End |
|-------|-------|-------|-----|
| **Kick‑off** | Requirements finalisation, repo creation | 2026‑10‑01 | 2026‑10‑04 |
| **Design** | Architecture diagram, Terraform module layout, CLI spec | 2026‑10‑05 | 2026‑10‑12 |
| **Implementation** | • Build Docker images <br> • Write chooser service (FastAPI) <br> • Write VS Code CLI (Node.js) <br> • Write Python SDK | 2026‑10‑13 | 2026‑11‑07 |
| **CI/CD** | GitHub Actions workflow, Terraform apply to staging | 2026‑11‑08 | 2026‑11‑14 |
| **Testing** | Unit tests, integration tests (routing), load test (locust) | 2026‑11‑15 | 2026‑11‑28 |
| **Demo & Documentation** | OpenWebUI UI, CLI demo video, README, hand‑off guide | 2026‑11‑29 | 2026‑12‑05 |
| **Evaluation** | Cost analysis, performance report, final presentation | 2026‑12‑06 | 2026‑12‑12 |

---

### 7. Resources & Budget  

To keep the budegt real small and do most of the development on the local computer,  we develop a mock llm service, that does not actually uses an llm but returns information in th esame format an LLM would return.  Before any cloud services are used, the implementation is done locally with the mock service, then it is replicated on the cloud. In the fnal step we will use real llm services, but will more carefully evaluate which are realistic. We propose t chose the smallest andcheapest possible models. The possibly not even need tou use GPUs.
A configuration file in yaml will be used to describe the nature of the service and the resource need and where they are hosted. The chosen DevOps framework will then provision and stage the services.

As part of this we plan also to investigate if hosting on kubernetes or EC2 like VMs is more easy to do and costeffective. We will only implement one solution however.

| Resource | Qty | Cost (USD) | Reason |
|----------|-----|------------|--------|
| AWS Fargate (vCPU 0.5, 1 GB RAM) – 3 services – 30 days | – | $80 | Container execution |
| OpenAI GPT‑3.5‑Turbo usage (estimated 100 k tokens) | – | $20 | Model A cost |
| S3 storage (logs, 50 GB) | – | $5 | Persistence |
| GitHub Team plan (5 users) | – | $60 | Private repo & Actions minutes |
| Misc. – domain, SSL cert | – | $15 | Secure endpoint |
| **Total** | | **≈ $180** |  |

*(If your institution provides free credits, update accordingly.)*

---

### 8. Risk Management  

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Cloud cost runaway (e.g., unlimited GPT calls) | Medium | High | Set usage alerts in CloudWatch; enforce per‑user token quota in chooser. |
| Model container crash → service downtime | Low | Medium | Deploy each model in its own task with restart policy; health checks. |
| CLI incompatibility across OSes | Low | Low | Use Node.js + cross‑platform packaging (pkg) + automated CI build for Windows/macOS/Linux. |
| Secrets leakage | Low | High | Store keys only in Secrets Manager; no plain‑text in repo. |
| Insufficient test coverage → routing bugs | Low | Medium | Enforce 90 % coverage rule in CI; add mutation tests. |

---

### 9. Evaluation & Success Metrics  

| Metric | Target | Tool |
|--------|--------|------|
| Average routing latency (prompt → response) | ≤ 1.2 s (fast mode) | CloudWatch Custom Metric |
| End‑to‑end cost per 1 k tokens | ≤ $0.025 (vs. baseline $0.041) | OpenAI usage dashboard + custom script |
| CLI success rate (no error) | 100 % over 100 automated calls | GitHub Actions test matrix |
| Documentation completeness | 100 % of required sections with examples | Peer‑review checklist |
| Student satisfaction (survey) | ≥ 4/5 average | Post‑demo questionnaire |

---

### 10. Deliverables  

| Deliverable | Format | Due |
|-------------|--------|-----|
| Architecture diagram | PNG / PDF | End of Design |
| Terraform IaC code | .tf files (Git repo) | End of Implementation |
| LLM‑Chooser micro‑service | Docker image (ECR) + source | End of Implementation |
| VS Code CLI extension | VSIX package + README | End of Implementation |
| Python SDK (`llm_client.py`) | .py file + docs | End of Implementation |
| OpenWebUI demo instance | URL (staging) | End of Demo |
| Test suite (PyTest, locust) | repo + CI badge | End of Testing |
| Final report & presentation | PDF + Slides | End of Evaluation |

---

### 11. References  

- AWS Well‑Architected Framework – <https://aws.amazon.com/architecture/well-architected/>  
- OpenAI API Documentation – <https://platform.openai.com/docs/api-reference>  
- “Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation” – Jez Humble & David Farley (2010)  
- HuggingFace Docker images for Llama‑2 & Mistral – <https://huggingface.co/models>  

---  


## Technologies Used

Suggestions:

* FastAPI
* MariaDB
* LLM to create darfted responses and classification


## References



