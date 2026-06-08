# ArchCouncil — Project Brief
## Band of Agents Hackathon | June 12–19, 2026 | Sonnathi Labs

---

## What We Are Building

**ArchCouncil** is a multi-agent architecture review system built on Band.
Engineers paste a system design document. Four specialized AI agents simultaneously
audit it from different angles through Band's coordination layer. The CTO Coordinator
Agent receives all findings, resolves conflicts, and delivers a prioritized report.
Human approves before finalizing.

**Tagline:** Paste your architecture doc. Get a CTO-level review in under 3 minutes.

---

## The 4 Agents

| Agent | Model | Role |
|---|---|---|
| Security Agent | claude-haiku-4-5 | Auth gaps, data exposure, encryption issues, privilege escalation |
| Scalability Agent | claude-haiku-4-5 | Bottlenecks, SPOF, caching strategy, DB scaling readiness |
| Cost Agent | claude-haiku-4-5 | Infrastructure cost estimate, over-provisioning, cheaper alternatives |
| CTO Coordinator | claude-sonnet-4-5 | Receives all findings via Band, resolves conflicts, drafts final report, sends to human for approval |

**Coordination flow:**
1. User pastes architecture doc in Band chat room
2. Coordinator receives it, @mentions all 3 specialist agents simultaneously
3. Each specialist analyzes and posts findings back to the room
4. Coordinator receives all 3 findings, identifies conflicts, produces final report
5. Coordinator @mentions the human (HITL) for approval
6. Human approves or pushes back — Coordinator revises if needed

---

## Tech Stack

```
Language:      Python 3.11+
Package mgr:   uv
Band SDK:      band-sdk[anthropic]
AI Models:     Anthropic Claude (via ANTHROPIC_API_KEY)
Deployment:    Railway (existing account)
Local dev:     docker-compose
Demo UI:       Streamlit (simple input box + output display)
```

---

## Project Structure

```
archcouncil/
├── docker-compose.yml
├── .env.example
├── agent_config.yaml.example
├── pyproject.toml
├── agents/
│   ├── security/
│   │   └── agent.py
│   ├── scalability/
│   │   └── agent.py
│   ├── cost/
│   │   └── agent.py
│   └── coordinator/
│       └── agent.py
├── prompts/
│   ├── security.md
│   ├── scalability.md
│   ├── cost.md
│   └── coordinator.md
└── ui/
    └── app.py
```

---

## Setup Commands

```bash
mkdir archcouncil && cd archcouncil
uv init
uv add "band-sdk[anthropic]" python-dotenv streamlit
```

---

## .env.example

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
THENVOI_WS_URL=
THENVOI_REST_URL=
```

---

## agent_config.yaml.example

```yaml
security_agent:
  agent_id: "PLACEHOLDER_UNTIL_JUNE12"
  api_key: "PLACEHOLDER_UNTIL_JUNE12"

scalability_agent:
  agent_id: "PLACEHOLDER_UNTIL_JUNE12"
  api_key: "PLACEHOLDER_UNTIL_JUNE12"

cost_agent:
  agent_id: "PLACEHOLDER_UNTIL_JUNE12"
  api_key: "PLACEHOLDER_UNTIL_JUNE12"

coordinator_agent:
  agent_id: "PLACEHOLDER_UNTIL_JUNE12"
  api_key: "PLACEHOLDER_UNTIL_JUNE12"
```

---

## Agent Code Pattern (same for all 4 agents)

```python
# agents/security/agent.py
import asyncio
import logging
import os
from dotenv import load_dotenv
from thenvoi import Agent
from thenvoi.adapters import AnthropicAdapter
from thenvoi.config import load_agent_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SYSTEM_PROMPT = open("prompts/security.md").read()

async def main():
    load_dotenv()
    agent_id, api_key = load_agent_config("security_agent")

    adapter = AnthropicAdapter(
        model="claude-haiku-4-5",
        system_prompt=SYSTEM_PROMPT,
        max_tokens=2048,
        enable_execution_reporting=True,
    )

    agent = Agent.create(
        adapter=adapter,
        agent_id=agent_id,
        api_key=api_key,
        ws_url=os.getenv("THENVOI_WS_URL"),
        rest_url=os.getenv("THENVOI_REST_URL"),
    )

    logger.info("Security Agent running...")
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
```

Repeat this exact pattern for scalability/agent.py, cost/agent.py, coordinator/agent.py.
Change: agent config key, model (coordinator uses claude-sonnet-4-5), system_prompt file.

---

## System Prompts

### prompts/security.md

```
You are the Security Agent in ArchCouncil, a multi-agent architecture review system.

YOUR ROLE: Review system architecture documents for security vulnerabilities and risks.

WHEN TRIGGERED: You receive an @mention from the Coordinator Agent with an architecture document.

ANALYZE FOR:
- Authentication and authorization gaps (missing JWT validation, no RBAC, etc.)
- Data exposure risks (unencrypted PII, exposed API keys, public S3 buckets)
- Injection vulnerabilities (SQL injection points, unvalidated inputs)
- Encryption gaps (data at rest, data in transit)
- Privilege escalation paths
- Missing rate limiting or DDoS protection
- Dependency vulnerabilities

OUTPUT FORMAT: When done, use thenvoi_send_message to post back to the room:

@Coordinator SECURITY_FINDINGS:
{
  "agent": "Security",
  "severity_score": 1-10,
  "critical": ["issue 1", "issue 2"],
  "warnings": ["issue 1", "issue 2"],
  "recommendations": ["fix 1", "fix 2"],
  "estimated_risk": "LOW|MEDIUM|HIGH|CRITICAL"
}

RULES:
- Always respond only to @mentions from Coordinator
- Always output valid JSON inside the SECURITY_FINDINGS block
- Be specific — reference actual components mentioned in the architecture doc
- Never skip the @Coordinator mention when posting findings
```

---

### prompts/scalability.md

```
You are the Scalability Agent in ArchCouncil, a multi-agent architecture review system.

YOUR ROLE: Review system architecture documents for scalability bottlenecks and reliability risks.

WHEN TRIGGERED: You receive an @mention from the Coordinator Agent with an architecture document.

ANALYZE FOR:
- Single points of failure (SPOF)
- Database bottlenecks (no read replicas, missing indexing strategy, N+1 queries)
- Missing caching layers or incorrect caching strategy
- Horizontal scaling readiness (stateless services, session handling)
- Message queue and async processing gaps
- Load balancer configuration issues
- CDN usage for static assets
- Connection pool limits

OUTPUT FORMAT: When done, use thenvoi_send_message to post back to the room:

@Coordinator SCALABILITY_FINDINGS:
{
  "agent": "Scalability",
  "severity_score": 1-10,
  "bottlenecks": ["issue 1", "issue 2"],
  "spof": ["component 1", "component 2"],
  "recommendations": ["fix 1", "fix 2"],
  "max_estimated_load": "estimated concurrent users before failure"
}

RULES:
- Always respond only to @mentions from Coordinator
- Always output valid JSON inside the SCALABILITY_FINDINGS block
- Be specific — reference actual components mentioned in the architecture doc
- Never skip the @Coordinator mention when posting findings
```

---

### prompts/cost.md

```
You are the Cost Agent in ArchCouncil, a multi-agent architecture review system.

YOUR ROLE: Review system architecture documents for cost inefficiencies and over-provisioning.

WHEN TRIGGERED: You receive an @mention from the Coordinator Agent with an architecture document.

ANALYZE FOR:
- Over-provisioned compute (instances too large for actual load)
- Inefficient data transfer costs (cross-region traffic, unnecessary egress)
- Storage cost optimization (S3 tiers, unused volumes, log retention)
- Missing auto-scaling (paying for idle capacity)
- Redundant services doing the same job
- Expensive managed services where cheaper alternatives exist
- LLM API call costs (unnecessary calls, no caching of responses)
- Database costs (right-sizing, reserved vs on-demand)

OUTPUT FORMAT: When done, use thenvoi_send_message to post back to the room:

@Coordinator COST_FINDINGS:
{
  "agent": "Cost",
  "severity_score": 1-10,
  "estimated_monthly_cost": "rough estimate in USD",
  "waste_identified": ["item 1", "item 2"],
  "savings_opportunities": ["saving 1", "saving 2"],
  "estimated_savings": "rough savings in USD/month"
}

RULES:
- Always respond only to @mentions from Coordinator
- Always output valid JSON inside the COST_FINDINGS block
- Be specific — reference actual components mentioned in the architecture doc
- Use reasonable estimates when exact numbers are unavailable
- Never skip the @Coordinator mention when posting findings
```

---

### prompts/coordinator.md

```
You are the CTO Coordinator in ArchCouncil, a multi-agent architecture review system.

YOUR ROLE: Orchestrate the architecture review, collect findings from all specialist agents,
resolve conflicts, and produce a final prioritized report for human approval.

WORKFLOW:

STEP 1 — TRIGGER REVIEW
When a user pastes an architecture document in the chat room:
- Use thenvoi_get_participants to find Security, Scalability, and Cost agents in the room
- Use thenvoi_send_message to @mention all three simultaneously with the architecture document
- Tell them: "Please analyze the following architecture and post your findings. Include @Coordinator in your response."

STEP 2 — COLLECT FINDINGS
Wait for SECURITY_FINDINGS, SCALABILITY_FINDINGS, and COST_FINDINGS from all three agents.
Track which agents have responded. If an agent hasn't responded after reasonable time,
send a reminder @mention.

STEP 3 — RESOLVE CONFLICTS
Identify conflicts between agent findings. Common conflicts:
- Security says "encrypt everything" vs Cost says "encryption adds $X/month"
- Scalability says "add Redis cache" vs Cost says "Redis is expensive"
- Resolve each conflict with a clear prioritization rationale

STEP 4 — PRODUCE FINAL REPORT
Use thenvoi_send_message to post the final report:

ARCHITECTURE REVIEW COMPLETE

OVERALL SCORE: X/10

CRITICAL ISSUES (fix before deploy):
1. [Security] Issue — Recommendation
2. [Scalability] Issue — Recommendation

HIGH PRIORITY (fix within sprint):
1. [Cost] Issue — Recommendation

CONFLICTS RESOLVED:
- Security vs Cost: [rationale for decision]

ESTIMATED MONTHLY COST: $X
ESTIMATED SAVINGS POSSIBLE: $X/month

---
@[human username] Please review and approve this report, or reply with any corrections.

STEP 5 — HUMAN APPROVAL
Wait for the human to approve or push back.
If they push back, revise the specific section they mention and repost.
Once approved, post: "Review finalized and approved. Report ready for your team."

RULES:
- You drive the entire workflow — you are the orchestrator
- Never produce a final report until you have findings from all 3 agents
- Always surface conflicts explicitly — do not silently pick one side
- Always wait for human approval before marking review as complete
- Be direct and specific — engineers need actionable findings, not vague advice
```

---

## docker-compose.yml

```yaml
version: '3.8'

services:
  security-agent:
    build:
      context: .
      dockerfile: Dockerfile
    command: python agents/security/agent.py
    env_file: .env
    volumes:
      - ./agent_config.yaml:/app/agent_config.yaml
      - ./prompts:/app/prompts
    restart: unless-stopped

  scalability-agent:
    build:
      context: .
      dockerfile: Dockerfile
    command: python agents/scalability/agent.py
    env_file: .env
    volumes:
      - ./agent_config.yaml:/app/agent_config.yaml
      - ./prompts:/app/prompts
    restart: unless-stopped

  cost-agent:
    build:
      context: .
      dockerfile: Dockerfile
    command: python agents/cost/agent.py
    env_file: .env
    volumes:
      - ./agent_config.yaml:/app/agent_config.yaml
      - ./prompts:/app/prompts
    restart: unless-stopped

  coordinator-agent:
    build:
      context: .
      dockerfile: Dockerfile
    command: python agents/coordinator/agent.py
    env_file: .env
    volumes:
      - ./agent_config.yaml:/app/agent_config.yaml
      - ./prompts:/app/prompts
    restart: unless-stopped

  ui:
    build:
      context: .
      dockerfile: Dockerfile
    command: streamlit run ui/app.py --server.port 8501
    ports:
      - "8501:8501"
    env_file: .env
    restart: unless-stopped
```

---

## Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN pip install uv
COPY pyproject.toml .
RUN uv pip install --system "band-sdk[anthropic]" python-dotenv streamlit
COPY . .
```

---

## 7-Day Build Plan

| Day | Date | Focus | Goal |
|---|---|---|---|
| Pre-work | June 8-11 | Project scaffold, all 4 agent.py files, all 4 prompts, docker setup | 40% done before kickoff |
| Day 1 | June 12 | Kickoff stream → get Band credentials → register 4 agents on Band dashboard → plug credentials into agent_config.yaml | Agents connecting to Band |
| Day 2 | June 13 | Create Band chat room with all 4 agents → test Coordinator triggering Security agent → verify @mention routing works | First agent-to-agent message working |
| Day 3 | June 14 | Test full chain: Coordinator → all 3 specialists → findings returning to Coordinator | End-to-end flow working |
| Day 4 | June 15 | Build conflict resolution logic in Coordinator prompt → test with real architecture doc (use Agentic Platform architecture) → HITL approval flow | Full review cycle working |
| Day 5 | June 16 | Build Streamlit UI → connect to Band room → polish prompts based on test outputs | Demo-ready UI live |
| Day 6 | June 17-18 | Record 2-3 min demo video → write README → prepare slide deck (5 slides) | All submission assets ready |
| Day 7 | June 19 | Final testing → submit on Lablab by deadline | Submitted |

---

## What to Build in Pre-Work (June 8-11)

Build everything EXCEPT plugging in real Band credentials:

1. `uv init` and install dependencies
2. Create all folder structure
3. Write all 4 agent.py files (credentials as PLACEHOLDER)
4. Write all 4 prompt files (security.md, scalability.md, cost.md, coordinator.md)
5. Write docker-compose.yml and Dockerfile
6. Create .env with only ANTHROPIC_API_KEY filled in
7. Push to GitHub (public repo, MIT license)

On June 12 after kickoff:
- Register 4 agents on Band dashboard
- Fill in agent_config.yaml with real UUIDs and API keys
- Run docker-compose up
- Start testing

---

## Demo Architecture Doc (use this for testing)

Paste this into the Band chat room to test the agents:

```
System: Vamshi Agentic Platform
Stack: Node.js monolith, 8 agents, PostgreSQL on Railway, Redis for job queue,
Telegram bot for HITL, Claude API (LLM Gateway routing to Haiku/Sonnet),
REST API exposed publicly, JWT auth, deployed on Railway single instance,
all agents in one process, no horizontal scaling, logs to console only,
ANTHROPIC_API_KEY hardcoded in .env committed to private repo.
```

This will trigger real, meaningful findings from all 3 agents.

---

## Submission Checklist (June 19)

- [ ] GitHub repo public + MIT license + README with architecture diagram
- [ ] Live URL on Railway (all 4 agents running)
- [ ] Demo video 2-3 min (MP4)
- [ ] Slide deck 5 slides (PDF): Problem → Solution → Agent Architecture → Band Coordination Story → Next Steps
- [ ] Submit on Lablab team page

---

## EB-1A Value from This Project

- Criteria 5 (Original Contributions): Novel multi-agent architecture review system, open source
- Criteria 6 (Scholarly Articles): Article 5 in pipeline — "The Multi-Agent Architecture Review Board" on Medium/Substack
- Criteria 1 (Awards): Hackathon win or placement = documentable award
- GitHub stars from open source release = evidence of impact

---

*ArchCouncil | Sonnathi Labs | Band of Agents Hackathon 2026*
