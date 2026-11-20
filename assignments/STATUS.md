# CatchUp Plan

## Missed classes:

- Oct 29th, reviewed the weekend of Friday Nov 13th
- Nov 5th, reviewed over the weekend of Friday Nov 13th

## Cloudmesh-ai-vm:

Always review all:
* Issues: <https://github.com/cloudmesh-ai/cloudmesh-ai-vm/issues>
* PRs: <https://github.com/cloudmesh-ai/cloudmesh-ai-vm/pulls>

### Provider A: Jetstream
  
- Status: ?
-  Suggestion (GvL):
   - weekly:
     - run smoke tests including the one you created
     - verify status and purge work
     - verify floating ip assignment works and is done before vm is started
     - make sure everything is implemented
     - use issues and only file missing issues, e.g. look over all issues before filing ne once, verify with LLM.
     - create pull requests
     - post in piazza to class mates that also do jetstream your findings while pointing to the urls of issues and pull requests
     - make sure issue suggestions PRs are no halucinations and do not regress code (make it worth)
       
### Provider B: Google Cloud
  
- Status: Not yet started
- Suggestion  (GvL):
  - weekly:
    - same as Jetstream 

- Provider C: Multipass
  - Status:  ?
  - Suggestion (Gvl):
    - weekley:
      - same as Jetstream  

## Project: 911 Text Analysis

- Issues are to be documented in https://github.com/cloudmesh-ai-luc/sstewart/issues 
- Suggestion (GvL): Limit implementation on one cloud so you can finish, as Cloudmesh-ai-vm task is behind. Pick just one of jetstream or chameleon.
- Suggestion (GVl): use cmx to manage your vms to simplify. YOu can also use ansible, but I find this for your project to complex. Make sure if you use cmx to create 
  - make vms-start - starts your vms
  - make vms-stop - deletes your vms or at least shelves them (as stopping them only used $)
  - make serve - starts the services
  - make test - creates some test
- If knowledable with docker, you could use docker compose on the VM(s).

### Week of November 13th

- Spend 5 hours working on project to establish reliable database connection and routing, send a test message and see it persists in the database,
  start thinking about Ollama implementation using AI assisted implementation
- Update TODO.md and start thinking about remaining aspects of project

### Next Steps

- Meet with Professor Gregor to review what needs to be done with my 3 cloud providers (Can be done Sat, or Sunday if desired so you can make quickly progress, propose time slots Gregor has not yet a fixed schedule.)
- Continue to work on project, hoping to have the front end started by Thanksgiving week
  - Suggestion: Use an LLM to plan and create draft this weekend if possible (e.g. before Thanksgiving) 
- Continue to contribute to cloudmesh-ai-vm project (Suggestion: Great you understand what is to be done).

### Week of November 20th

Completed
1. Installed and configured MariaDB 13.0.2 using Homebrew on macOS.
2. Resolved MariaDB startup issues caused by an old recovery-mode process running with --skip-grant-tables and networking disabled.
3. Enabled TCP networking and verified:
   - Host: 127.0.0.1
   - Port: 3306
   - skip_networking: OFF
4. Created the application database and user:
   - Database: 911_analysis
   - User: analysis_user
   - Configured database permissions without using root for application access.
5. Established external configuration management using $HOME/.config/911/env to store database credentials securely.
6. Updated the backend database architecture to use:
   - SQLAlchemy
   - MariaDB Connector/Python
   - A shared database engine and session factory
   - Existing SQLAlchemy models for Operator, EmergencyMessage, and MessageEvent.
7. Verified database connectivity through SQLAlchemy. Successfully executed a query returning the database name and MariaDB version.
- Update TODO.md and start thinking about remaining aspects of project
- Work on 3 issues found when working with Professor Gregor (~ 7-8 hours)
### Next Steps

- Continue to work on project, hoping to have the front end started by Thanksgiving week
  - Suggestion: Use an LLM to plan and create draft this weekend if possible (e.g. before Thanksgiving) 
- Continue to contribute to cloudmesh-ai-vm project (Suggestion: Great you understand what is to be done).



