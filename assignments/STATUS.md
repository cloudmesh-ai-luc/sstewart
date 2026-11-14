# CatchUp Plan

## Missed classes:

- Oct 29th, will review over the weekend of Friday Nov 13th
- Nov 5th, will review over the weekend of Friday Nov 13th

## Cloudmesh-ai-vm:

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
