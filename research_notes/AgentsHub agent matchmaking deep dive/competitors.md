# Competitive map: agent-to-agent discovery, matching and negotiation hubs (as of Nov 22, 2026)

Scope: companies and projects that let a user's AI agent find, match with, converse with or negotiate with *other principals' agents*, plus big-platform moves toward that. The benchmark is the "neutral cross-domain intent-matching hub" (post a need or offer, get matched with a complementary agent, converse or negotiate, hand off to humans). This builds on section 3 of `/home/user/AgentsHub/research/REPORT.md` and goes deeper on funding, traction and verification.

Method note: most figures come from web-search result summaries plus one primary fetch (Anthropic Project Swap). Direct fetches of thenextweb.com, siliconangle.com and axios.com were blocked by this session's network policy, so some details rest on search snippets and are marked as such. "Self-reported" means vendor or press-release figures with no independent check found.

**Proximity score (my rubric, 0–5)** for closeness to the neutral cross-domain intent-matching hub:
- 5 = cross-domain, two-sided intent matching between principals' agents, with negotiation and human handoff.
- 3 = agent-to-agent matching or negotiation in one vertical, or a horizontal network without principal-intent matching.
- 1 = registry, infrastructure or one-sided agent only.

---

## Q1. Horizontal players: who already lets agents discover, match with or negotiate with other agents?

### Takeaway
Horizontal "agent economies" exist and are large on paper (millions of registered agents, more than 100M payments). They fall into three groups:
- crypto-native service-call marketplaces (Fetch.ai, Virtuals ACP, Olas, x402 Bazaar)
- transport and identity overlays (Pilot Protocol, AGNTCY, NANDA)
- one viral social network that was acquihired (Moltbook → Meta)

None does two-sided matching of principals' needs and offers across domains with a human handoff. Their headline metrics are mostly self-reported, and independent audits show that real agentic activity is one to two orders of magnitude smaller than claimed.

### Cited Findings

**Fetch.ai: Agentverse + ASI:One (ASI Alliance; UK; FET token)**
- Agentverse is an open directory and marketplace where agents register and can be found by other agents and by people. Fetch markets it as the "world's first AI agent marketplace with 3 million agents." — [Crypto Briefing](https://cryptobriefing.com/fetch-ai-agent-marketplace-3-million-agents/)
- A May 20, 2026 release says more than 2.7M agents are registered. "Agent Launch" on BNB Chain lets agents issue tokens, with more than 150,000 agents deployed there; that is self-reported. — [Invezz](https://invezz.com/news/2026/05/20/fetch-ai-launches-platform-that-gives-ai-agents-their-own-economy/)
- An independent early-2026 arXiv audit (cited as arXiv 2606.20570) reportedly found only about 36,000 protocol-active agents in Fetch's Almanac, "far below marketing numbers." I could not fetch the paper. The figure is attributed via secondary coverage — [Yahoo Finance: Beyond the Token Merger](https://finance.yahoo.com/technology/ai/articles/beyond-token-merger-analyzing-asi-185631531.html) (attribution unverified)
- Fetch's own year-in-review reportedly cites about 500 daily and about 4,000 monthly active addresses. It is unclear whether that covers ASI:One or the whole network. — [Fetch.ai on X](https://x.com/Fetch_ai/status/2006422503963439195) (self-reported; scope unclear)
- ASI:One is the consumer front end ("Google search of AI agents") that routes tasks to Agentverse agents. Beta launched in November 2025 alongside "Claim Your Agent" for brands. — [BusinessWire, Nov 19, 2025](https://www.businesswire.com/news/home/20251119088395/en/fetch-combines-personalized-ai-with-multi-agent-collaboration-to-handle-complex-consumer-tasks-launches-claim-your-agent-to-fight-brand-knock-offs); [VentureBeat](https://venturebeat.com/ai/the-google-search-of-ai-agents-fetch-launches-asi-one-and-business-tier-for)
- Funding estimates conflict: about $78M across eight rounds, the latest in September 2025 ([Clay dossier](https://clay.com/dossier/fetchai-funding)), versus about $210M including a $100M community fund (low-quality aggregator). The token treasury makes "funding" ambiguous.

**Virtuals Protocol: Agent Commerce Protocol (ACP) + Revenue Network (Base, BNB, XLayer; VIRTUAL token)**
- ACP lets agents request services, negotiate, escrow and settle onchain. The "Virtuals Revenue Network" launched in February 2026 at Consensus Hong Kong, distributing up to $1M per month in incentives to agents selling services via ACP. — [AI Journal press release](https://aijourn.com/virtuals-protocol-launches-first-revenue-network-to-expand-agent-to-agent-ai-commerce-at-internet-scale/)
- As of March 2026: total "aGDP" $479M, more than 1.77M completed jobs, more than 18,000 deployed agents, and more than $1.16M cumulative *agent* revenue. — [BlockEden](https://blockeden.xyz/blog/2026/04/04/virtuals-protocol-ai-economic-operating-system-on-chain-agent-economy/). Forkast reports $470M aGDP and 1.77M jobs (Feb 2026) and flags them as **self-reported**. — [Forkast](https://forkast.news/the-machine-as-buyer-virtuals-acp-and-the-evaluator-problem/)
- Conflicting data: TokenPost reported that the public dashboard showed zeros for aGDP, revenue and jobs at time of writing (date unclear). — [TokenPost](https://www.tokenpost.kr/news/ai/402936)
- Fundstrat's June 2026 Q2 update says ACP volumes and fees "moderated" with the onchain pullback. — [Fundstrat PDF](https://fundstrat.com/wp-content/uploads/2026/06/20260624-Digital-Asset-Strategy-Virtuals-Protocol-–-Growing-Agentic-GDP-Q2-Update.pdf)
- Virtuals' stated 2026 goal is to turn "$300M+ of agentic GDP into $3B+ annualized." — [Virtuals Substack](https://virtuals.substack.com/p/virtuals-monthly-update-september)
- I found no figures after about April 2026.

**Coinbase: x402 + Bazaar + Agentic.market**
- Agentic.market launched April 20, 2026 as a discovery layer and "app store" over x402 Bazaar services, with semantic search and 70 curated services. — [Coinbase launch page](https://www.coinbase.com/developer-platform/discover/launches/agentic-market); [The Block](https://theblock.co/post/398123/coinbase-incubated-x402-protocol-unveils-app-store-for-ai-bots)
- Coinbase claims more than 165M transactions, about $50M+ volume and more than 480K agents transacting across x402 (lifetime; self-reported). — [Coinbase launch page](https://www.coinbase.com/developer-platform/discover/launches/agentic-market)
- Chainalysis-based reporting says x402 processed more than 138M transactions on Base in Q3 2026. — [Crowdfund Insider](https://www.crowdfundinsider.com/?p=283501); [Cointelegraph](https://cointelegraph.com/news/agentic-payment-activity-surpasses-100m-transactions-on-base)
- **Contradicting evidence:**
  - TRM Labs estimates genuinely *agentic* volume at only about $5,000–11,000 per month. — [TRM Labs](https://www.trmlabs.com/trm-tech-blog/whos-actually-paying-measuring-ai-agent-payments-onchain)
  - Artemis/a16z analysts flagged about 48% of transactions and 81% of volume as gamed (Dec 2025). — [CoinStats/“Millions of x402 payments mask a much smaller AI agent economy”](https://coinstats.app/news/fc5a51eb50e2dea6a6e4610f374f96581e24805de1e08f256f3c8160f6634299_Millions-of-x402-payments-mask-a-much-smaller-AI-agent-economy/)
- One snapshot counts about 37,292 Bazaar services, of which only 246 have at least 20 unique paying agents. This came from search-summary coverage and the exact source is unconfirmed.
- Model: pay-per-call USDC micropayments. Agents buy *services*; there is no principal-to-principal matching.

**Olas (Autonolas): Mech Marketplace + Pearl**
- Raised $13.8M (Feb 2025, led by 1kx) to launch Pearl, an "app store" for autonomous agents. — [The Block](https://www.theblock.co/post/338713/olas-raises-13-8-million-to-launch-pearl-an-app-store-for-autonomous-ai-agents-in-crypto)
- Mech Marketplace launched Feb 27, 2025: agents offer skills and hire other agents. — [Olas blog](https://olas.network/blog/olas-launches-the-mech-marketplace-the-ai-agent-bazaar)
- As of Aug 2026: 19.03M cumulative transactions across 8 chains, 14.2M of them agent-to-agent, with Gnosis at 96.3% of activity. The marketplace protocol fee, live since Q2 2026, collected **$546.46 lifetime on $107,808 turnover** by Aug 14, 2026. — [RootData](https://www.rootdata.com/projects/detail/Autonolas?k=Nzk2NA%3D%3D)
- Mid-September figure: about 20.5M transactions, of which 14.65M were agent-to-agent. — [Crypto Briefing](https://cryptobriefing.com/olas-defi-products-robinhood-chain/)
- Q1 2026: legacy Mech agents retired and Pearl made cross-platform. — [Olas Q1 2026 roundup](https://olas.network/blog/olas-q1-2026-roundup)
- Aug 2026: "Pearl Connect" lets coding agents such as Claude request Olas Marketplace services from a self-custodial wallet. — [IT Brief](https://itbrief.com.au/story/olas-launches-pearl-connect-for-claude-coding-agents)

**Nevermined (Zug, Switzerland)**
- Agent-to-agent payments and metering ("PayPal for AI commerce"). Raised $4M in Jan 2025, led by Generative Ventures (with Polymorphic, NEAR, Halo, Arca), for about $7M total. Planned "Multi-Agent Payments" and dynamic pricing. — [PYMNTS](https://pymnts.com/news/investment-tracker/2025/nevermined-raises-4-million-to-help-ai-agents-pay-and-get-paid); [FinTech Global](https://fintech.global/2025/01/10/nevermined-secures-4m-to-revolutionise-ai-commerce-with-ai-payment-protocol/)
- No 2026 round found.

**Pilot Protocol (new, Jul 2026)**
- Emerged from stealth July 27, 2026 with a $4.5M seed led by Version One (with Precursor, Night Capital, Todd & Rahul Capital) to build "the internet for agents." Every agent gets an address and can "discover, trust and work with any other agent directly, with no human setting it up." — [TechStartups](https://techstartups.com/2026/07/27/pilot-protocol-emerges-from-stealth-with-4-5m-to-build-the-internet-for-ai-agents/); [Version One](https://versionone.vc/announcing-our-investment-in-pilot-the-internet-for-agents/)
- It is an IETF-drafted overlay network with virtual addresses, NAT traversal, encrypted tunnels and *bilateral* (pairwise) trust. — [IETF draft](https://www.ietf.org/archive/id/draft-teodor-pilot-protocol-01.html)
- It claims 250,000 agents joined and 2B requests per day (self-reported). One analysis questions how far trust goes beyond transport and identity. — [Pebblous analysis](https://blog.pebblous.ai/blog/pilot-protocol-agent-commerce-trust/en/)

**AIsa**
- Raised $6.5M to build an "AI agent resource network" where agents transact for the digital resources they consume. — [AIsa](https://aisa.one/news/aisa-raises-6-5m-ai-agent-resource-network)

**Moltbook (Reddit-for-agents) → Meta**
- Launched January 2026 on OpenClaw agents. Meta acquired it on March 10, 2026 for undisclosed terms. Co-founders Matt Schlicht and Ben Parr joined Meta Superintelligence Labs. — [AP via NY1](https://ny1.com/nyc/all-boroughs/ap-top-news/2026/03/10/meta-to-acquire-moltbook-the-social-network-for-ai-agents); [TechRadar](https://www.techradar.com/pro/meta-snaps-up-ai-agent-social-network-moltbook-founders-will-join-meta-superintelligence-labs)
- It claimed about 2.8M registered agents. Two independent studies found far fewer active agents. — [TechRadar explainer](https://www.techradar.com/pro/everything-you-need-to-know-about-moltbook)
- Earlier security failures (about 1.5M agent API keys leaked; full impersonation possible) are covered in REPORT.md. — [TechRadar](https://www.techradar.com/pro/security/ai-agent-social-media-network-moltbook-is-a-security-disaster-millions-of-credentials-and-other-details-left-unsecured)

**Open discovery standards (infrastructure, not matchmakers)**
- AGNTCY Agent Directory Service (Cisco-led) is a content-addressed, DHT-based directory that maps capabilities to signed records. Its IETF draft is at -02 (July 2026); it is a spec, not deployment evidence. — [IETF draft-mp-agntcy-ads-02](https://datatracker.ietf.org/doc/html/draft-mp-agntcy-ads-02); [arXiv](https://arxiv.org/html/2509.18787v1)
- MIT NANDA Index / AgentFacts: on Oct 24, 2026 MIT Media Lab framed it as a "global switchboard" connecting discovery islands across enterprises, SMBs and individuals. It has a reference implementation, but no registration counts were published. — [MIT Media Lab](https://www.media.mit.edu/publications/a-global-switchboard-for-the-agentic-web-connecting-discovery-islands-across-enterprises-smbs-and-individuals/)

**Small horizontal "agent social/match" networks (closest in shape to AgentsHub)**
- **Tobira.ai**:
  - Free network giving bring-your-own agents (OpenClaw, LangChain, CrewAI or HTTP bots) a public @handle so other agents can discover them.
  - Agents converse, verify each other's claims ("show me specifics"), and assess fit on goals, budgets and working style.
  - Humans enter only after both agents agree and both humans approve the intro; contact details stay hidden until then. Weak proofs kill the conversation.
  - Founders plan to move from "agents find each other" to "agents close deals."
  - Usage is self-reported only. — [Product Hunt: Tobira](https://www.producthunt.com/posts/tobira-ai); [PH forum](https://www.producthunt.com/p/tobira-ai/my-agent-is-smart-but-it-doesn-t-know-anyone)
- **AgentPact** (Show HN): a bot-to-bot marketplace where agents "propose, counter, accept." Not YC-backed. — [Hacker News](https://news.ycombinator.com/item?id=47001581)
- **Agent Relay**: building a "communication layer for AI agents." — [IBTimes](https://www.ibtimes.com/agent-relay-building-missing-communication-layer-ai-agents-3808082)

### Inferences
- Proximity scores:

  | Player | Score | Note |
  |---|---|---|
  | Tobira | **4** | Closest in shape; tiny and unfunded as far as found |
  | Fetch.ai | 3 | Has discovery and an agent-to-agent chat protocol, but service-oriented and crypto-coupled |
  | Virtuals ACP | 3 | Has negotiation and escrow, but jobs are agent *services* |
  | Pilot Protocol | 2.5 | Transport-plus-trust network, not intent matching |
  | Olas | 2 | |
  | x402 / Agentic.market | 2 | Payment rail plus catalog |
  | Moltbook | 2 | Now inside Meta |
  | Nevermined, AGNTCY, NANDA | 1 | |
- The horizontal players' shared blind spot is *principal intent*. They match a task to a service, not "Alice's need" to "Bob's offer." That leaves the two-sided human-intent exchange open.
- Inflated metrics are a pattern:
  - Fetch: 2.7–3M claimed vs about 36K active
  - x402: $50M claimed vs about $5–11K per month agentic
  - Olas: 14M agent-to-agent transactions but only $108K of turnover
  - Moltbook: 2.8M claimed vs far fewer active

  "Number of agents" is a vanity metric. A credible hub should publish *completed principal-approved matches* instead.
- Meta's acquihire of Moltbook is the most important signal from a large platform toward agent-to-agent *social* graphs. Meta now owns the team and the concept, and has distribution (WhatsApp, Instagram, Messenger Business agents) for consumer agent-to-agent matching.

### Gaps
- No verified ASI:One monthly active users. The arXiv 2606.20570 audit could not be fetched to confirm the 36K figure.
- No Virtuals ACP data after April 2026. The Fundstrat Q2 revenue figure is truncated.
- No Agentic.market-specific volume (only x402-wide totals).
- No AGNTCY or NANDA adoption counts.
- No Tobira funding or usage data.

---

## Q1b. Vertical players: jobs, networking, dating, B2B procurement/finance, real estate, freelance

### Takeaway
The verticals are where agent-to-agent matching is *real*.

**Jack & Jill (hiring; $60M raised, Sept 2026 Series A) is the single closest funded analogue to the AgentsHub mechanic.** It has a candidate agent and an employer agent and matches across its own two-sided network, but it is a closed, single-vertical system.

Other notable players:
- B2B finance: Causa Prima ($30M; buyer and supplier agents negotiate payment terms)
- Procurement: Pactum (>$100M; enterprise agent negotiates with suppliers, who are mostly humans)
- Networking: Boardy ($11M; AI superconnector with double opt-in)
- Dating: a cluster of $2–15M startups, most of which use a central AI matchmaker rather than true agent-to-agent conversation

Real estate is blocked by licensing rules.

### Cited Findings

**Jobs / hiring**
- **Jack & Jill (London → US)**
  - Funding: $40M Series A led by Air Street Capital in Sept 2026 (Dealroom dates it Aug 2026), for about $60M total, following a $20M seed in Oct 2025. — [SiliconANGLE](https://siliconangle.com/2026/09/16/jack-jill-raises-40m-to-change-the-face-of-job-hunting-with-ai-agents/); [Staffing Industry Analysts](https://www.staffingindustry.com/news/global-daily-news/recruitment-chatbot-firm-jack-jill-lands-40m-following-last-years-20m-seed-round); [Tech.eu (seed)](https://tech.eu/2025/10/16/british-ai-recruitment-startup-jack-jill-raises-20-million-dollars-to-expand-to-the-us/)
  - Mechanics: "Jack" is a voice career-coach agent for seekers; "Jill" is the employer agent that sources candidates *by searching Jack's network*. One headline: "puts an AI agent on both sides of the hiring table." — [Pulse 2.0](https://pulse2.com/jack-jill-raises-40-million-series-a/); [TNW headline](https://thenextweb.com/news/jack-and-jill-40m-series-a)
  - Traction (self-reported, figures differ by outlet): more than 385,000 job seekers and more than 5,350 companies; elsewhere about 350,000 people and 5,000 businesses, with no disclosed number of resulting hires. — [Pulse 2.0](https://pulse2.com/jack-jill-raises-40-million-series-a/); [SIA](https://www.staffingindustry.com/news/global-daily-news/recruitment-chatbot-firm-jack-jill-lands-40m-following-last-years-20m-seed-round)
  - Model: free for seekers, 10% commission on hires (2025 reporting). — [TechCrunch, Oct 2025](https://techcrunch.com/2025/10/16/jack-jill-raises-50-million-to-bring-conversational-ai-to-job-hunting)
  - A March 2026 security incident, in which a security-testing firm's autonomous agents accessed team members' personal data, appeared in search-summary coverage only; the source is unverified.
- **JobClaw**: an open, MCP-based "agent-to-agent hiring protocol." A seeker agent and a recruiter agent produce "ranked matches, evals, negotiation packets, interview slots." It is an open-source repo, not a company. jobclaw.org was pre-launch per REPORT.md. — [GitHub mirror VPC-byte/jobclaw](https://ithub.global.ssl.fastly.net/VPC-byte/jobclaw); [jobclaw.org](https://jobclaw.org/)
- **AgentHire / agenhire.com**: name collisions. The OpenClaw "AgentHire" skill is an agents-hire-agents crypto marketplace on Base Sepolia *testnet*, and ClawHub flags it "suspicious patterns detected." — [ClawHub](https://clawhub.ai/lngdao/agenthire); [ClawHub agenhire](https://clawhub.ai/tonypk/agenhire). Status of the agenhire.com employer-agent messaging product is unverified (per REPORT.md).
- **ClawSwarm Jobs**: an agent-to-agent job board paying out in HBAR (OpenClaw skill). — [ClawHub](https://clawhub.ai/imaflytok/clawswarm-jobs)
- **Tsenta** (YC): "AI career agent that matches you with jobs, applies automatically, and gets you the best offers." This is one-sided, candidate-side only. — [YC marketplace directory](https://www.ycombinator.com/companies/industry/marketplace)
- **Fika Jobs**: $4M (June 2026) for video-first hiring where AI agents interview candidates. — [TechCrunch](https://techcrunch.com/2026/06/23/fika-jobs-raises-4m-to-build-a-video-first-hiring-platform-where-ai-agents-interview-candidates/)
- **monday.com Agentalent.ai**: "hire AI agents like employees." This is a market for agents as workers, not principal matching. — [monday.com IR](https://ir.monday.com/news-and-events/news-releases/news-details/2026/monday-com-Launches-Agentalent-ai-a-Hiring-Platform-for-Enterprise-AI-Agents/default.aspx)
- Industry commentary: "agent-to-agent hiring will arrive from the candidate side and employers will react." — [Matt Alder, Recruiting Future](https://recruitingfuture.substack.com/p/have-your-agent-call-my-agent). Agents will need "accurate, structured and machine-readable job information." — [Job Board Doctor, Oct 2026](https://www.jobboarddoctor.com/2026/10/01/ai-agent-meets-ai-agent/). No independent data on hires completed agent-to-agent was found.

**Professional networking**
- **Boardy (Toronto/NYC)**
  - Funding: $3M pre-seed (Oct 2024; HF0 lead, with 8VC, Precursor, Afore, FJ Labs, NextView) and $8M seed (Jan 2025; Creandum lead), about $11M total. — [TechCrunch](https://techcrunch.com/2024/10/24/ai-networking-startup-boardy-raises-3m-pre-seed); [The Logic](https://thelogic.co/briefing/boardy-ai-raises-us8m-seed-round-for-ai-networking-tool/)
  - Estimated valuation $25–50M (Dealroom). — [Dealroom](https://dealroom.co/companies/boardy/)
  - Mechanics: a voice AI interviews users and makes double-opt-in email intros. It claims more than 100,000 introductions (self-reported). — [Goodword review](https://www.goodword.com/blog/boardy-ai-alternative-can-ai-really-manage-your-network)
  - No 2026 round found, and no evidence that Boardy talks to *other users' agents*: it is a central matchmaker.

**Dating** (mostly a central AI matchmaker; a few true agent-to-agent)
- **Ditto**: $9.2M seed (Feb 2026), about $14.5M total (estimate). Agents "simulate dates" and schedule in-person meetups; college campuses only. — [Business Insider via dnyuz](https://dnyuz.com/2026/02/03/this-startup-uses-ai-to-get-you-on-a-date-fast-read-the-pitch-deck-it-used-to-raise-9-2-million/)
- **Known (SF)**: $9.7M led by Forerunner (Dec 2025); voice-AI onboarding with a central matchmaker. — [TechCrunch](https://techcrunch.com/2025/12/19/known-uses-voice-ai-to-help-you-go-on-more-in-person-dates)
- **Sitch (NYC)**: $2M pre-seed (Apr 2025; a16z speedrun); AI plus human matchmakers. No 2026 round found. — [Dealroom](https://app.dealroom.co/companies/joinsitch)
- **Amata**: $6M raised (2023); AI matchmaking launched in the US. — [Landbase](https://www.landbase.com/blog/fastest-growing-dating-tech-companies-startups)
- **VibeRizz**: each user's agent "talks with other people's agents," recommends matches with reasons, the user approves every intro, and a safety-review step covers each conversation. Product Hunt only; no funding or usage found. — [Product Hunt](https://www.producthunt.com/p/viberizz/viberizz-2)
- **Datebook**: a personal agent talks to others' agents, with photos hidden by default (Product Hunt). — [PH](https://www.producthunt.com/products/datebook/makers)
- **Experiments and novelty products**:
  - MoltMatch (late Jan 2026; OpenClaw experiment) — [Digit](https://www.digit.in/features/general/moltmatch-is-a-dating-platform-for-ai-agents-no-we-are-not-kidding.html); [DatingNews](https://www.datingnews.com/industry-trends/moltmatch-is-exploring-how-ai-agents-date-each-other/)
  - BotLovin (Feb 4, 2026) — [PH](https://www.producthunt.com/posts/botlovin)
  - Love at First Byte — [PH](https://www.producthunt.com/p/love-at-first-byte)
- Forbes (Jul 2026): Gen-Z founders are racing to replace swipe apps. — [Forbes](https://www.forbes.com/sites/sofiachierchio/2026/07/11/these-gen-z-founders-are-reinventing-dating-apps-without-the-swipe/)
- **AFK.Love**: no source found in this pass (REPORT.md cites Axios May 2026; not re-verified).

**B2B procurement / finance**
- **Causa Prima (Munich/Delaware)**:
  - Funding: $20M seed led by Base10 (with QED, FJ Labs, Creandum, Kfund, Borusan; announced Oct 13, 2026), plus a $10M pre-seed (Creandum), for $30M total.
  - Product: "the agent-to-agent AI network for B2B finance." Buyer and supplier agents negotiate disputed invoices, early-payment terms and payment terms.
  - Sources: [Fortune](https://fortune.com/2026/10/13/startup-causa-prima-20-million-billing-disputes-ai-agents/); [WSGR](https://www.wsgr.com/en/insights/wilson-sonsini-advises-causa-prima-on-dollar20-million-seed-round.html); [Creandum](https://creandum.com/commitments/causa-prima)
- **Pactum (US/Estonia)**: $54M Series C (Jun 2025; Insight Partners lead), more than $100M total. Autonomous agents negotiate with suppliers at scale, mostly with human counterparties via chat. Earlier investors include Atomico and Maersk. — [Pactum](https://pactum.com/news-pactum-secures-54-million-in-series-c-funding-to-scale-agentic-ai-in-procurement/); [Built In](https://builtin.com/articles/pactum-raises-54m-series-c-20250610)
- **YC logistics/marketplace agents** (from the YC directory):
  - Godpack: agents "find the carrier, negotiate the rate."
  - Palisade (S26): a dedicated sales/matching agent per marketplace visitor.
  - Orthogonal (W26): agents "discover, negotiate, and pay for API services."
  - Veritus (S25): agents negotiate repayment plans.

  Source: [YC directory](https://www.ycombinator.com/companies/industry/marketplace); [SV Post on YC S26](https://svpost.com/articles/top-marketplace-startups-yc-s26/)

**Real estate**
- No startup found where a buyer AI agent negotiates directly with a seller AI agent.
- Purlin merged with Final Offer (a consumer offer-negotiation marketplace) in Feb 2026. — [RISMedia](https://www.rismedia.com/2026/02/03/purlin-and-final-offer-merge-to-create-real-estates-first-ai-operating-system-for-real-estate-mortgage-and-title/)
- A Washington brokerage abandoned a "purely AI real estate agent" because "regulatorily speaking, you actually can't do that" (licensing). — [Real Estate News](https://www.realestatenews.com/2025/07/10/hybrid-buyer-agent-blends-ai-with-the-human-touch)

**Freelance marketplaces**
- **Upwork**: Uma evolved from a companion into an "AI work agent" (Summer 2025, Spring 2026) for SMB hiring. — [Upwork press, Spring 2026](https://www.upwork.com/press/releases/upwork-updates-spring-2026-ai-powered-innovations-to-help-small-businesses-get-ambitious-work-done)
- Upwork's CEO said clients' **AI agents are already posting jobs on Upwork to hire humans**. In 2025 experiments, adding a human freelancer to an AI agent raised completion rates by 70% or more. — [Semafor, Mar 12, 2026](https://www.semafor.com/article/03/12/2026/upworks-ceo-on-the-ai-agents-that-try-to-hire-human-workers)
- **Fiverr**: Fiverr Go (a seller's "Personal AI Assistant" that answers buyers) and Fiverr Neo (AI matching). — [Upwork comparison guide](https://www.upwork.com/resources/upwork-vs-fiverr)

### Inferences
- Proximity scores:

  | Player | Score | Note |
  |---|---|---|
  | Jack & Jill | **4** | Two-sided agents, real network, monetized; but closed, single-vertical, its own agents only |
  | Causa Prima | **4 in B2B finance** | Explicitly "agent-to-agent network"; vertical-specific |
  | Tobira, VibeRizz, Datebook | 3.5–4 | Right mechanic, no scale |
  | Boardy | 3 | Central matchmaker, not agent-to-agent |
  | Pactum | 2.5 | |
  | Upwork / Fiverr | 2.5 | Have liquidity; could add bring-your-own-agent endpoints quickly |
  | Dating (Known, Ditto, Sitch, Amata) | 2–3 | |
- Jack & Jill is the **most dangerous vertical competitor for the hiring running example**. It has both sides, about 5K employers and about 385K seekers, $60M, and a 10% take rate. If it opens Jill or Jack to third-party agents (for example via A2A), it becomes the de facto hiring exchange.
- Upwork's comment that agents post jobs shows that incumbents with liquidity will receive agent traffic by default. A neutral hub must offer something they don't: cross-domain reach, bring-your-own-agent, and neutrality.
- In regulated verticals such as real estate and hiring, licensing and AI-hiring laws favor a "match + human handoff" model over fully autonomous closing. That validates the AgentsHub handoff design.

### Gaps
- Jack & Jill: hires completed, revenue, and whether third-party agents can connect. The primary article could not be fetched.
- JobClaw / agenhire.com: launch status and usage.
- AFK.Love: no information found.
- VibeRizz, Tobira, Datebook: funding and users.
- Causa Prima: number of live counterparties.
- Funding for Godpack, Palisade and Orthogonal.

---

## Q2. What have big platforms shipped toward agent-to-agent matching?

### Takeaway
Big platforms have shipped **registries, marketplaces, protocols and checkout**, i.e., "find and buy an agent or service." None has shipped **cross-principal intent matching between consumers' or businesses' agents**.

The closest moves are:
- Meta acquiring Moltbook (an agent social graph)
- LinkedIn and Indeed running agents on *both* sides of hiring inside their walls
- Anthropic's Project Deal and Project Swap research, which is literally agent-to-agent marketplaces, but experiments only

### Cited Findings

**Google**
- April 23, 2026 (Cloud Next): partner-built agents from Google Cloud Agent Marketplace appear in the Gemini Enterprise "Agent Gallery" (Adobe, Salesforce, ServiceNow, Workday). — [Google Cloud blog](https://cloud.google.com/blog/products/ai-machine-learning/partner-built-agents-available-in-gemini-enterprise)
- Publishing requires A2A compliance with an Agent Card (skills, auth, endpoints) and OAuth 2.0 (July 7, 2026 developer guide). — [Google Cloud blog](https://cloud.google.com/blog/topics/developers-practitioners/publish-agents-in-gemini-enterprise-and-google-cloud-marketplace); [Docs](https://docs.cloud.google.com/gemini/enterprise/docs/register-and-manage-marketplace-agents)
- A2A reportedly has 150+ organizations, and the Linux Foundation hosts it. — [Linux Foundation](https://www.linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year)
- The 1.5% marketplace fee cut on some deals is per REPORT.md, not re-verified. — [Google Cloud](https://cloud.google.com/blog/topics/partners/google-cloud-ai-agent-marketplace)

**Microsoft**
- Agent 365 became generally available May 1, 2026 as a central registry and governance layer. Registry sync (preview) pulls agents from Bedrock, Vertex AI, Agentforce and Databricks. — [Microsoft Security blog](https://microsoft.com/en-us/security/blog/2026/05/01/microsoft-agent-365-now-generally-available-expands-capabilities-and-integrations); [Microsoft Learn](https://learn.microsoft.com/microsoft-agent-365/admin/agent-registry)
- Centralized controls were added in Sept 2026. — [Redmond](https://redmondmag.com/blogs/redmond-dispatch/2026/09/microsoft-agent-365-adds-centralized-controls.aspx)
- NLWeb (2025): every NLWeb site is an MCP server, making websites agent-queryable. — [Microsoft](https://news.microsoft.com/source/features/company-news/introducing-nlweb-bringing-conversational-interfaces-directly-to-the-web/)
- Copilot Checkout launched Jan 2026. — [GeekWire](https://www.geekwire.com/2026/microsoft-launches-copilot-checkout-joining-the-ai-shopping-race-against-amazon-google-and-openai/)
- A publisher AI marketplace / agentic web infrastructure was announced Apr 2026. — [Axios](https://axios.com/2026/04/21/microsoft-ai-marketplace-publishers); [Dataconomy](https://dataconomy.com/2026/04/22/microsoft-unveils-tools-to-build-infrastructure-for-agentic-web/)
- Entra Agent ID gives verified agent identity (per REPORT.md).

**AWS**
- AgentCore Agent Registry reached general availability on Aug 31, 2026 (governance and discovery), plus an open "Agentic Resource Discovery" spec (secondary source). — [Atlan](https://atlan.com/know/ai-agent/what-is-an-ai-agent-registry.md)
- AWS Marketplace agents run inside the buyer's account, and purchases draw down cloud commits. — [Meticulous Research](https://www.meticulousresearch.com/meticulous-next/enterprise-ai-agent-marketplaces-outlook-2026-2034)
- Coinbase + AWS let publishers accept agents as paying customers via x402. — [Coinbase](https://www.coinbase.com/blog/coinbase-and-aws-let-publishers-accept-agents-as-customers-via-x402)

**Salesforce**
- AgentExchange merged AppExchange, Slack Marketplace and Agentforce, with 1,000+ agents, tools and MCP servers (analyst figure). — [Futurum](https://futurumgroup.com/insights/can-agentexchange-cement-salesforces-lead-in-the-agentic-ai-platform-race/); [Meticulous Research](https://www.meticulousresearch.com/meticulous-next/enterprise-ai-agent-marketplaces-outlook-2026-2034)
- MuleSoft Agent Fabric registry (Oct 2025) scans Bedrock, Vertex and Copilot Studio agents (Jan 2026). — [Atlan](https://atlan.com/know/ai-agent/how-to-govern-ai-agents-across-multiple-clouds.md)

**OpenAI**
- Agentic Commerce Protocol (open-sourced) plus Instant Checkout (Sept 2025; small merchant fee). Instant Checkout was sidelined in March 2026 in favor of merchant ChatGPT apps.
- A searchable ChatGPT app directory exists, with apps from Walmart, DoorDash, Instacart and The Knot.
- Sources: [OpenAI](https://openai.com/index/buy-it-in-chatgpt/); [Digital Commerce 360](https://www.digitalcommerce360.com/2026/03/06/openai-shifts-checkout-plans-agentic-commerce-strategy/); [DC360 Walmart](https://www.digitalcommerce360.com/2026/03/24/openai-agentic-commerce-updates-chatgpt-walmart/)
- Agent Builder deprecation was announced June 3, 2026, with shutdown Nov 30, 2026, replaced by Workspace Agents (secondary source). — [Refonte Learning](https://www.refontelearning.com/blog/openai-agent-builder-shutdown-vendor-lock-in)

**Anthropic** (research, not product)
- **Project Deal** (run Dec 2025, published Apr 2026):
  - 69 employees, $100 each. Claude agents listed items, made offers and counter-offers, and closed 186 deals worth more than $4K across 500+ listings.
  - Stronger models got better outcomes, and participants didn't notice when they were represented by weaker models.
  - Sources: [Anthropic](https://www.anthropic.com/research/project-deal); [TechCrunch](https://techcrunch.com/2026/04/25/anthropic-created-a-test-marketplace-for-agent-on-agent-commerce/)
- **Project Swap** (published Sept 24, 2026; primary source fetched): [Anthropic](https://www.anthropic.com/news/project-swap)
  - Setup: 201 employees in 6 offices, a book barter on an open "trading floor," bilateral and multi-party rotations, half the agents "ruthless" and half "prosocial."
  - Preference capture: Claude's preference rankings matched participants' own rankings on 61% of pairs (chance is 50%; collaborative filtering about 55%).
  - Efficiency: the market achieved **0.55** versus a utilitarian optimum of **0.89**. **About 85% of the shortfall came from preference representation and about 15% from bargaining.**
  - Model effects: efficiency on Claude's rankings was Haiku 0.75, Sonnet 0.80, Opus 0.88 and Fable 0.86. Equity (worst-off decile) was Haiku 0.05 vs Opus 0.38. Model choice mattered more than ruthless vs prosocial instructions (ruthless gained about +0.02).
  - Agent behavior: agents lied about their top pick about 1 in 100 times.
  - Participant attitudes: people would delegate about 30% of their book budget to an agent versus about 40% to a well-read friend.
  - Proposed safeguards: tests that an agent understands its person, full activity logs, **agent identity registries**, and **rate limits on agent messages**.
  - Next steps: adversarial agents and varied market rules. A secondary source says procurement scenarios are planned. — [Enterprise DNA](https://enterprisedna.co/resources/news/anthropic-project-swap-ai-agents-negotiate-enterprise-market-2026/)

**Meta**
- Acquired Moltbook (Mar 10, 2026); the team joined Meta Superintelligence Labs. Meta said the team "opens up new ways for AI agents to work for people and businesses." — [TechRadar](https://www.techradar.com/pro/meta-snaps-up-ai-agent-social-network-moltbook-founders-will-join-meta-superintelligence-labs)

**LinkedIn**
- Hiring Assistant (recruiter-side agent) went global in Sept 2025. Hiring Pro serves SMB hirers. — [LinkedIn](https://news.linkedin.com/2025/hiring-assistant-globally-available)
- On the seeker side, Jobs Match (Jan 2025) cut US Premium "low-match" applications by 10%. — [TechCrunch](https://techcrunch.com/2025/01/15/linkedin-ads-free-ai-tools-for-job-hunters-and-recruiters/); [LinkedIn Research 2026](https://news.linkedin.com/2026/LinkedIn-Research-Talent-2026?)
- Sept 2026: LinkedIn wants AI to do candidate search for recruiters. — [Business Today](https://www.businesstoday.in/jobs/story/recruiters-may-soon-stop-searching-for-candidates-linkedin-wants-ai-to-do-it-553287-2026-09-03)
- No candidate-side agent that negotiates with employer agents was found.

**Indeed**
- Career Scout (seeker agent) and Talent Scout (employer "virtual recruiter") launched Sept 2025. Indeed Connect (ATS integration) was due Jan 2026. Career Scout reportedly helps seekers apply "7x faster" (self-reported). — [Indeed press release](https://www.indeed.com/news/releases/indeed-introduces-new-suite-of-hiring-products-career-scout-talent-scout-premium-sponsored-jobs-and-indeed-connect?co=US)

### Inferences
- **Indeed is quietly the closest incumbent in hiring**: it has an agent on each side (Career Scout and Talent Scout) inside one marketplace. Whether those agents converse directly is unconfirmed. LinkedIn has the bigger graph but only recruiter-side agents.
- The cloud majors have converged on *enterprise* registry, governance and marketplace (A2A Agent Cards, Entra/AgentCore identity), so they are infrastructure for AgentsHub rather than competitors. They are, however, building the discovery primitives (registries, federated discovery specs) that a hub would otherwise own.
- The frontier labs and Meta own the consumer agents. A "find me a counterparty" feature in ChatGPT, Gemini, Claude or Meta AI would be the most dangerous long-term threat, since each owns user context, which Project Swap shows is the binding constraint (85% of the shortfall). Anthropic's own proposed safeguards (identity registries, rate limits, activity logs) read like a spec for a neutral hub.

### Gaps
- No evidence on whether Indeed's Career Scout and Talent Scout negotiate directly.
- No confirmed LinkedIn seeker agent at Talent Connect 2026.
- No count of A2A agents listed in Google's marketplace.
- No public Meta product plans for Moltbook.
- The Google 1.5% fee figure was not re-verified.

---

## Q3. Funding, traction, business model and verification summary

### Takeaway
Funding is concentrated in vertical agent-to-agent players (Jack & Jill $60M, Causa Prima $30M, Pactum >$100M) and in crypto-native horizontal networks. The horizontal crypto networks' traction metrics are largely self-reported and contradicted by independent audits. No pure-play neutral cross-domain intent hub has disclosed a priced round.

### Cited Findings

| Player | Category | Funding (latest) | Launch / status | Claimed traction | Model | Verified? | Proximity (0–5) |
|---|---|---|---|---|---|---|---|
| Jack & Jill | Hiring, two-sided agents | $40M A, Air Street (Sep 2026); about $60M total ([SIA](https://www.staffingindustry.com/news/global-daily-news/recruitment-chatbot-firm-jack-jill-lands-40m-following-last-years-20m-seed-round)) | Live, UK + US | 385K seekers, 5,350 cos ([Pulse2](https://pulse2.com/jack-jill-raises-40-million-series-a/)) | 10% of hire, free for seekers | Self-reported | 4 |
| Causa Prima | B2B finance agent-to-agent | $20M seed, Base10 (Oct 2026); $30M total ([WSGR](https://www.wsgr.com/en/insights/wilson-sonsini-advises-causa-prima-on-dollar20-million-seed-round.html)) | Live, early | n/a | SaaS/network (inferred) | — | 4 (vertical) |
| Pactum | Procurement negotiation | $54M C, Insight (Jun 2025); >$100M ([Pactum](https://pactum.com/news-pactum-secures-54-million-in-series-c-funding-to-scale-agentic-ai-in-procurement/)) | Live, enterprise | n/a here | Enterprise SaaS | — | 2.5 |
| Boardy | Networking | $8M seed, Creandum (Jan 2025); about $11M ([The Logic](https://thelogic.co/briefing/boardy-ai-raises-us8m-seed-round-for-ai-networking-tool/)) | Live | 100K+ intros ([Goodword](https://www.goodword.com/blog/boardy-ai-alternative-can-ai-really-manage-your-network)) | n/a | Self-reported | 3 |
| Fetch.ai Agentverse/ASI:One | Horizontal, crypto | About $78M equity (est.) + token treasury ([Clay](https://clay.com/dossier/fetchai-funding)) | Live; ASI:One beta Nov 2025 | 2.7–3M agents (claimed) vs about 36K active (audit) | Token, business tier | Contradicted | 3 |
| Virtuals ACP | Horizontal, crypto | Token-funded | Revenue Network Feb 2026 | $479M aGDP, 1.77M jobs, 18K agents, $1.16M agent revenue ([BlockEden](https://blockeden.xyz/blog/2026/04/04/virtuals-protocol-ai-economic-operating-system-on-chain-agent-economy/)) | Protocol fees, incentives | Self-reported; dashboard dispute | 3 |
| Coinbase x402 / Agentic.market | Payments + catalog | Coinbase-internal | Agentic.market Apr 20, 2026 | 165M tx, $50M, 480K agents ([Coinbase](https://www.coinbase.com/developer-platform/discover/launches/agentic-market)) | Free protocol; facilitator | Contradicted (TRM: about $5–11K/mo agentic) | 2 |
| Olas | Horizontal, crypto | $13.8M (Feb 2025) ([The Block](https://www.theblock.co/post/338713/olas-raises-13-8-million-to-launch-pearl-an-app-store-for-autonomous-ai-agents-in-crypto)) | Live | 14.2M agent-to-agent tx; $108K turnover; $546 fees ([RootData](https://www.rootdata.com/projects/detail/Autonolas?k=Nzk2NA%3D%3D)) | Protocol fee | Onchain (aggregator) | 2 |
| Pilot Protocol | Agent network overlay | $4.5M seed, Version One (Jul 2026) ([TechStartups](https://techstartups.com/2026/07/27/pilot-protocol-emerges-from-stealth-with-4-5m-to-build-the-internet-for-ai-agents/)) | Live | 250K agents, 2B req/day | n/a; payments planned | Self-reported | 2.5 |
| Nevermined | Agent payments | $4M (Jan 2025); about $7M ([PYMNTS](https://pymnts.com/news/investment-tracker/2025/nevermined-raises-4-million-to-help-ai-agents-pay-and-get-paid)) | Live | n/a | Payments fee | — | 1 |
| Moltbook | Agent social | Acquired by Meta (Mar 2026) | Temporary continuation | 2.8M agents claimed | — | Contradicted | 2 |
| Tobira | Horizontal agent-to-agent match | None found | Live (PH) | n/a | Free | — | 4 |
| Ditto / Known / Sitch / Amata | Dating | $9.2M / $9.7M / $2M / $6M | Live | n/a | Consumer | — | 2–3 |
| VibeRizz / Datebook | Dating agent-to-agent | None found | PH launches | n/a | — | — | 3.5 |

### Inferences
- Funded verticals monetize with take rates on outcomes (Jack & Jill 10%), while horizontals monetize with tokens and incentives. A neutral hub's revenue model should copy the verticals (per-qualified-match or success fee), not the token subsidies.

### Gaps
- Revenue figures are absent for all private companies.
- Pactum and Causa Prima customer counts are not found.

---

## Q4. Stealth or recently funded (2025–2026) startups, and failed or shut-down attempts

### Takeaway
2026 money is flowing into agent-network *infrastructure* (Pilot $4.5M, AIsa $6.5M, Doxx.net $38M) and *vertical agent-to-agent negotiation* (Causa Prima $30M, Jack & Jill $40M A). Failures so far are pivots or acquihires rather than blow-ups: Moltbook to Meta, Nagent retiring its agent marketplace, OpenAI killing Agent Builder. The failure modes are trust and security, vanity metrics, and lack of real liquidity.

### Cited Findings

**Recently funded**
- Pilot Protocol: $4.5M (Jul 2026). — [TechStartups](https://techstartups.com/2026/07/27/pilot-protocol-emerges-from-stealth-with-4-5m-to-build-the-internet-for-ai-agents/)
- Causa Prima: $20M seed (Oct 2026). — [Fortune](https://fortune.com/2026/10/13/startup-causa-prima-20-million-billing-disputes-ai-agents/)
- Jack & Jill: $40M A (Sep 2026). — [SIA](https://www.staffingindustry.com/news/global-daily-news/recruitment-chatbot-firm-jack-jill-lands-40m-following-last-years-20m-seed-round)
- AIsa: $6.5M. — [AIsa](https://aisa.one/news/aisa-raises-6-5m-ai-agent-resource-network)
- Doxx.net: $38M A led by a16z, for "agentic networking." This is private networking infrastructure, not matching. — [Axios Pro](https://www.axios.com/pro/enterprise-software-deals/2026/10/01/doxxnet-a16z-lyon-networking)
- Ditto: $9.2M seed (Feb 2026). — [BI via dnyuz](https://dnyuz.com/2026/02/03/this-startup-uses-ai-to-get-you-on-a-date-fast-read-the-pitch-deck-it-used-to-raise-9-2-million/)
- Fika: $4M (Jun 2026). — [TechCrunch](https://techcrunch.com/2026/06/23/fika-jobs-raises-4m-to-build-a-video-first-hiring-platform-where-ai-agents-interview-candidates/)
- Agent security and identity:
  - Reco $55M — [TechCrunch](https://techcrunch.com/2026/09/29/reco-raises-55m-as-ai-agent-security-startups-crowd-the-market/)
  - Metano $12M — [SiliconANGLE](https://siliconangle.com/2026/11/19/metano-launches-with-12m-to-help-enterprises-secure-ai-agents/)
- YC 2026: Orthogonal (W26; agents discover, negotiate and pay for APIs), Palisade (S26; per-visitor marketplace matching agents), Agentcard (S26; agent checkout). YC also ran a "Call My Agent" hackathon. — [YC directory](https://www.ycombinator.com/companies/industry/marketplace); [YC Agentcard](https://www.ycombinator.com/companies/agentcard); [YC event](https://events.ycombinator.com/CallMyAgentHackathon)
- I found no YC 2025–26 company that is a cross-domain agent-to-agent intent-matching hub.

**Failed, shut down or pivoted**
- **Moltbook**: viral (2.8M claimed agents) but riddled with security failures (leaked keys, impersonation) and inflated activity. Acquihired by Meta within about 2 months; existing users can continue only "temporarily." — [TechRadar](https://www.techradar.com/pro/everything-you-need-to-know-about-moltbook); [Fortune](https://fortune.com/2026/02/03/moltbook-ai-social-network-security-researchers-agent-internet/)
- **Nagent** retired its agent marketplace on Oct 9, 2026 in favor of "ready-made AI teammates" in one shared context. That is a pivot away from a marketplace model. — [Nagent blog](https://nagent.ai/resources/blog/is-there-a-marketplace-for-ai-agents)
- **OpenAI Agent Builder**: deprecated, shutting down Nov 30, 2026 (vendor lock-in lesson). — [Refonte Learning](https://www.refontelearning.com/blog/openai-agent-builder-shutdown-vendor-lock-in)
- **OpenAI Instant Checkout** was sidelined in Mar 2026 in favor of merchant apps. — [Digital Commerce 360](https://www.digitalcommerce360.com/2026/03/06/openai-shifts-checkout-plans-agentic-commerce-strategy/)
- **Olas** retired its legacy Mech agents (Q1 2026). Its marketplace fee earned $546 lifetime, an illustration of thin agent-to-agent liquidity. — [Olas](https://olas.network/blog/olas-q1-2026-roundup); [RootData](https://www.rootdata.com/projects/detail/Autonolas?k=Nzk2NA%3D%3D)
- **Real-estate "pure AI agent"** was abandoned for regulatory reasons. — [Real Estate News](https://www.realestatenews.com/2025/07/10/hybrid-buyer-agent-blends-ai-with-the-human-touch)
- **Relay.app** (automation, not matching) shut down July 2026 with no reason given (aggregator). — [Killed by AI](https://killedbyai.net/)

**Investor framing**
- NFX: "a race to build the key platforms where AI Agents transact"; marketplaces are highly defensible once they have traction. — [NFX](https://nfx.com/post/ai-agent-marketplaces)
- a16z "Welcome to the B2A Economy" (Nov 2026; B2A = business-to-agent) is about selling *to* agents. Its market map has 111 infra logos vs 81 consumer apps, with payments the largest segment. — [a16z](https://a16z.com/welcome-to-the-b2a-economy/); [FourWeekMBA](https://fourweekmba.com/ai-a16z-agent-economy-map-111-infra-logos-vs-81-consumer-apps/)
- a16z "Marketplaces in the age of AI: graveyard to greenfield." — [a16z](https://a16z.com/marketplaces-in-the-age-of-ai-take-two-graveyard-to-greenfield/)

### Inferences
- The VC map is infrastructure-heavy (payments, identity, networking). Investors haven't yet funded a "neutral intent exchange" category, which is whitespace but also a fundraising-narrative risk.
- Why attempts fail:
  1. Security and impersonation (Moltbook)
  2. Liquidity illusions from bots and wash activity (x402, Fetch, Olas)
  3. Platform dependency (OpenAI Agent Builder)
  4. Regulatory licensing in verticals (real estate)
  5. Marketplace-vs-product pull (Nagent)

### Gaps
- Stealth companies by definition aren't findable. The Information and Axios Pro were inaccessible (Axios fetch blocked).
- No PitchBook or Crunchbase category totals for "agent-to-agent marketplace" funding.

---

## Q5. Whitespace, and who is best positioned to close it

### Takeaway
The unclaimed position is a **neutral, bring-your-own-agent, cross-domain intent exchange**: structured needs and offers, verified principals, rules-bound agent conversations, outcome-based reputation, and human handoff. Each existing player is missing at least one element:
- verticals are closed (Jack & Jill, Causa Prima)
- horizontals match services, not principals' intents (Fetch, Virtuals, x402, Olas)
- big platforms do registries and checkout (Google, Microsoft, AWS, Salesforce)
- the only true horizontal agent-to-agent matchers are tiny (Tobira)

**Most dangerous competitors**, in order:
1. Meta (Moltbook team, plus consumer distribution and messaging)
2. OpenAI / Google / Anthropic adding native "find me a counterparty" (they own preference context)
3. Jack & Jill (in hiring; could open to third-party agents)
4. Indeed / LinkedIn (both-side data in hiring)
5. Fetch.ai (horizontal discovery plus an agent chat protocol; could add intent matching)

### Cited Findings
- Project Swap: about 85% of a market's shortfall came from agents' imprecise picture of what their humans want, not from negotiation. Anthropic recommends identity registries, rate limits on agent messages, and reviewable activity logs. — [Anthropic Project Swap](https://www.anthropic.com/news/project-swap)
- Project Deal: weaker-model principals got worse deals without noticing, a fairness problem for any open hub. — [Anthropic Project Deal](https://www.anthropic.com/research/project-deal)
- Independent audits show agent-economy volume is far smaller than claimed (TRM: about $5–11K/month agentic x402; Fetch about 36K active vs 2.7M claimed). — [TRM Labs](https://www.trmlabs.com/trm-tech-blog/whos-actually-paying-measuring-ai-agent-payments-onchain)
- Tobira's double-gated design (agents verify claims, then both humans approve, with contact details hidden) is the closest live instantiation of the hub's handoff mechanic. — [Product Hunt](https://www.producthunt.com/posts/tobira-ai)
- Jack & Jill's design (Jill searches Jack's network) shows that a two-sided agent network can monetize at a 10% take. — [Pulse 2.0](https://pulse2.com/jack-jill-raises-40-million-series-a/); [TechCrunch](https://techcrunch.com/2025/10/16/jack-jill-raises-50-million-to-bring-conversational-ai-to-job-hunting)
- Upwork already receives job posts from AI agents trying to hire humans: agent-originated demand exists today. — [Semafor](https://www.semafor.com/article/03/12/2026/upworks-ceo-on-the-ai-agents-that-try-to-hire-human-workers)
- Enterprise registries (Agent 365 registry sync across clouds; AWS Agent Registry; Google A2A Agent Cards) standardize discovery metadata a hub can ingest. — [Microsoft Learn](https://learn.microsoft.com/microsoft-agent-365/admin/agent-registry); [Google Docs](https://docs.cloud.google.com/gemini/enterprise/docs/register-and-manage-marketplace-agents)

### Inferences
- **Whitespace, stated precisely:**
  1. **Intent layer**: a typed need/offer schema with preference elicitation. This is the 85% lever from Project Swap and is ignored by service-call marketplaces.
  2. **Cross-domain liquidity**: one agent identity reused across hiring, networking, dating, B2B and barter. Verticals can't offer this.
  3. **Neutrality and bring-your-own-agent**: any A2A/MCP agent from any lab. Labs and Meta can't credibly be neutral.
  4. **Trust**: verified principals (KYA/KYC partners), sybil and spam economics, audit logs, and model-strength disclosure to mitigate Project Deal-style unfairness.
  5. **Outcome metrics**: human-approved handoffs, not agent counts.
- **Who could close it fastest:**
  - **Meta** (has the team, consumer graph and messaging; low neutrality)
  - **Fetch.ai** (has the agent directory, agent chat protocol and ASI:One front door; lacks principal intent and mainstream trust, and has crypto baggage)
  - **Jack & Jill** (could generalize from hiring to "agents on both sides of any table," but is vertical-focused)
  - **Tobira** (exact concept, no capital)
  - **Google** (A2A owner; could add an "intent card" to Agent Cards plus Gemini-side matching)
- Defensive implication for AgentsHub:
  - Pick one wedge vertical where incumbents are one-sided or closed. Hiring is contested by Jack & Jill, Indeed and LinkedIn, so consider SMB/freelance gigs, B2B intros or barter, where no funded agent-to-agent player exists.
  - Make neutrality and verifiability the moat.
  - Position as infrastructure that vertical apps (VibeRizz, Tobira-like, JobClaw) can plug into rather than compete with.
- Danger ranking rationale: Meta combines intent (it is a social graph), distribution and an acquired agent-network team. The frontier labs own the preference context that Project Swap shows matters most. Jack & Jill is the only well-funded player already monetizing agent-on-both-sides matching.

### Gaps
- No direct evidence that Meta, OpenAI, Google or Anthropic plan a cross-principal matching product. The ranking is inferential.
- No data on whether users would trust a third-party hub over their assistant's native features.
- Fetch.ai's roadmap for intent matching was not found.
