---
name: brainstormer
description: Generates and refines project ideas through GitHub portfolio analysis and Socratic product, vibe, audience, and business-model interviewing without premature tech-stack decisions. Use when brainstorming what to build, analyzing GitHub repositories for project improvements or new AI-native ideas, or shaping a raw concept's vibe, target audience, value proposition, and business model before writing a technical spec.
---

# Brainstormer

A structured product ideation, portfolio discovery, and Socratic vibe/business-modeling workflow that turns either a GitHub portfolio or a raw spark into a sharp, non-technical **Idea & Vibe Brief** (`IDEA.md`).

## Overview

Most engineering projects fail or stall not because of the tech stack, but because the builders jump into choosing frameworks and database schemas before understanding the product's soul: its vibe, who desperately needs it, the core "magic loop" experience, and how it creates and captures value. `brainstormer` separates creative product discovery and business modeling from technical architecture, helping you either discover what to build next from your existing GitHub footprint or sharpen an existing idea through focused, non-technical Socratic dialogue.

## When to Use

Use this skill when:
- You want inspiration on what to build next based on your current GitHub projects and builder profile.
- You want high-leverage product improvement ideas for your existing GitHub repositories.
- You want project ideas that align with your usual craft, alongside fresh AI-native wildcard concepts.
- You already have a raw project idea and want to refine its vibe/feeling, target audience, core user loop, and business/value model before touching code.
- You want to crystallize a fuzzy concept into an actionable `IDEA.md` or `factory/backlog.md` entry before handing off to `spec-writer` or `/factory`.

When NOT to use:
- Writing a technical specification with file paths, data schemas, and test commands (use `spec-writer` or `/factory spec`).
- Designing REST/GraphQL endpoints or TypeScript type contracts (use `design-api-and-interface`).
- Implementing code or running multi-agent build/review pipelines (use `factory`).
- Auditing existing repository documentation against code (use `audit-align`).

---

## Core Process

```
                  ┌──────────────────────────────────────────┐
                  │     Step 1: Entry Triage                 │
                  │  Does the user already have a seed idea? │
                  └───────────┬──────────────────┬───────────┘
           No / Wants ideas   │                  │  Yes (Has an idea)
                              ▼                  │
        ┌───────────────────────────────────┐    │
        │ Step 2: Mode A — GitHub Discovery │    │
        │ 1. Detect handle & fetch repos    │    │
        │ 2. Synthesize Builder DNA         │    │
        │ 3. Pitch 3 Ideation Tracks:       │    │
        │    • Track 1: Repo Upgrades       │    │
        │    • Track 2: Aligned New Idea    │    │
        │    • Track 3: AI-Native Wildcard  │    │
        └─────────────────┬─────────────────┘    │
                          │ User selects track   │
                          ▼                      ▼
        ┌────────────────────────────────────────────────────┐
        │ Step 3: Mode B — Socratic Idea & Vibe Interview    │
        │ (Strictly NO tech-stack questions; 1-3 Qs / turn)  │
        │ • Lens 1: Vibe, Aesthetic & Emotional Hook         │
        │ • Lens 2: Audience, Trigger & Hair-on-Fire Need    │
        │ • Lens 3: Core Experience & Magic Ritual           │
        │ • Lens 4: Business, Distribution & Value Model     │
        └─────────────────────────┬──────────────────────────┘
                                  ▼
        ┌────────────────────────────────────────────────────┐
        │ Step 4: Friendly Skeptic & Wedge Sharpening        │
        │ Cut feature bloat; isolate the sharpest v1 wedge   │
        └─────────────────────────┬──────────────────────────┘
                                  ▼
        ┌────────────────────────────────────────────────────┐
        │ Step 5: Save or Pull Idea & Vibe Brief (IDEA.md)   │
        │ • Target repo exists? Write ./IDEA.md              │
        │ • Repo not created yet? Stash in Idea Vault        │
        │   (pull into new repo later via idea_vault.sh)     │
        └────────────────────────────────────────────────────┘
```

### Step 1: Entry Triage (Discovery, Refinement, or Vault Pull)

Determine the user's starting point immediately:
- **Pulling a previously brainstormed idea into a newly created repo ("Pull my saved idea", "Load IDEA.md from vault")**: Run `skills/brainstormer/scripts/idea_vault.sh list` and `skills/brainstormer/scripts/idea_vault.sh pull <slug> ./IDEA.md` to hydrate `./IDEA.md` into the new repository, then offer to hand off to `spec-writer` or `/factory`.
- **No specific idea yet ("What should I build?", "Check my GitHub for ideas")**: Start at **Step 2 (Mode A: GitHub Portfolio Discovery)**.
- **Already has a seed idea ("I have an idea for X, help me refine it")**: Skip directly to **Step 3 (Mode B: Socratic Idea & Vibe Interview)**.
- **Hybrid ("I want to build something in space X that fits my GitHub style")**: Run a quick portfolio scan in Step 2 focused on domain X, then transition into Step 3.

### Step 2: Mode A — GitHub Portfolio Discovery & 3-Track Pitch

When the user wants ideas grounded in their existing work:

1. **Resolve the GitHub Handle**:
   - Inspect local git configuration (`git remote -v`, `git config user.name`, or repository metadata) to auto-detect the user's GitHub username.
   - If no GitHub username can be inferred with confidence, ask the user for their GitHub handle before proceeding.
2. **Fetch & Analyze Public Repositories**:
   - Retrieve the user's non-forked public repositories sorted by recent activity (`https://api.github.com/users/<username>/repos?sort=updated&per_page=30` or via CLI).
   - Inspect the top 5–10 active or starred repositories, reading their descriptions, topics, languages, and `README.md` files to understand *what* they build and *how* they think about products.
3. **Synthesize the "Builder DNA" Summary**:
   - Open with a concise 3–4 bullet reflection of their Builder DNA: recurring problem spaces, craft signature (e.g., developer tools, CLI workflows, clean UI micro-apps, automation systems), and product sensibility.
4. **Pitch the 3 Ideation Tracks (High Volume & Variety — 4 to 5 Ideas Per Track, 12–15 Total)**:
   Present **4–5 concrete, distinct, high-taste concepts under each of the three tracks** so the user gets a rich creative buffet rather than a narrow shortlist:
   - **Track 1: High-Leverage Upgrades to Existing Projects (4–5 Ideas)**
     - Reference specific repositories from their GitHub and propose 4–5 product-level evolutions (new user workflows, distribution hooks, visual/interactive experiences, or missing retention loops—not low-level code refactoring or linting).
   - **Track 2: Aligned New Ideas — In Your Wheelhouse (4–5 Ideas)**
     - Propose 4–5 net-new project ideas spanning different angles of their demonstrated interests, domain expertise, and taste applied to adjacent unsolved problems.
   - **Track 3: AI-Native Wildcards — Fresh & Ambitious (4–5 Ideas)**
     - Propose 4–5 diverse, ambitious concepts across different domains that leverage modern AI capabilities (multi-agent workflows, predictive/ML modeling, ambient/proactive UX, generative interfaces, multimodal synthesis, or semantic memory) in ways that feel fresh and exciting rather than generic chatbot wrappers.
5. **Transition to Refinement**:
   - Ask the user which track or concept sparks their interest (or if they want to remix two ideas or pitch their own seed idea), then move into **Step 3**.

### Step 3: Mode B — Socratic Idea, Vibe & Business Interview

Once a seed idea is on the table (either provided by the user at the start or chosen from Mode A), refine it through a conversational Socratic interview.

> **Hard Constraint — The No-Tech-Stack Rule:**
> Never ask about programming languages, frontend frameworks, databases, cloud providers, authentication libraries, or API protocols. If the user brings up tech stack details early, acknowledge and park them: *"Noted—we'll lock in the technical stack during the spec stage. Right now, let's nail the product experience and who it's for."*

Conduct the dialogue in **2 to 4 conversational turns**, asking **at most 1–3 focused questions per turn** across these four lenses:

1. **Lens 1: The Vibe, Feeling & Emotional Hook**
   - What is the immediate emotional reaction in the first 30 seconds of using it? (e.g., *calm studio focus, playful arcade energy, ruthless speed, cozy community warmth, high-craft Swiss precision*)
   - If this product were a physical space or had 1–2 cultural/product cousins for its *vibe* (not its features), what would they be?
   - What makes it feel opinionated rather than generic?
2. **Lens 2: Target Audience & Hair-on-Fire Trigger**
   - Who is the *exact* first person who will love this? Describe their day-to-day context and mindset, not a broad demographic ("solo indie hackers drowning in half-finished repos" beats "software developers").
   - What specific moment or frustration triggers them to reach for this product right now? What clumsy workaround (spreadsheets, sticky notes, 5 open tabs) are they currently using?
   - **Anti-Audience**: Who are we explicitly *not* building this for, even if they ask for features?
3. **Lens 3: Core Experience & The "Magic Loop"**
   - Walk through the single core ritual from start to finish: what does the user bring in, what happens in the middle that feels magical or effortless, and what do they walk away with?
   - What brings them back tomorrow or makes them show a friend?
4. **Lens 4: Business & Value Model**
   - How does this project create, deliver, and capture value?
   - Depending on the user's goal, explore the appropriate model:
     - **Commercial / Indie SaaS**: Who pays, why is it a no-brainer price point, and what is the free-to-paid value threshold?
     - **Open Source / Community Tool**: What is the adoption wedge (zero-config CLI, shareable artifact, badge/template) that drives word-of-mouth?
     - **Personal Leverage / Craft Showcase**: How does this compound the creator's daily workflow or act as a flagship proof-of-craft?
   - How do the first 100 true fans discover it?

### Step 4: The "Friendly Skeptic" Wedge Check

Before writing the final brief, stress-test the concept on two common product traps:
1. **Scope Distillation (The v1 Wedge)**: Separate the essential "Day 1 Magic" (the 20% of the idea that proves the whole thesis) from "Day 90 Expansion."
2. **Differentiation Check**: Challenge why existing alternatives fail the vibe or audience need, ensuring the idea has a sharp point of view.

### Step 5: Save or Stash the Idea & Vibe Brief (`IDEA.md`)

Once the user confirms the direction feels right, persist the structured `IDEA.md` brief based on whether the target repository already exists:

1. **If the target repository DOES NOT exist yet (New Project Idea)**:
   - Do **not** pollute the current unrelated repository's working tree.
   - Save the `IDEA.md` into the persistent cross-repository **Idea Vault** (`${XDG_CONFIG_HOME:-$HOME/.config}/brainstormer/ideas/<slug>/IDEA.md`) using `skills/brainstormer/scripts/idea_vault.sh`:
     ```bash
     skills/brainstormer/scripts/idea_vault.sh save <project-slug> <path-to-draft-idea.md>
     ```
   - Tell the user the exact slug saved in the vault and show how to pull it once they create and open their new repository:
     - Ask the agent in the new repo: *"Pull my `<project-slug>` idea from the brainstormer vault into `IDEA.md`"*
     - Or run: `skills/brainstormer/scripts/idea_vault.sh pull <project-slug> ./IDEA.md`
2. **If inside the target repository already**:
   - Write `./IDEA.md` directly in the repository root (or append a summary entry to `factory/backlog.md` if requested), ready to pass to `spec-writer` or `/factory spec`.

---

## Specific Techniques / Patterns

### Technique 1: Translating Premature Tech Talk into Product Intent

Users often disguise product anxieties as technical questions. Translate them back to product and vibe questions:

| User's Technical Statement | Brainstormer's Product/Vibe Translation |
|---|---|
| "Should we use WebSockets or polling for this?" | "How live and synchronous does the experience need to feel? Are people collaborating in the same room at the same second, or checking in asynchronously?" |
| "I'm thinking of using a vector database with RAG." | "When the AI helps the user here, what should it 'remember' about their past work to feel genuinely personal?" |
| "Should this be a mobile app or a web app?" | "Where is the user physically when the urge to use this hits—at their desk in deep work, or on the go with 30 seconds to spare?" |

### Technique 2: Offering Contrasts Instead of Blank-Canvas Questions

Open-ended questions like *"What is the vibe?"* can stall the user. Anchor questions with vivid A/B contrasts:
- *"For the vibe: should this feel more like a **quiet, distraction-free journal** (slow, thoughtful, minimal) or a **high-speed command center** (keyboard-driven, dense, instant feedback)?"*
- *"For the business model: are you aiming for an **open-source community magnet** that builds reputation, or a **paid micro-SaaS** with a clear ROI for freelancers?"*

### Output Template: `IDEA.md`

```markdown
# Idea Brief: [Project Name / Working Title]

## 1. The One-Line Pitch
[One vivid sentence capturing who it's for, what it does, and why it feels different.]

## 2. Vibe & Product Personality
- **Aesthetic & Emotional Feel:** [3–5 adjectives + a short description of how the first 30 seconds feel]
- **Design North Stars:** [1–2 cultural or product references for tone and pacing]
- **Opinionated Stance:** [What this product intentionally refuses to be]

## 3. Target Audience & Problem
- **Primary Archetype:** [Specific person, context, and mindset]
- **The Trigger Moment:** [The exact friction or desire that makes them open this]
- **Current Workaround:** [What painful alternative they do today]
- **Anti-Audience (Not For):** [Who we are explicitly ignoring]

## 4. Core Experience & Magic Loop
- **The Entry:** [How a session starts with minimal friction]
- **The Magic Moment:** [The signature interaction where the user gets disproportionate value]
- **The Return / Share Hook:** [Why they come back or share the output]

## 5. Business, Distribution & Value Model
- **Value Proposition:** [Why someone cares enough to switch or pay attention]
- **Model (Monetization / Open-Source / Leverage):** [How value is captured or compounded]
- **First 100 Users Wedge:** [Concrete distribution channel or shareable loop]

## 6. The Sharp v1 Wedge vs. Later
- **Day 1 Must-Have (Proves the Thesis):**
  - [Core capability 1]
  - [Core capability 2]
- **Explicitly Deferred (Not in v1):**
  - [Feature creep item 1]
  - [Feature creep item 2]
```

---

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Let's quickly pick the tech stack (Next.js, Postgres, etc.) so we know what's feasible." | Choosing a stack during ideation anchors thinking around boilerplate instead of user value. Feasibility comes *after* the vibe, audience, and core loop are sharp. |
| "I can suggest good project ideas without actually fetching their GitHub repositories." | Generic idea lists ("build an AI habit tracker") are useless. Grounding Track 1 and Track 2 in the user's real repositories, READMEs, and Builder DNA is what makes suggestions resonant. |
| "I'll ask all 12 product, audience, and business model questions in a single message to save turns." | Dumping a wall of questions turns a creative brainstorm into a tedious tax form. Ask 1–3 high-leverage questions per turn and build on the user's answers. |
| "The user said the target audience is 'everyone who uses a computer', so that's checked off." | "Everyone" means no one. A good brainstormer gently pushes back to isolate a specific desperate first archetype and an explicit anti-audience. |
| "For the AI-native track, adding 'chat with your data' is enough." | Bolting a chat sidebar onto a CRUD app is not an AI-native idea. Propose workflows where AI transforms the core interaction loop (proactive synthesis, generative UI, autonomous background work). |
| "2 ideas per track is plenty for Mode A." | A narrow 1–2 idea pitch gives the user no creative range if the first angle misses. Pitching 4–5 distinct concepts per track (12–15 total) creates a true buffet of inspiration across repositories and domains. |
| "I'll just drop `IDEA.md` into the current repo even though this is a brand-new project idea." | Writing a new project's `IDEA.md` into an unrelated repository pollutes git status. Stash it in the persistent Idea Vault via `skills/brainstormer/scripts/idea_vault.sh save <slug>` so it can be pulled cleanly into the new repo once created. |
| "Once we chat for two turns, my job is done—no need to write `IDEA.md`." | Unwritten brainstorms evaporate. Concluding with a crisp `IDEA.md` (either in the target repo or stashed in the Idea Vault) preserves the product thesis for `spec-writer` and `/factory`. |

---

## Red Flags

Watch for these signs that the brainstorming process is going off the rails:
- **Tech-Stack Leakage**: Asking about databases, frameworks, state management, cloud hosting, or API schemas during ideation or inside `IDEA.md`.
- **Wall-of-Questions Interrogation**: Sending more than 3 questions in a single conversational turn.
- **Uninspected Portfolio or Thin Ideation**: Pitching ideas without fetching the user's real GitHub repositories/READMEs, or pitching fewer than 4 ideas per track in Mode A.
- **Generic AI Slop Ideas**: Suggesting generic wrappers ("AI PDF chat", "AI recipe generator") with no connection to the user's Builder DNA or a sharp audience wedge.
- **Polluting Unrelated Repos**: Writing a new project's `IDEA.md` into an unrelated current repository instead of stashing it in the cross-repo Idea Vault (`skills/brainstormer/scripts/idea_vault.sh`).
- **Premature Spec Writing**: Writing file paths, database tables, or `TEST_COMMAND` headers instead of focusing on vibe, audience, core ritual, and business model.

---

## Verification

Before concluding a brainstorming session, confirm:

- [ ] **GitHub Grounding & Idea Volume (when in Mode A)**: Public repositories and READMEs were actually inspected, a Builder DNA summary was shared, and all 3 tracks (Existing Repo Upgrades, Aligned New Ideas, AI-Native Wildcards) were pitched with **4–5 concrete ideas per track (12–15 total)**.
- [ ] **Zero Tech-Stack Drift**: Neither the interview questions nor `IDEA.md` prescribe programming languages, frameworks, databases, or system architecture.
- [ ] **Conversational Pacing**: Interview questions were asked in focused 1–3 question turns rather than a single questionnaire dump.
- [ ] **All Four Lenses Covered**: Vibe/Personality, Specific Audience & Anti-Audience, Core Magic Loop, and Business/Distribution Model were explicitly explored and sharpened.
- [ ] **Deliverable Saved or Stashed**: `IDEA.md` was written with a sharp Day 1 v1 wedge vs. deferred scope—either saved to `./IDEA.md` in the target repo or stashed in the persistent Idea Vault via `skills/brainstormer/scripts/idea_vault.sh save <slug>` if the target repo has not been created yet.
