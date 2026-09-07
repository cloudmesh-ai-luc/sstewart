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

A managed MariaDB database will store emergency messages and application data.

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


#### 5.2 Open-Source DevOps and Deployment Pipeline  

# DevOps Pipeline

## Overview

The application will use a containerized, open-source DevOps pipeline designed to minimize infrastructure costs while maintaining modern software engineering and deployment practices.

The pipeline will use **GitHub Actions** for continuous integration and continuous deployment, **Docker and Docker Compose** for containerization and deployment, and **GitHub Container Registry (GHCR)** for storing application images.

The core pipeline is:

```text
Developer
    │
    │ git push / pull request
    ▼
┌──────────────────────┐
│       GitHub         │
│  Source Repository   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   GitHub Actions     │
│        CI            │
├──────────────────────┤
│ • Linting            │
│ • Unit Tests         │
│ • Integration Tests  │
│ • Security Checks    │
│ • Frontend Tests     │
└──────────┬───────────┘
           │
       Tests Pass
           │
           ▼
┌──────────────────────┐
│    Docker Build      │
├──────────────────────┤
│ • FastAPI Image      │
│ • React Image        │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ GitHub Container     │
│ Registry (GHCR)      │
└──────────┬───────────┘
           │
           │ deployment
           ▼
┌──────────────────────────────────┐
│       Docker Compose Host        │
├──────────────────────────────────┤
│                                  │
│  ┌────────────┐  ┌────────────┐ │
│  │   React    │  │  FastAPI   │ │
│  │ Container  │  │ Container  │ │
│  └────────────┘  └─────┬──────┘ │
│                         │        │
│             ┌───────────┼──────┐ │
│             │           │      │ │
│             ▼           ▼      ▼ │
│         ┌────────┐ ┌────────┐    │
│         │MariaDB │ │ Ollama │    │
│         │        │ │  LLM   │    │
│         └────────┘ └────────┘    │
│                                  │
│         Caddy Reverse Proxy      │
│                │                 │
│                ▼                 │
│             HTTPS                │
└──────────────────────────────────┘
```

GitHub Actions supports both continuous integration and continuous deployment workflows, including automated testing, building, and deployment.

---

# 1. Source Control

The project source code will be stored in a GitHub repository.

A recommended repository structure is:

```text
911-analysis/
│
├── backend/
│   ├── app/
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── Dockerfile
│
├── database/
│   └── migrations/
│
├── infrastructure/
│   ├── docker-compose.yml
│   ├── docker-compose.dev.yml
│   └── docker-compose.prod.yml
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
│
├── .gitignore
├── README.md
└── LICENSE
```

The repository will use a branch strategy such as:

```text
main
 │
 ├── develop
 │
 ├── feature/message-analysis
 │
 ├── feature/admin-dashboard
 │
 └── feature/llm-integration
```

The `main` branch will contain stable code suitable for deployment.

---

# 2. Continuous Integration

Every pull request and push to the development branches will trigger the CI pipeline.

```text
Git Push / Pull Request
          │
          ▼
    GitHub Actions
          │
          ▼
    Install Dependencies
          │
          ▼
        Linting
          │
          ▼
     Unit Testing
          │
          ▼
  Integration Testing
          │
          ▼
    Security Scanning
          │
          ▼
      Docker Build
          │
          ▼
     CI Successful
```

GitHub Actions can automatically run tests when code is pushed or when pull requests are created, allowing problems to be detected before changes are merged.

## CI Tasks

### Backend

The backend CI pipeline will:

* Install Python dependencies.
* Run formatting checks.
* Run linting.
* Run unit tests.
* Run API integration tests.
* Test database interactions.
* Test keyword analysis.
* Test priority calculations.
* Test Ollama integration using controlled test responses.
* Check test coverage.

Example:

```bash
pip install -r requirements.txt

ruff check .

pytest

pytest --cov=app
```

### Frontend

The frontend pipeline will:

```bash
npm ci

npm run lint

npm test

npm run build
```

---

# 3. Database Testing

The CI environment will use a temporary MariaDB container.

```text
GitHub Actions
      │
      ▼
Docker Compose
      │
      ├── FastAPI
      │
      └── MariaDB
             │
             ▼
       Integration Tests
```

This ensures that database-dependent tests are executed against the same database technology used by the application.

Docker Compose is particularly useful here because it can define the application, database, networks, and volumes in a single configuration file and can be used in CI environments.

---

# 4. Security Testing

The CI pipeline will perform automated security checks before an application can be deployed.

Potential checks include:

* Dependency vulnerability scanning.
* Python package vulnerability scanning.
* JavaScript dependency auditing.
* Docker image vulnerability scanning.
* Secret detection.
* Static analysis.
* Configuration validation.

Example tools include:

```text
Python:
    Ruff
    Bandit
    pip-audit

JavaScript:
    npm audit

Docker:
    Docker Scout
    Trivy

Secrets:
    Gitleaks
```

Docker provides official GitHub Actions that can build images and perform security analysis of Docker images.

---

# 5. Docker Build

After all tests pass, GitHub Actions will build the application containers.

The primary application containers will be:

```text
┌──────────────────────┐
│ React Container      │
│ Frontend             │
└──────────────────────┘

┌──────────────────────┐
│ FastAPI Container    │
│ Backend/API          │
└──────────────────────┘

┌──────────────────────┐
│ MariaDB Container    │
│ Database             │
└──────────────────────┘

┌──────────────────────┐
│ Ollama Container     │
│ Local LLM            │
└──────────────────────┘

┌──────────────────────┐
│ Caddy Container      │
│ Reverse Proxy        │
└──────────────────────┘
```

The containers will be defined using Dockerfiles and managed together through Docker Compose.

---

# 6. Container Image Registry

After successful CI testing, Docker images can be published to **GitHub Container Registry (GHCR)**.

```
GitHub Actions
      │
      ▼
Docker Build
      │
      ▼
Security Scan
      │
      ▼
GHCR
      │
      ▼
Versioned Docker Image
```

GitHub supports publishing Docker images to GitHub Container Registry directly through GitHub Actions.

Images should use identifiable version tags.

Example:

```
ghcr.io/username/911-backend:1.0.0
ghcr.io/username/911-frontend:1.0.0
```

For development builds:

```
ghcr.io/username/911-backend:develop
```

For production releases:

```
ghcr.io/username/911-backend:v1.0.0
```

This allows deployments to be traced back to a specific application version.

---

# 7. Continuous Deployment

Once the `main` branch passes all CI checks, the CD workflow can deploy the new version.

```text
             main branch
                  │
                  ▼
          GitHub Actions
                  │
                  ▼
          Run CI Pipeline
                  │
             Tests Pass
                  │
                  ▼
           Build Images
                  │
                  ▼
           Push to GHCR
                  │
                  ▼
        Deployment Host
                  │
                  ▼
        docker compose pull
                  │
                  ▼
        docker compose up -d
                  │
                  ▼
           Health Checks
                  │
                  ▼
             Deployment
             Successful
```

GitHub Actions supports automated deployment workflows and can restrict deployments to specific branches or environments.

---

# 8. Docker Compose Deployment

The deployment host will use Docker Compose to run the application.

Example architecture:

```
services:

  frontend:
    image: ghcr.io/username/911-frontend:latest

  backend:
    image: ghcr.io/username/911-backend:latest
    depends_on:
      - mariadb
      - ollama

  mariadb:
    image: mariadb:latest
    volumes:
      - mariadb_data:/var/lib/mysql

  ollama:
    image: ollama/ollama

  caddy:
    image: caddy:latest
    depends_on:
      - frontend
      - backend

volumes:
  mariadb_data:
```

The actual production configuration will pin specific image versions rather than relying on `latest`.

---

# 9. Database Deployment

Database migrations will be handled using **Alembic**.

The deployment process will be:

```text
New Application Version
          │
          ▼
     Pull Containers
          │
          ▼
    Database Backup
          │
          ▼
    Run Alembic Migration
          │
          ▼
     Start Application
          │
          ▼
     Health Check
```

Database migrations should be designed to be backward-compatible whenever possible.

For example:

```text
Version 1
    │
    ▼
Add new nullable column
    │
    ▼
Deploy application
    │
    ▼
Populate existing records
    │
    ▼
Enable new functionality
```

This reduces the risk of application downtime during deployments.

---

# 10. Ollama Deployment

Ollama will provide the local LLM inference layer.

The architecture will be:

```text
FastAPI
   │
   │ HTTP request
   ▼
Ollama API
   │
   ▼
Local LLM
   │
   ▼
Structured Analysis
   │
   ▼
FastAPI
```

The application will **not** allow the LLM to directly modify priority records or make dispatch decisions.

Instead:

```
911 Message
     │
     ├───────────────┐
     ▼               ▼
Keyword Engine    Ollama
     │               │
     │               ▼
     │         Semantic Analysis
     │               │
     └───────┬───────┘
             ▼
       Priority Engine
             │
             ▼
       Human Review
```

The LLM therefore functions as an analysis component rather than an autonomous emergency-dispatch system.

---

# 11. Monitoring

The application will use open-source monitoring tools.

```
Application
     │
     ├──────────────┐
     │              │
     ▼              ▼
Prometheus        Loki
     │              │
     ▼              ▼
          Grafana
             │
             ▼
       Monitoring Dashboard
```

Metrics can include:

* API response time
* HTTP status codes
* Request volume
* Database connections
* Database errors
* LLM response time
* LLM failures
* Analysis processing time
* CPU usage
* Memory usage
* Container health
* Number of analyzed messages

---

# 12. Health Checks

Each major service should expose or support a health check.

Example:

```text
GET /health
```

Expected response:

```json
{
  "status": "healthy",
  "database": "healthy",
  "ollama": "healthy"
}
```

Docker Compose can then be used to manage service startup and health dependencies.

---

# 13. Deployment Verification

After deployment, the CD pipeline will perform automated smoke tests.

```text
Deployment
    │
    ▼
Health Check
    │
    ▼
API Test
    │
    ▼
Database Test
    │
    ▼
LLM Test
    │
    ▼
Frontend Test
    │
    ▼
Deployment Confirmed
```

Example tests:

```
GET /health                 → 200 OK

POST /messages              → 201 Created

GET /messages/{id}          → 200 OK

POST /messages/{id}/analyze → 200 OK

GET /admin/messages         → 200 OK
```

If a critical health check fails, the deployment should be considered unsuccessful.

---

# 14. Rollback Strategy

Each Docker image will have a version number.

For example:

```
v1.0.0
v1.1.0
v1.2.0
```

If version `v1.2.0` fails:

```
v1.2.0
   │
   ▼
Deployment Failure
   │
   ▼
Restore v1.1.0
   │
   ▼
docker compose pull
   │
   ▼
docker compose up -d
```

This provides a simple rollback mechanism without requiring a complex cloud orchestration platform.

---

# 15. Complete Pipeline

The final DevOps lifecycle will be:

```
┌───────────────────────┐
│      Developer        │
└───────────┬───────────┘
            │
            │ git push / PR
            ▼
┌───────────────────────┐
│       GitHub          │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│    GitHub Actions     │
│                       │
│  Lint                 │
│  Unit Tests            │
│  Integration Tests     │
│  Security Scans        │
│  Build                 │
└───────────┬───────────┘
            │
       Tests Pass
            │
            ▼
┌───────────────────────┐
│     Docker Build      │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Security / Image Scan │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│         GHCR          │
│ Docker Image Registry │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│   Deployment Host     │
│                       │
│   Docker Compose      │
└───────────┬───────────┘
            │
     ┌──────┼─────────┐
     │      │         │
     ▼      ▼         ▼
  React  FastAPI   MariaDB
             │
             ▼
           Ollama
             │
             ▼
       Local LLM
            │
                        ▼
┌───────────────────────┐
│  Prometheus / Loki    │
│       + Grafana       │
└───────────────────────┘
```

## Definition of "Done"

A deployment will be considered successful when:

* [ ] All automated tests pass.
* [ ] Code passes linting and static analysis.
* [ ] Dependencies have been checked for known vulnerabilities.
* [ ] Docker images build successfully.
* [ ] Docker images pass security scanning.
* [ ] Images are published to GHCR.
* [ ] Database migrations complete successfully.
* [ ] MariaDB is accessible.
* [ ] Ollama is accessible.
* [ ] FastAPI health check returns `200 OK`.
* [ ] React frontend loads successfully.
* [ ] API smoke tests pass.
* [ ] LLM analysis test succeeds.
* [ ] Monitoring services are operational.
* [ ] Application logs are available.
* [ ] Deployment version is recorded.
* [ ] Previous version can be restored if necessary.                    

### 5.3 Architecture Component Description

1. Not yet sure if this is needed, we can simulate with a mock service, which actually may be better: **F/OSS SMS Gateway:** Replaces paid commercial APIs. This could be a self-hosted Kannel server connected to a cellular modem (SMPP) or an open-source Android application that forwards received SMS messages via HTTP POST to the API layer.
2. **FastAPI Application:** The central integration point. It handles HTTP requests from the gateway, invokes the Triage Engine, manages database transactions, and pushes real-time updates to the dashboard via WebSockets.
3. **Triage Engine:** A distinct Python module that performs keyword analysis on message bodies to calculate priority scores (see Section 3).
4. **PostgresSQL:** The source of truth. It stores session state, full message logs, and dispatcher activity logs with full ACID compliance.
5. **Admin Dispatch Dashboard:** A React-based single-page application that provides dispatchers with a live view of incoming emergencies, sorted by priority.

---

## MariaDB Database Schema

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

A user will be able to submit a simulated 911 text message through the React application, send it to the Spring Boot API, and have it persisted in MariaDB
.

The complete workflow will be:

User
  ↓
React Application
  ↓
REST API
  ↓
MariaDB

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



*Usage limits and account/repository configuration may apply.
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
### 10. PostgreSQL vs. MariaDB

*Database Selection: PostgreSQL vs. MariaDB*

The 911 Call Center Analysis application requires a relational database capable of storing simulated 911 messages, user accounts, emergency classifications, keyword-analysis results, LLM analysis results, priority scores, and audit records. Two suitable open-source database options considered for the project are *PostgreSQL* and *MariaDB*.

Both databases provide the relational functionality required by the application and are available without software licensing costs. PostgreSQL is distributed under the PostgreSQL License, a permissive open-source license similar to the BSD and MIT licenses. MariaDB Community Server is distributed under the GNU General Public License v2.

After comparing the requirements of the application, MariaDB is selected as the preferred database for this project because it provides the required relational capabilities while fitting particularly well with the project's goal of creating a completely free, open-source, containerized infrastructure.

*Why Postgres was considered*

PostgreSQL is a powerful open-source object-relational database system with support for foreign keys, transactions, triggers, complex queries, extensibility, and multiversion concurrency control. It is also available free of charge for academic and commercial use.

PostgreSQL would therefore be a completely valid choice for this application. It would be particularly attractive if the project required sophisticated analytical queries, advanced database extensions, or more complex data-processing workloads.

However, many of these capabilities exceed the requirements of the proposed prototype.

The application primarily needs to:

Store simulated 911 messages.
Store user and administrator information.
Store message classifications.
Store keyword-analysis results.
Store LLM analysis results.
Store priority levels.
Retrieve messages efficiently.
Maintain relationships between messages and their analyses.
Maintain an audit history.
Support standard CRUD operations.
Perform basic filtering, sorting, and reporting.

These requirements do not require many of PostgreSQL's more advanced capabilities.

*Why MariaDB Is Ideal for This Project*

1. Completely Open Source

MariaDB Community Server is released under the GNU General Public License v2 and is explicitly maintained as an open-source database.

This directly supports the project's objective of creating a zero-cost software infrastructure, meets the requirements for a CRUD based application, and is appropriate for the projected scale of the project. 

The project does not need to purchase a database license, enterprise database software, or proprietary development tools.

2. Excellent Fit for a CRUD-Based Application

The primary operations of the application will involve:

```
CREATE
    ↓
911 Message

READ
    ↓
Admin Dashboard

UPDATE
    ↓
Human Review / Priority

DELETE
    ↓
Data Management
```

MariaDB is well suited to this type of workload.

3. Strong Compatibility with the Proposed Technologies

The proposed backend architecture uses:

Python
   ↓
FastAPI
   ↓
SQLAlchemy
   ↓
MariaDB

SQLAlchemy provides the database abstraction layer between the Python application and MariaDB.

This means the application code can remain relatively independent of the underlying database implementation.

For example:

class Message:
    id
    user_id
    message_text
    created_at
    priority

The application can interact with the model through SQLAlchemy rather than embedding large amounts of database-specific SQL throughout the FastAPI application.

This also improves the project's future portability.

4. Excellent Docker Compatibility

MariaDB can be deployed as a Docker container alongside the other components of the application.

The proposed infrastructure can therefore be defined through Docker Compose:

Docker Compose
│
├── React
│
├── FastAPI
│
├── MariaDB
│
├── Ollama
│
├── Caddy
│
└── Monitoring

This creates a reproducible development environment in which the database does not need to be installed directly on the developer's operating system.

MariaDB also provides official Docker installation options through its Community Server distribution.

5. Familiar SQL-Based Development Model

MariaDB uses SQL and shares significant compatibility with the MySQL ecosystem. MariaDB was originally created by the developers behind MySQL and maintains substantial compatibility with MySQL protocols, clients, APIs, and tools.

This provides an additional benefit for the project because SQL knowledge developed while working with MariaDB is broadly applicable to other relational database environments.

6. Appropriate for the Project's Expected Scale

The proposed application is an academic prototype, not a production 911 emergency dispatch system.

The expected workload will consist primarily of:

A relatively small number of simulated users.
A relatively small message database.
Administrative queries.
Automated analysis requests.
Development and testing traffic.

There is therefore little justification for introducing additional database complexity that the project does not require.

MariaDB provides more than enough capacity for this scale while keeping the infrastructure straightforward.

7. Supports the Zero-Cost Infrastructure Goal

One of the major changes to the project architecture is the decision to prioritize free and open-source infrastructure.

The revised stack can therefore be represented as:
```
Frontend
React
  │
  ▼
Backend
FastAPI
  │
  ▼
Database
MariaDB
  │
  ├── Message Data
  ├── User Data
  ├── Keyword Analysis
  ├── LLM Analysis
  ├── Priority Results
  └── Audit Records
```
All of these components can run locally using free software.

This eliminates the requirement for a paid managed database service such as Google Cloud SQL during development.

MariaDB's Role in the Overall Architecture

The database will intentionally have a focused responsibility within the architecture.

MariaDB will store and retrieve application data, while other components will perform specialized processing.

                  911 Message
                       │
                       ▼
                   FastAPI
                       │
            ┌──────────┴──────────┐
            │                     │
            ▼                     ▼
     Keyword Engine           Ollama
            │                     │
            │              Local LLM Analysis
            │                     │
            └──────────┬──────────┘
                       ▼
                Priority Engine
                       │
                       ▼
                   MariaDB
                       │
            ┌──────────┴──────────┐
            │                     │
            ▼                     ▼
      Admin Dashboard        Audit Records

This separation of responsibilities follows a modular architecture:

- FastAPI manages application and API logic.
- MariaDB manages persistent relational data.
- Keyword Engine performs deterministic analysis.
- Ollama performs semantic LLM analysis.
- Priority Engine combines analysis results.
- React provides the user interface.
- Caddy manages external HTTP/HTTPS access.
- Prometheus/Grafana provide observability.


**Limitations and Tradeoffs**

MariaDB is not being selected because it is objectively superior to PostgreSQL.

PostgreSQL has several advantages that could make it the better choice for a different version of this project. PostgreSQL provides extensive extensibility and advanced database functionality and is particularly strong for complex queries and sophisticated data workloads.

MariaDB also has differences from PostgreSQL that should be acknowledged. The two database systems are not interchangeable, and applications should be tested against their target database rather than assuming complete SQL compatibility.

For this project, however, those differences are unlikely to create significant problems because the application primarily requires conventional relational database functionality.

**Final Decision**

MariaDB will be used as the primary relational database for the 911 Call Center Analysis application.

The decision is based on the following factors:

1. $0 software licensing cost.
2. Strong open-source commitment.
3. Sufficient relational functionality for the application's requirements.
4. Excellent compatibility with Docker and Docker Compose.
5. Straightforward integration with Python, FastAPI, and SQLAlchemy.
6. Strong support for conventional CRUD and transactional workloads.
7. Familiar SQL-based development model.
8. Appropriate complexity for an academic prototype.
9. Alignment with the project's goal of completely free infrastructure.
10. Ability to maintain a modular architecture that could support a future database migration if requirements change.

Overall, MariaDB provides the necessary functionality without introducing unnecessary infrastructure complexity. Its combination of open-source licensing, relational capabilities, Docker compatibility, and suitability for the application's expected workload makes it the most appropriate database for the proposed implementation.

### 11. References  

The following references document the technologies and infrastructure used in the proposed 911 Call Center Analysis application. Official documentation and primary project sources are preferred where available.

1. **MariaDB Foundation.** (2026). *MariaDB Community Server*.
   MariaDB Community Server is the open-source relational database used to store simulated 911 messages, user information, analysis results, priority levels, and audit records. MariaDB Community Server is released under the GNU General Public License v2.0.
   https://mariadb.com/products/community-server/

2. **Ollama.** (2026). *Ollama Documentation — API Introduction*.
   Ollama provides a local runtime and API for running and interacting with large language models. It will be used to provide local semantic analysis of simulated 911 messages without requiring a paid external AI API.
   https://docs.ollama.com/api/introduction

3. **Ollama.** (2026). *Ollama GitHub Repository*.
   The Ollama source repository provides implementation details, source code, licensing information, and documentation for the Ollama project. The Ollama repository is distributed under the MIT License.
   https://github.com/ollama/ollama

4. **FastAPI.** (2026). *FastAPI Documentation*.
   FastAPI is the Python web framework used to implement the application's REST API and backend services.
   https://fastapi.tiangolo.com/

5. **React.** (2026). *React Documentation*.
   React is used to develop the application's simulated 911 messaging interface and administrative dashboard.
   https://react.dev/

6. **SQLAlchemy.** (2026). *SQLAlchemy Documentation*.
   SQLAlchemy provides the Python SQL toolkit and Object Relational Mapper used to interact with the MariaDB database from the FastAPI backend.
   https://docs.sqlalchemy.org/

7. **Alembic.** (2026). *Alembic Documentation*.
   Alembic is a database migration tool designed for use with SQLAlchemy. It will be used to manage database schema changes throughout development.
   https://alembic.sqlalchemy.org/

8. **Docker.** (2026). *Docker Documentation*.
   Docker provides containerization capabilities for packaging the FastAPI backend, MariaDB database, Ollama service, and supporting infrastructure into reproducible environments.
   https://docs.docker.com/

9. **Docker.** (2026). *Docker Compose Documentation*.
   Docker Compose will be used to define and run the application's multi-container development environment.
   https://docs.docker.com/compose/

10. **Caddy.** (2026). *Caddy Documentation — Reverse Proxy*.
    Caddy can serve as the application's reverse proxy and provide automatic HTTPS when the application is deployed to a publicly accessible domain.
    https://caddyserver.com/docs/quick-starts/reverse-proxy

11. **Prometheus Authors.** (2026). *Prometheus Documentation*.
    Prometheus is an open-source monitoring and alerting system that can collect application and infrastructure metrics for the project.
    https://prometheus.io/docs/introduction/overview/

12. **Grafana Labs.** (2026). *Grafana Open Source Documentation*.
    Grafana OSS can be used to visualize application metrics, logs, and other observability data collected from the application infrastructure.
    https://grafana.com/docs/grafana/latest/

13. **GitHub.** (2026). *GitHub Actions Documentation*.
    GitHub Actions provides the project's continuous integration and continuous delivery (CI/CD) capabilities, including automated testing, builds, and deployment workflows.
    https://docs.github.com/en/actions

14. **Python Software Foundation.** (2026). *Python Documentation*.
    Python is the primary programming language used to implement the FastAPI backend, keyword analysis engine, priority engine, and Ollama integration.
    https://docs.python.org/

15. **pytest Development Team.** (2026). *pytest Documentation*.
    pytest will be used to implement automated unit and integration tests for the backend and analysis components.
    https://docs.pytest.org/

16. **NIST.** (2023). *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. National Institute of Standards and Technology.
    The NIST AI Risk Management Framework provides guidance for managing risks associated with artificial intelligence systems. It supports the project's use of human oversight, evaluation, transparency, and risk management when incorporating LLM-based analysis.
    https://www.nist.gov/itl/ai-risk-management-framework

17. **NIST.** (2024). *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile*. National Institute of Standards and Technology.
    The Generative AI Profile provides additional guidance for identifying and managing risks associated with generative AI systems and is relevant to the project's use of an LLM for semantic message analysis.
    https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence

## 8. Reference-to-Project Mapping

| Technology / Concept   | Primary Reference            | Project Purpose                           |
| ---------------------- | ---------------------------- | ----------------------------------------- |
| **MariaDB**            | MariaDB Community Server     | Relational database                       |
| **Ollama**             | Ollama Documentation         | Local LLM execution and semantic analysis |
| **FastAPI**            | FastAPI Documentation        | REST API and backend                      |
| **React**              | React Documentation          | User interface and admin dashboard        |
| **SQLAlchemy**         | SQLAlchemy Documentation     | Database access and ORM                   |
| **Alembic**            | Alembic Documentation        | Database migrations                       |
| **Docker**             | Docker Documentation         | Application containerization              |
| **Docker Compose**     | Docker Compose Documentation | Multi-container infrastructure            |
| **Caddy**              | Caddy Documentation          | Reverse proxy and HTTPS                   |
| **Prometheus**         | Prometheus Documentation     | Metrics and monitoring                    |
| **Grafana**            | Grafana Documentation        | Monitoring dashboards and visualization   |
| **GitHub Actions**     | GitHub Actions Documentation | CI/CD automation                          |
| **pytest**             | pytest Documentation         | Automated testing                         |
| **NIST AI RMF**        | NIST                         | AI risk management and human oversight    |
| **NIST GenAI Profile** | NIST                         | Generative AI risk management             |

## 9. Infrastructure Philosophy

The project prioritizes **free and open-source software (FOSS)** wherever practical. The core application can therefore be developed and demonstrated without requiring paid cloud infrastructure or proprietary software licenses.

The proposed infrastructure consists primarily of:

* React
* FastAPI
* MariaDB
* SQLAlchemy
* Alembic
* Ollama
* Docker
* Docker Compose
* Caddy
* Prometheus
* Grafana
* GitHub Actions
* pytest

This approach reduces the project's financial requirements while providing practical experience with modern application development, containerization, database management, AI integration, CI/CD, monitoring, and security.

The architecture is also designed to remain portable. If additional resources become available, the containerized application can later be deployed to a cloud provider without requiring a fundamental redesign of the application.



**This references section has been formatted with the assistance of AI. All ideas, verbage, and content remain at the discretion of the project owner.**
---

