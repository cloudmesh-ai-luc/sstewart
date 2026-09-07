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

**Problem:**  
Traditional emergency communication systems primarily rely on voice calls. However, there are situations in which a person may not be able to communicate with emergency services through a traditional voice call (ex. deaf, non-verbal, etc.). 

**Proposed solution:**  
A simulated text-to-911 system provides an opportunity to explore how emergency communications can be collected, stored, analyzed, and presented to emergency personnel. This particularly serves well during times of high volume emergency messages. An emergency call center may receive many messages at the same time, making it difficult for personnel to manually evaluate every message in the same amount of time.

**Benefits:**  

1. Allows users to submit simulated emergency text messages.
2. Stores messages in a centralized cloud database.
3. Automatically analyzes message content.
4. Assigns a preliminary priority level.
5. Presents messages to administrators in priority order.
6. Allows administrators to review and modify the assigned priority.
7. Provides analytics about incoming emergency messages.

---

### 3. Objectives & Success Criteria  

| # | Objective | Success Metric |
|---|-----------|----------------|
| 1 | Create a user-facing interface where users can submit emergency text messages | Users are able to submit messages to the backend 
| 2 | Cloud Based Message Storage | 100 % of test requests routed to the correct database for authorized admin to engage with
| 3 | Automated Message Analysis | Develop a text-analysis service that examines incoming messages using predefined word and assign a preliminary priority score. Potential for implementation of an NLP model to analyze the meaning of the overall message rather than screening for keywords |
| 4 | Priority Classification | Messages will receive a preliminary priority classifaction (Critical, High, Moderate, Low) |
| 5 | Admin Dashboard | Create an admin dashboard that allows authorized users to monitor incoming messages |
| 6 | Analytics | The application will provide basic analytics about emergency messages |
| 7 | Set up CI/CD pipeline that automatically builds Docker images, runs tests, and deploys to staging on every push. | 2‑minute pipeline run, 0 failed builds for 3 consecutive commits. |

---

### 4. MVP Scope  

To keep the project achievable, the Minimum Viable Product will include:

**User**
- Submit simulated emergency text
- Receive submission confirmation
**Backend**
- REST API
- Message validation
- Database persistence
- Keyword analysis
- Priority scoring
- LLM Integration
**Administrator**
- Login
- View incoming messages
- Sort by priority
- Filter messages
- View message details
- Change status
- Override priority
**Analytics**
- Total messages
- Messages by priority
- Messages by category
- Average processing time

* Which LLMs to chose will be determined based on the resource capabilities.
  
---

### 5. Technical Approach  

#### 5.1 Cloud Architecture  

The project will demonstrate several cloud computing concepts.

Cloud Database

A managed PostgreSQL database will store emergency messages and application data.

Cloud Application Hosting

The backend API and frontend application will be deployed to cloud infrastructure.

Scalability

The system could be designed so that additional backend instances can be created when message volume increases.

Availability

The application can be designed with redundant services and managed cloud infrastructure to minimize downtime.

Security

Communication between clients and the backend will use HTTPS.

Administrative functionality will require authentication and authorization.

Monitoring

Cloud monitoring tools can track:

- API response time
- Application errors
- Database usage
- Number of incoming messages
- System availability 

**High Level Architecture Diagram**

<img width="1312" height="1199" alt="image" src="https://github.com/user-attachments/assets/a6a2c794-7f38-4718-9761-03daefd27a6d" />


#### 5.2 DevOps Pipeline  

                    DEVELOPER
                        │
                        ▼
                ┌───────────────┐
                │    GitHub     │
                │  Repository   │
                └───────┬───────┘
                        │
                    git push
                        │
                        ▼
              ┌─────────────────────┐
              │   CI PIPELINE       │
              │                     │
              │ • Lint              │
              │ • Unit Tests        │
              │ • Integration Tests │
              │ • Security Scan     │
              └──────────┬──────────┘
                         │
                    Tests Pass?
                    /          \
                  NO            YES
                  │              │
                  ▼              ▼
               STOP       Build Docker Image
                                │
                                ▼
                       ┌──────────────────┐
                       │ Artifact Registry│
                       │                  │
                       │ Docker Image     │
                       └────────┬─────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │  CD PIPELINE     │
                       │                  │
                       │ Deploy Staging   │
                       └────────┬─────────┘
                                │
                                ▼
                       Integration Tests
                                │
                         Tests Pass?
                         /         \
                       NO           YES
                       │             │
                       ▼             ▼
                    ROLLBACK     Deploy PROD
                                     │
                                     ▼
                            ┌────────────────┐
                            │  Cloud Run     │
                            │                │
                            │ FastAPI        │
                            └───────┬────────┘
                                    │
                   ┌────────────────┼────────────────┐
                   │                │                │
                   ▼                ▼                ▼
             Cloud SQL         Vertex AI       Secret Manager
             PostgreSQL        Gemini LLM        Secrets
                   │
                   ▼
             Cloud Logging
             & Monitoring

### 5.3 Architecture Component Description

1. Not yet sure if this is needed, we can simulate with a mock service, which actually may be better: **F/OSS SMS Gateway:** Replaces paid commercial APIs. This could be a self-hosted Kannel server connected to a cellular modem (SMPP) or an open-source Android application that forwards received SMS messages via HTTP POST to the API layer.
2. **FastAPI Application:** The central integration point. It handles HTTP requests from the gateway, invokes the Triage Engine, manages database transactions, and pushes real-time updates to the dashboard via WebSockets.
3. **Triage Engine:** A distinct Python module that performs keyword analysis on message bodies to calculate priority scores (see Section 3).
4. **PostgresSQL:** The source of truth. It stores session state, full message logs, and dispatcher activity logs with full ACID compliance.
5. **Admin Dispatch Dashboard:** A React-based single-page application that provides dispatchers with a live view of incoming emergencies, sorted by priority.

---

## PostgresSQL Database Schema

The database uses sample (incomplete) tables configured for transactional integrity, automatic timestamp updates, and performance indexing to instantly surface high-priority emergencies.

```sql
-- Active Emergency Sessions / Threads
CREATE TABLE emergency_sessions (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    phone_number VARCHAR(20) NOT NULL,
    current_status VARCHAR(50) DEFAULT 'QUEUED', -- QUEUED, DISPATCHED, RESOLVED
    assigned_dispatcher_id INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Individual Text Messages
CREATE TABLE messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT,
    sender_type ENUM('CITIZEN', 'DISPATCHER', 'SYSTEM') NOT NULL,
    body TEXT NOT NULL,
    priority_score FLOAT DEFAULT 0.0,
    priority_tier TINYINT CHECK (priority_tier BETWEEN 1 AND 3),
    classification_label VARCHAR(20),
    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES emergency_sessions(session_id) ON DELETE CASCADE
);

-- Indexing for real-time dashboard sorting performance
CREATE INDEX idx_messages_priority ON messages (priority_tier ASC, received_at DESC);
CREATE INDEX idx_sessions_status ON emergency_sessions (current_status);

```

---

## Python Priority Ranking & Triage Engine

The triage engine analyzes incoming text content to assign a priority tier 
(`1` for Critical, `2` for Urgent, `3` for Routine), protecting against false positives by accounting for simple negations.

```python
import re
from typing import Tuple

# Weighted keyword dictionary mapping emergency terms to severity scores
KEYWORD_WEIGHTS = {
    # Critical Life Safety (Priority 1)
    "gun": 50, "shot": 50, "shooting": 50, "stab": 50, "bleeding": 45,
    "unconscious": 45, "not breathing": 50, "cpr": 50, "fire": 45,
    "choking": 45, "suicide": 50, "overdose": 45, "knife": 45,
    
    # Urgent Safety / Property (Priority 2)
    "robbery": 30, "break-in": 30, "intruder": 35, "car accident": 30,
    "crash": 30, "fight": 25, "harassment": 20,
    
    # Non-Urgent / Routine (Priority 3)
    "noise": 5, "theft": 10, "lost": 5, "property": 5
}

NEGATION_TERMS = {"no", "not", "isn't", "wasn't", "never", "no longer"}

def calculate_priority(text: str) -> Tuple[int, str, float]:
    """
    Scans text message for weighted keywords, checks for immediate negation context,
    and returns a priority tier, label, and cumulative score.
    """
    cleaned_text = text.lower()
    words = re.findall(r'\b\w+\b', cleaned_text)
    
    score = 0.0
    matched_triggers = []

    for i, word in enumerate(words):
        if word in KEYWORD_WEIGHTS:
            # Check context window for negation (e.g., "no weapon")
            context_window = words[max(0, i-2):i]
            is_negated = any(neg in context_window for neg in NEGATION_TERMS)
            
            if is_negated:
                score += (KEYWORD_WEIGHTS[word] * 0.1)
                matched_triggers.append(f"{word} (negated)")
            else:
                score += KEYWORD_WEIGHTS[word]
                matched_triggers.append(word)

    # Map cumulative score to Priority Tiers
    if score >= 40:
        priority_tier = 1
        label = "CRITICAL"
    elif score >= 20:
        priority_tier = 2
        label = "URGENT"
    else:
        priority_tier = 3
        label = "ROUTINE"

    return priority_tier, label, score

```

---

#### 5.4 Security  

- **IAM**: least‑privilege role for ECS task execution.  
- **Secrets**: OpenAI API key stored in GCP Secrets Manager; injected as env‑var at runtime.  
- **Network**: LLM containers run in a private subnet; only the chooser has a public endpoint.  
- **TLS**: API Gateway enforces HTTPS.

---

### 6. Development Milestones

The project will have several major milestones throughout development.

Milestone 1 — Project Foundation

End of Week 2

The project architecture and database design will be complete. The development environment, source-control repository, database schema, and initial application structure will be established.

Milestone 2 — Working Message System

End of Week 4

A user will be able to submit a simulated 911 text message through the React application, send it to the Spring Boot API, and have it persisted in PostgreSQL.

The complete workflow will be:

User
  ↓
React Application
  ↓
REST API
  ↓
PostgreSQL

Milestone 3 — Automated Prioritization

End of Week 5

The system will automatically analyze incoming messages, identify keywords, calculate a priority score, and assign a preliminary priority level.

Example:

Message:
"I'm trapped in my house. There is a fire."

Analysis:
fire       +8
trapped    +8

Priority Score: 16
Priority: HIGH

Milestone 4 — Functional Call Center Dashboard

End of Week 7

An authenticated administrator will be able to:

Log in

View incoming messages

Sort messages by priority

Filter messages by category/status

View message details

Change message status

Override automated priority

View priority history

At this point, the core MVP will be considered functionally complete.

Milestone 5 — Cloud Deployment

End of Week 8

The application will be deployed to a cloud environment. The frontend, backend API, and MariaDB database will operate as cloud-hosted components.

The deployment architecture will resemble:

```                     ┌─────────────────────┐
                    │     React/Vite      │
                    │    Web Interface    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       FastAPI       │
                    │      REST API       │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
      ┌────────────┐    ┌──────────────┐   ┌──────────────┐
      │  MariaDB   │    │    Keyword   │   │   Ollama     │
      │  Database  │    │    Engine    │   │ Local LLM    │
      └────────────┘    └──────┬───────┘   └──────┬───────┘
                                │                  │
                                └────────┬─────────┘
                                         ▼
                                ┌─────────────────┐
                                │ Priority Engine │
                                └────────┬────────┘
                                         │
                                         ▼
                                ┌─────────────────┐
                                │  Admin Dashboard │
                                │ Human Review     │
                                └─────────────────┘
```
Milestone 6 — Final Testing

End of Week 9

Testing will verify that the application correctly handles normal and unexpected scenarios.

Testing will include:

- Valid message submission

- Empty messages

- Extremely long messages

- Invalid API requests

- Authentication failures

- Unauthorized administrator actions

- Keyword detection

- Priority scoring

- Priority overrides

- Database operations

- Concurrent message submissions

- API error handling

- Frontend validation

- Security vulnerabilities

*Special attention will be given to false positives and false negatives in the priority system.*

For example, the system should be tested against messages such as:

"There is no fire at my house."

This is important because a simplistic keyword search could detect "fire" and incorrectly increase the priority.

Milestone 7 — Final Demonstration

End of Week 10

The final demonstration will show the complete workflow:

```
1. User submits emergency text
   
             ↓
   
2. API receives message
   
             ↓
   
3. Message stored in database

             ↓
4. Analysis service evaluates message

             ↓
5. Priority score calculated
   
             ↓
6. Message appears in admin queue
    
             ↓
7. Administrator reviews message
    
             ↓
8. Administrator confirms/overrides priority
    
             ↓
9. Message status updated
    
             ↓
10. Data appears in analytics
```

---

### 7. Resources & Budget  

The proposed 911 Call Center Analysis application is designed to minimize development and operational costs by using open-source technologies and Google Cloud services with free usage tiers. The project will use synthetic 911 data for development and demonstration purposes.

## Resource Budget

| Layer                  | Technology                           |   Cost | Purpose                                                        |
| ---------------------- | ------------------------------------ | -----: | -------------------------------------------------------------- |
| Frontend               | **React + Vite**                     |     $0 | 911 simulation interface and admin dashboard                   |
| Backend                | **FastAPI**                          |     $0 | REST API and application logic                                 |
| Database               | **MariaDB Community Server**         |     $0 | Store messages, users, analysis, priorities, and audit records |
| ORM                    | **SQLAlchemy**                       |     $0 | Python database interaction                                    |
| Database migrations    | **Alembic**                          |     $0 | Manage database schema changes                                 |
| AI/LLM                 | **Ollama + local open-source model** |     $0 | Local semantic analysis without paying an API provider         |
| Containerization       | **Docker + Docker Compose**          |     $0 | Run the entire application stack consistently                  |
| Reverse proxy          | **Caddy**                            |     $0 | HTTPS and reverse proxy if you expose the application          |
| Version control        | **Git + GitHub**                     |     $0 | Source control and collaboration                               |
| CI/CD                  | **GitHub Actions**                   |     $0 | Automated testing and builds                                   |
| Testing                | **pytest**                           |     $0 | Backend unit/integration testing                               |
| API testing            | **Swagger/OpenAPI**                  |     $0 | Test and document FastAPI endpoints                            |
| Infrastructure         | **Your MacBook**                     |     $0 | Development and local hosting                                  |
| Monitoring             | **Prometheus + Grafana**             |     $0 | Application/system monitoring                                  |
| Logging                | **Loki**                             |     $0 | Centralized application logs                                   |
| Infrastructure-as-code | **Docker Compose**                   |     $0 | Reproducible local infrastructure                              |
| **Total**              |                                      | **$0** |                                                                |


*(If your institution provides free credits, update accordingly.)*

---

### 8. Risk Management  

Several risks could affect the project timeline. To reduce these risks, the project will prioritize the core message submission, database, analysis, and administrative dashboard functionality before implementing advanced features.

**Risk: Scope Expansion**

Features such as machine learning, real-time communications, geospatial mapping, and SMS integration could significantly increase development time.

Mitigation: These features will remain future enhancements unless the MVP is completed ahead of schedule.

**Risk: Automated Classification Accuracy**

Keyword-based classification may produce incorrect priority levels.

Mitigation: The system will treat the automated priority as a recommendation and provide administrators with the ability to override it.

**Risk: Cloud Deployment Problems**

Cloud configuration can introduce unexpected deployment or networking issues.

Mitigation: A local development environment will remain available throughout the project, and cloud deployment will begin by Week 8 rather than being left until the final week.

**Risk: Security Issues**

Emergency-style communications may contain sensitive information.

Mitigation: Only synthetic data will be used, administrator access will require authentication, and security testing will be performed before final deployment.

---

### 9. Deliverables  

| Deliverable | Format | Due |
|-------------|--------|-----|
| Architecture diagram | PNG / PDF | End of Design |
| Terraform IaC code | .tf files (Git repo) | End of Implementation |
| LLM‑Chooser micro‑service | Docker image (ECR) + source | End of Implementation |
| Python SDK (`llm_client.py`) | .py file + docs | End of Implementation |
| React demo instance | URL (staging) | End of Demo |
| Test suite (PyTest, others?) | repo + CI badge | End of Testing |
| Final report & presentation & live demo | PDF + Slides + Demo | End of Evaluation |

---

### 10. References  

The following sources provide the technical and architectural foundations for the technologies, development practices, cloud services, and responsible-AI principles proposed for this project.

## Cloud Infrastructure

1. Google Cloud. (2026). *Cloud Run documentation*. Google Cloud Documentation.
   [Google Cloud Run Documentation](https://cloud.google.com/run/docs?utm_source=chatgpt.com)

   Used to support the proposed containerized application deployment, automatic scaling, service configuration, and cloud-hosted backend architecture.

2. Google Cloud. (2026). *Cloud SQL for PostgreSQL documentation*. Google Cloud Documentation.
   [Cloud SQL for PostgreSQL Documentation](https://docs.cloud.google.com/sql/docs/postgres?utm_source=chatgpt.com)

   Used as the reference for the managed PostgreSQL database component of the application.

3. Google Cloud. (2026). *Pub/Sub documentation*. Google Cloud Documentation.
   [Google Cloud Pub/Sub Documentation](https://docs.cloud.google.com/pubsub/docs?utm_source=chatgpt.com)

   Used to support the proposed optional event-driven architecture for asynchronous message analysis.

4. Google Cloud. (2026). *Secret Manager documentation*. Google Cloud Documentation.
   [Google Cloud Secret Manager Documentation](https://docs.cloud.google.com/secret-manager/docs?utm_source=chatgpt.com)

   Used to support the secure management of database credentials, API keys, and other application secrets.

---

## Backend & Database Technologies

5. FastAPI. (2026). *FastAPI Documentation*.
   [FastAPI Documentation](https://fastapi.tiangolo.com/learn/?utm_source=chatgpt.com)

   Used as the primary reference for the proposed Python REST API framework, API validation, testing, and deployment.

6. PostgreSQL Global Development Group. (2026). *PostgreSQL 18 Documentation*.
   [PostgreSQL Documentation](https://www.postgresql.org/docs/current/index.htm?utm_source=chatgpt.com)

   Used as the technical reference for PostgreSQL database design, SQL, data types, indexes, concurrency, and database administration.

---

## Containerization

7. Docker. (2026). *Docker Documentation*.
   [Docker Documentation](https://docs.docker.com/?utm_source=chatgpt.com)

   Used to support the proposed containerization strategy, Docker images, Dockerfiles, and application deployment workflow.

---

## DevOps & CI/CD

8. GitHub. (2026). *GitHub Actions Documentation*. GitHub Docs.
   [GitHub Actions Documentation](https://docs.github.com/en/actions?utm_source=chatgpt.com)

   Used to support the proposed continuous integration and continuous deployment pipeline.

9. GitHub. (2026). *Continuous Integration with GitHub Actions*. GitHub Docs.
   [GitHub Actions — Continuous Integration](https://docs.github.com/en/actions/get-started/continuous-integration?utm_source=chatgpt.com)

   Used to support automated linting, testing, security checks, and build validation within the CI pipeline.

10. GitHub. (2026). *Continuous Deployment with GitHub Actions*. GitHub Docs.
    [GitHub Actions — Continuous Deployment](https://docs.github.com/en/actions/get-started/continuous-deployment?utm_source=chatgpt.com)

    Used to support automated application deployment following successful CI checks.

---

## Infrastructure as Code

11. HashiCorp. (2026). *Terraform Google Cloud Provider Documentation*. Terraform Registry.
    [Terraform Google Cloud Provider Documentation](https://registry.terraform.io/providers/hashicorp/google/latest/docs?product_intent=terraform&utm_source=chatgpt.com)

    Used as the reference for provisioning and managing Google Cloud infrastructure using Terraform.

Terraform will be used to make the project's cloud infrastructure reproducible and version controlled.

---

## Artificial Intelligence & Responsible AI

12. National Institute of Standards and Technology. (2023). *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. NIST AI 100-1.
    [NIST AI Risk Management Framework](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10?utm_source=chatgpt.com)

    Used to guide the project's approach to AI risk management, evaluation, trustworthiness, and human oversight.

13. National Institute of Standards and Technology. (2024). *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile*. NIST AI 600-1.
    [NIST Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence?utm_source=chatgpt.com)

    Used to address risks and evaluation considerations specific to generative AI and LLM-based functionality.

14. National Institute of Standards and Technology. (2023). *AI RMF — Human-AI Interaction and Oversight*.
    [NIST AI RMF — Human-AI Interaction](https://airc.nist.gov/airmf-resources/airmf/appendices/app-c-ai-risk-management-and-human-ai-interaction/?utm_source=chatgpt.com)

    This reference supports the project's decision to use the LLM as an analytical aid rather than allowing it to autonomously make emergency-dispatch decisions. NIST specifically discusses configurations in which AI provides an additional opinion while a human remains responsible for decision-making and oversight.

---

# 11. Reference-to-Project Mapping

| Project Component       | Primary Reference                   |
| ----------------------- | ----------------------------------- |
| Python REST API         | FastAPI Documentation               |
| PostgreSQL Database     | PostgreSQL Documentation            |
| Cloud-hosted backend    | Google Cloud Run                    |
| Managed PostgreSQL      | Google Cloud SQL                    |
| Containerization        | Docker Documentation                |
| CI/CD                   | GitHub Actions                      |
| Infrastructure as Code  | Terraform Google Cloud Provider     |
| Secret Management       | Google Cloud Secret Manager         |
| Event-driven processing | Google Cloud Pub/Sub                |
| LLM/Generative AI Risk  | NIST AI RMF                         |
| Human-in-the-loop AI    | NIST AI RMF                         |
| AI Evaluation           | NIST AI RMF / Generative AI Profile |
| Cloud Scaling           | Google Cloud Run                    |


**This references section has been formatted with the assistance of AI. All ideas, verbage, and content remain at the discretion of the project owner.**
---  
