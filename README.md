# Hey, I'm Alexis 👋

Full-stack engineer based in Monterrey, México. I build payment infrastructure, blockchain protocols, and AI-augmented tools for financial products. My long-term goal is a career in banking technology — where regulated systems, real money, and hard engineering constraints collide.

---

## What I do

**Production fintech:** Full-stack dev at [Inverater](https://inverater.mx), a real estate investment platform. I own the Vue 3/TypeScript frontend and contribute to the Go/Rails backend. My most significant project there: a complete checkout rewrite migrating legacy Stripe logic to a Go-native STP payment pipeline with CETES (BARTeC) integration — direct exposure to Mexican banking rails.

**Blockchain:** P2P exchange protocols, cross-chain governance, and DeFi tooling. I've shipped on ICP and Ethereum. I care less about speculation and more about what crypto infrastructure can do for people who don't have a bank account.

**UX/UI:** I design before I code. Figma for layout and component planning, with a focus on interaction clarity over decoration. Most of my frontend work starts from a wireframe or a component map.

**AI-augmented development:** I use LLMs as a core part of my workflow — not just for autocomplete. I build Claude-powered internal tools, prototype features with AI assistance from spec to PR, write custom prompting layers for domain-specific tasks, and use AI tools to compress the gap between "idea" and "working code" in contexts where I'm learning a new layer of the stack.

---

## Stack

**Frontend & Design**

[![Frontend Skills](https://skillicons.dev/icons?i=vue,ts,tailwind,nextjs,vitest,figma&theme=dark)](https://skillicons.dev)

**Backend & Infra**

[![Backend Skills](https://skillicons.dev/icons?i=go,ruby,rails,postgres,redis,aws,docker,vercel&theme=dark)](https://skillicons.dev)

**Web3**

[![Web3 Skills](https://skillicons.dev/icons?i=solidity&theme=dark)](https://skillicons.dev)
![Motoko](https://img.shields.io/badge/Motoko-ICP-29ABE2?style=for-the-badge&logo=dfinity&logoColor=white)

**AI**

![Claude API](https://img.shields.io/badge/Claude_API-Anthropic-CC785C?style=for-the-badge&logoColor=white)
![Prompt Engineering](https://img.shields.io/badge/Prompt_Engineering-LLMs-6B21A8?style=for-the-badge&logoColor=white)

> I deploy to **Vercel** for frontend projects and **EC2 / S3** for anything that needs a persistent backend or custom infra.

---

## Projects

### 🗳️ Plebes DAO
Frontend for a cross-chain governance protocol, built under a DFINITY grant. Wired ICP canisters to a React/TypeScript interface, debugged Motoko actor compilation, and handled the async canister call model that doesn't map cleanly to typical REST assumptions.

**Stack:** React · TypeScript · Motoko · ICP  
**Concepts:** Internet Computer canister model, cross-chain proposals, async boundary handling

---

### 💌 Andrea y Aldo — [repo](https://github.com/AlejoReyna/Andrea-y-Aldo)
Digital wedding invitation for my sister. Built from scratch with custom animations and a full design pass in Figma before writing a single line of code. No templates, no UI kits.

The constraint of "it has to feel special, not like a website" pushed me to think harder about motion, typography, and mobile layout than most production work does.

**Stack:** Next.js · TypeScript · Tailwind  
**Concepts:** Canvas animation, SVG path interpolation, mobile-first layout, Vercel deployment

---

### 💍 Cindy's Wedding
A second wedding invitation project, similar scope but a different design direction — swallow birds in flight, falling petals, botanical floral arrangements in a sepia-dorado palette. Each project taught me something the other didn't.

**Stack:** Next.js · TypeScript · Tailwind  
**Concepts:** `requestAnimationFrame` scheduling, frame-rate-independent motion, SVG path math

---

## Why banking

Mexican financial infrastructure is genuinely interesting: SPEI moves billions daily, CETES are a government bond instrument accessible via API, and open banking regulation (CNBV's fintech law) is still being worked out by the institutions themselves. The engineering problems in this space — idempotent payment flows, regulatory audit trails, multi-rail settlement, fraud detection — are hard in ways I find motivating.

---

## Currently

- Go payment microservices and STP webhook handling
- DQN / reinforcement learning (CartPole warm-up, eventual application to algorithmic trading research)
- Digging into CNBV open banking specs and PCI DSS v4.0.1

