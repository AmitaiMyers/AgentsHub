# Business Model & Go-To-Market for an Agent-to-Agent Matching Hub (hiring as first vertical) — as of Nov 2026

Scope note: these notes go deeper than section 5 of /home/user/AgentsHub/research/REPORT.md (which proposed success fee per hand-off + verification + subscriptions; MCP-first distribution; hosted "lite agent"; seeding from public ATS feeds; one niche first). Below are the benchmarks and case evidence behind (or against) those choices. Many recruiting price points come from vendor/competitor blogs, flagged as such. Source-quality caveat: a lot of 2026 figures came via search-result summaries of secondary outlets; primary filings were not opened directly for every number.

---

## 1. Marketplace economics: take rates, fee models, leakage

### Takeaway
At-scale talent/services marketplaces charge ~20% (Upwork ~20%, Fiverr ~28%, contingency recruiters 15–25% of salary, Paraform ~20–25% of salary), and both public freelance marketplaces are raising take rates while their volume shrinks. Leakage is real but measurable (~5% offline on Airbnb in one study), and the main defenses are value delivered on-platform (payments, trust, protection) plus pricing that drops as relationships deepen. Per-call micropayments (x402) are real in count but tiny in dollars and mostly non-agentic, so they are not a viable main revenue model for a matching hub.

### Cited Findings
**Freelance marketplaces (public filings / earnings calls)**
- Upwork marketplace take rate: 19.4% Q1 2026; 19.8% Q2 2026 (up 40 bps YoY) while GSV fell 4% YoY to $966.4M and active clients fell 4% to 763k; FY2026 revenue guide $730–750M; management blames AI automation, weaker Google search referrals, soft labor market — [Nasdaq Q2 call highlights](https://www.nasdaq.com/articles/upwork-q2-earnings-call-highlights); [Fool Q1 2026 transcript](https://www.fool.com/earnings/call-transcripts/2026/05/12/upwork-upwk-q1-2026-earnings-transcript/); [Barchart Q1 deep dive](https://www.barchart.com/story/news/1880176/upwk-q1-deep-dive-lowered-revenue-outlook-and-cost-cuts-amid-ai-shifts)
- Upwork Q3 2026 take rate reported at 20.0% (+110 bps YoY), driven by "higher-margin products" — secondary transcript summary, verify against release — [Webull Q3 2026 transcript](https://www.webull.com/news/15858144814720000)
- Upwork fee structure: freelancer service fee variable 0–15% (replaced 20/10/5% tiers, reportedly May 2025), most freelancers pay ~10%; client marketplace fee reported ~3–5% (basic) up to ~8–10% (Business Plus) — third-party sources disagree on details — [Upwork: Is Upwork free](https://www.upwork.com/resources/is-upwork-free); [Jobbers fee guide](https://www.jobbers.io/upwork-fees-explained-hidden-costs-freelancers-dont-know-about/); [Hackernoon "Upwork fees are basically vibes now"](https://hackernoon.com/lite/upwork-fees-are-basically-vibes-now)
- Fiverr trailing-12-month take rate: 27.7% (Q1 2026), 28.0% (Q2), 28.2% (Q3 2026, vs 27.6% prior year). Q3 revenue $90.9M, −15.8% YoY; FY2026 revenue guide $374–380M (−12–13%); annual active buyers 2.4M vs 3.3M a year earlier; spend per buyer $373 (+12.9%) — [Fiverr Q3 2026 results (GlobeNewswire via Morningstar)](https://www.morningstar.com/news/globe-newswire/9855650/fiverr-announces-third-quarter-2026-results); [Fiverr Q2 2026](https://www.fiverr.com/news/fiverr-q2-2026-earnings); [Staffing Industry Analysts on Q3](https://www.staffingindustry.com/news/global-daily-news/fiverr-q3-revenue-falls-158-amid-downturn-in-marketplace-segment)

**Dating (subscription model, the counter-example to success fees)**
- Match Group Q3 2026: revenue $891M (−3%), payers 13.8M (−5%), revenue per payer $21.19/month (+3%). Tinder ~8.9M payers at ~$18 RPP; Hinge payers +23%, revenue +19% to ~$221M, RPP ~$30–33 (≈2x Tinder). Analyst-metric tables disagree slightly with the brand table — [Global Dating Insights](https://www.globaldatinginsights.com/featured/match-group-q3-2026-results-hinge-growth-and-new-plans-for-tinder/); [Securities.io](https://www.securities.io/payers-fall-5-at-match-group-as-q3-revenue-slips-to-891-million/); [Nasdaq/Zacks key metrics](https://www.nasdaq.com/articles/compared-estimates-match-group-mtch-q3-earnings-look-key-metrics)

**General take-rate benchmarks and theory**
- Take-rate benchmarks range from low single digits to mid-30s%; GMV-based marketplaces commonly 10–30%; marketplaces with strong network effects and hard-to-reach buyers can charge more; where users multi-home cheaply, rates converge to the lowest competitor — [Rework take rate](https://resources.rework.com/libraries/marketplace-growth/marketplace-take-rate); [Sharetribe glossary](https://www.sharetribe.com/academy/marketplace-glossary/)
- William Blair studied 300+ private/public company take rates (study exists; numbers not retrieved) — [William Blair](https://williamblair.com/Insights/Proprietary-Study-of-300-Plus-Private-and-Public-Company-Take-Rates)
- Higher take rate typically lowers transaction volume, so a deliberately low early rate is a common strategy — [Sharetribe glossary](https://www.sharetribe.com/academy/marketplace-glossary/); [TechCrunch: 4 strategies for setting marketplace take rates](https://techcrunch.com/2021/11/17/4-strategies-for-setting-marketplace-take-rates/)

**Leakage / disintermediation**
- Research estimates ~5.4% of Airbnb transactions in Austin, TX are taken offline — [UCLA Anderson Review](https://anderson-review.ucla.edu/a-renter-and-property-owner-meet-on-airbnb-will-they-ditch-the-site)
- Leakage is also a measurement problem: off-platform deals never show in GMV, so true liquidity is higher than measured — [Rework disintermediation](https://resources.rework.com/libraries/marketplace-growth/marketplace-disintermediation); [Rework metrics](https://resources.rework.com/libraries/marketplace-growth/marketplace-metrics)
- Academic work on "platform leakage" in two-sided markets — [PKU HSBC Business School](https://english.phbs.pku.edu.cn/info/3882/48882.htm); [BU Platform Strategy 2023 paper](https://questromworld.bu.edu/platformstrategy/wp-content/uploads/sites/49/2023/06/PlatStrat2023_paper_27.pdf)
- Upwork's move to a fee that can fall toward 0% and is locked per contract / declines with lifetime billing with a client is a leakage-reduction lever (mechanics disputed by sources) — [Jobbers](https://www.jobbers.io/upwork-fees-explained-hidden-costs-freelancers-dont-know-about/)

**Per-call / x402**
- x402 lifetime: ~196M transactions across 12 chains settling >$42M total as of Nov 1, 2026 (aggregate figure via crypto press); another count ~$15M adjusted volume over 109.6M tx since May 2025 launch; 87% of transactions <$0.10 by Sept 2026 (Chainalysis, via press); volume fell ~77% from Nov 2025 peak ($5.15M) to $1.19M by May 2026 — [Brave New Coin / Chainalysis](https://bravenewcoin.com/insights/coinbases-x402-records-138-5m-transactions-chainalysis-shows-ai-agents-reshaping-crypto-payments); [CryptoSlate](https://cryptoslate.com/tiny-x402-payments-expose-gap-holding-ai-agents-back/?rand=6792); [BeInCrypto](https://beincrypto.com/x402-transactions-drop-in-feb); [KuCoin $15M volume](https://www.kucoin.com/blog/es-visa-accelerates-ai-agent-payments-x402-protocol-hits-15m-on-chain-volume)
- TRM Labs: x402 is the most-used agent-payment rail but most of its volume is not agentic (any script can drive the 402 flow) — [TRM Labs](https://www.trmlabs.com/trm-tech-blog/whos-actually-paying-measuring-ai-agent-payments-onchain); [PYMNTS](https://www.pymnts.com/?p=4193315)
- Allium: agent payments doubled to 68.3M in Q3 2026 while value slipped to $3.7M (own classification) — [Cryptobriefing](https://cryptobriefing.com/base-agentic-payments-20-million-transfers/)

### Inferences
- Talent marketplaces sustain ~20% of the transaction value; a hub that only does matching + hand-off (no payroll, no escrow, no ongoing work management) offers less than Upwork/Fiverr and should expect a lower capture: plausibly 5–10% of first-year salary or a flat fee, not 20–25%.
- Both public freelance marketplaces are raising take rates on shrinking buyer bases due to AI; this is an opening for an agent-native entrant but also proof that "AI replaces the work" reduces GMV in freelance verticals. Hiring for full-time roles is less exposed to that than gig work.
- Dating monetizes via subscription (~$18–33/payer/month), not success fees (outcomes unobservable, no payer for "the marriage"). The hub needs per-vertical pricing primitives: success fee where an outcome is observable and has a payer (hiring, B2B deals), subscription where it is not (dating, networking).
- x402 per-call fees: total lifetime x402 value (~$42M) is smaller than one mid-size recruiting agency's annual revenue. Useful for anti-spam friction (charge agents fractions of a cent per post/query to raise the cost of flooding) rather than as revenue.
- Leakage defense in an agent hub: (a) make the hand-off itself the billable, logged event (both principals opt in → fee triggers before contact details are revealed); (b) keep value on-platform after hand-off (scheduling, verified credentials, offer negotiation agent, audit log); (c) charge the employer, who has contracts and legal exposure, so off-platform circumvention is a breach of terms the way agency "candidate ownership" clauses work.

### Gaps
- Did not open Upwork/Fiverr 10-Qs directly; Q3 2026 Upwork take rate is from a secondary transcript.
- No reliable public leakage rate for recruiting or freelance marketplaces specifically.
- William Blair take-rate study numbers not retrieved.
- Fiverr's current buyer/seller fee schedule (historically 20% seller commission + buyer service fee) not verified for 2026.

---

## 2. Recruiting pricing benchmarks: what would employers pay per qualified intro / hire?

### Takeaway
US employers already pay: ~20% of first-year salary per agency hire (15–25% contingency; 25–35% retained), ~$10–13k/seat/year for LinkedIn Recruiter Corporate (~$170/mo for Lite), Indeed sponsored jobs per started application/click, $4–5k/yr to ~$190k/yr for ATSs, and ~$1–4k/recruiter/yr for AI sourcing (Juicebox). A hub that delivers mutually opted-in, pre-screened candidate hand-offs sits between "sourcing tool" and "agency": a flat success fee in the low thousands to ~10% of salary, or a per-accepted-introduction fee in the low hundreds of dollars, would undercut agencies by a wide margin and still compare well to LinkedIn seats.

### Cited Findings
**Agency fees**
- Contingency fees typically 15–25% of first-year base; 20% is the most common rate in North America; 25–30% for senior/specialist roles; tiering e.g. entry 15–18%, mid 18–22%, senior 20–25% — vendor blogs, directional — [Underdog.io founder guide](https://underdog.io/blog/recruitment-agency-costs); [Paraform contingency guide](https://www.paraform.com/blog/contingency-recruiting-guide); [Top Echelon](https://topechelon.com/?p=239318); [Dover](https://www.dover.com/blog/contingency-recruiting-placement-fee-incentives)
- Retained search ~25–35% of first-year total comp, often paid in thirds (engagement/shortlist/placement); Korn Ferry executive search cited at one-third of first-year cash comp — [Kore1](https://www.kore1.com/contingency-vs-retainer-vs-engaged-search/); [Recruitly 2026 guide](https://recruitly.io/guides/recruitment-agency-fees-2026)

**Recruiter marketplaces**
- Paraform (marketplace connecting companies to independent recruiters): fee is a percentage of first-year base salary paid only on hire, reported ~20–25% (Paraform's own comparison says ~25%), plus a reported upfront listing fee per job; Paraform's own cut vs. recruiter payout not published — [Paraform for companies](https://www.paraform.com/for-companies); [HeroHunt Paraform pricing](https://www.herohunt.ai/blog/paraform-pricing-alternatives-2026/); [Dover on Paraform](https://www.dover.com/blog/paraform-reviews-pricing-alternatives); [TechCrunch 2024](https://techcrunch.com/2024/04/15/paraform-a-recruiting-platform-that-connects-recruiters-and-startups-raises-funding)
- Paraform funding: $3.6M seed, $20M Series A (June 2025, Felicis), Series B bringing total to $65M (2026) — [BusinessWire Series A](https://www.businesswire.com/news/home/20250624395231/en/In-a-Sea-of-AI-Tools-Paraform-Bets-on-People-with-$20M-Series-A); [Paraform Series B](https://paraform.com/blog/series-b)

**LinkedIn**
- Recruiter Lite ~$170/seat/month (~$1,680/yr annual); Recruiter Corporate quote-only, third-party estimates $8–15k/seat/yr, 2026 single-seat quotes cited at $10,800–$12,960/yr reflecting a reported ~15% increase on 2026 renewals; 3-seat minimum, annual auto-renew — estimates, not official — [Pin 2026](https://www.pin.com/blog/linkedin-recruiter-pricing-2026/); [Leonar: 2026 price increase](https://www.leonar.app/blog/linkedin-recruiter-price-increase-2026/); [Dover Lite vs Pro](https://dover.com/blog/linkedin-recruiter-lite-vs-professional)

**Indeed**
- Indeed ended its pay-per-application model (with 72-hour reject-without-paying) on Dec 18, 2023; Sponsored Jobs now billed Pay Per Started Application (PPSA) — employer pays when a job seeker starts an application — or per click in some markets; qualifying jobs auto-enrolled; up to 3 free job posts/month in the US; Smart Sourcing resume access ~$120/mo (~30 contacts) — [Indeed PPSA help](https://au.indeed.com/help/employers/articles/pay-per-started-application-ppsa-overview); [SHRM on pay-per-application](https://www.shrm.org/ResourcesAndTools/hr-topics/talent-acquisition/pages/indeed-shifts-pricing-to-pay-per-application.aspx); [100hires Indeed cost 2026](https://100hires.com/indeed-job-posting-cost.html)
- Third-party claim of a $25/day minimum per sponsored post (unverified; Indeed's own pages reportedly say no universal minimum) — [100hires](https://100hires.com/indeed-job-posting-cost.html)

**ATS**
- Ashby Foundations ~$400/mo monthly or ~$360/mo annual (~$4.3–4.8k/yr); upper tiers custom, can reach $120k+/yr — [Pin: Ashby pricing](https://www.pin.com/blog/ashby-pricing/)
- Greenhouse quote-only; SpendHound contract averages ~$29k/yr (SMB 50–1,000 employees) and ~$192k/yr (enterprise) — small self-reported sample — [SpendHound Juicebox/Greenhouse](https://www.spendhound.com/marketplace/juicebox-pricing)

**AI sourcing / AI recruiting tools**
- Juicebox (PeopleGPT): Starter reported $99–139/seat/month depending on date/source (July 2026 price change); AI agents add-on ~$199/agent; ATS integrations gated to Business/Enterprise; Pin estimates $3,576/yr for 1 recruiter with agents, $22,680 for 5; SpendHound avg ~$8–9k/yr — [usagepricing Juicebox price change](https://usagepricing.com/blueprint/activity/juicebox-2026-07-21-price-change); [Pin: Juicebox pricing](https://www.pin.com/blog/juicebox-pricing/); [Juicebox pricing page](https://www.juicebox.ai/pricing)
- Mercor (pivoted from AI recruiting to expert-labor marketplace for AI labs): crossed $2B annualized gross revenue run rate June 2026 (company claim), ~$614M gross H1 2026 (The Information via secondary), contractor pay is 60–70% of gross (Sacra estimate), OpenAI and Anthropic main buyers; $20B valuation talks reported July 2026 — [Dealroom](https://dealroom.co/news/137121-mercor-doubles-to-2b-gross-revenue-run-rate-as-ai-labs-buy-expert-data/); [Sacra](https://sacra.com/c/mercor/); [AI Weekly](https://aiweekly.co/alerts/mercor-books-614m-in-h1-2026-leaning-on-openai-anthropic)

### Inferences
- Reference math (US, $150k software role): agency contingency ≈ $30k per hire; Paraform ≈ $30–37.5k; one LinkedIn Corporate seat ≈ $11–13k/yr; Ashby entry ≈ $4.5k/yr; Juicebox ≈ $3.5k/recruiter/yr.
- Suggested price bands for the hub (inference, to be validated with design partners):
  - Per accepted hand-off (both principals opt in, candidate verified): ~$100–$500 for SMB/startup roles, a fraction of PPSA-plus-recruiter-time cost and far below agency fees.
  - Success fee on hire: flat $2.5–7.5k or ~5–10% of first-year base, positioning as "a quarter to half of agency cost."
  - Employer subscription (seat-free, intent-volume based): $300–1,000/mo, priced against Ashby entry/Juicebox seats.
  - Candidate side free (job-seeker agents bring supply; charging them would invite the "pay-to-apply" stigma and fairness concerns).
- Mercor's trajectory shows the largest money in "AI + talent" in 2025–26 went to supplying expert labor to AI labs rather than to classic recruiting fees; a hiring hub could add a contract/expert-work intent type as a second vertical.
- Indeed's move from pay-per-application to pay-per-started-application shows employers resisted paying for low-quality applications; a hub should bill on a stronger signal (mutual opt-in / interview scheduled), not on agent messages.

### Gaps
- Lever pricing, HeroHunt pricing and Mercor's original recruiting-era pricing not retrieved.
- No public data on employer cost per "qualified introduction" as a market price; the bands above are inferences.
- Indeed's actual average cost per started application not found from a primary source.

---

## 3. Cold start: classic marketplace case studies + agent-native distribution channels

### Takeaway
The proven playbook is: get the hardest side first in a tiny "white-hot" niche, aggregate public supply (Indeed scraped job postings; "claim your listing" onboarding converts near 100% vs cold outreach), do heavy one-on-one sales early, and subsidize supply if needed. Agent-native distribution (MCP Registry, ChatGPT plugin/app directory, ClawHub) is now large in listings (tens of thousands of MCP registry records; ~1,600+ ChatGPT apps) but listing ≠ distribution: no reliable evidence that a directory listing alone drives meaningful usage, and open skill marketplaces have serious malware problems that make trust/verification a selling point.

### Cited Findings
**Classic marketplace seeding**
- NFX "19 tactics": get the hardest side first by finding the small groups that care most ("white-hot center"); Indeed, Yelp and Goodreads aggregated supply data (job postings, businesses, books) before having activity, noting these tactics carried risk — [NFX 19 marketplace tactics](https://www.nfx.com/post/19-marketplace-tactics-for-overcoming-the-chicken-or-egg-problem)
- Lenny Rachitsky's research on how marketplaces got first users: one-on-one direct sales was the crucial lever for a large share of early marketplaces, about twice as common as the next lever (piggy-backing and referrals) — [Lenny's Newsletter](https://www.lennysnewsletter.com/i/176567/one-of-the-most-significant-learnings-and-surprises-for-me-in-doing-this-research-was-how-important-one-on-one-direct-sales-was-to-most-early-marketplaces-sales-ended-up-being-a-crucial-lever-for-about-of-the-companies-i-talked-to-twice-as-common-as-the-next-biggest-lever-piggy-backing-and-referrals)
- "Claim your listing" offer to pre-seeded suppliers yields onboarding success near 100% vs much lower cold outreach (VC claim) — [Antler](https://www.antler.co/blog/how-to-grow-marketplace-supply-fast)
- Lyft used guaranteed hourly earnings floors to subsidize early drivers; Sharetribe warns growing both sides at once early is a common mistake — [Antler](https://www.antler.co/blog/how-to-grow-marketplace-supply-fast); [Sharetribe supply guide](https://www.sharetribe.com/academy/how-to-build-supply-marketplace/); [Version One: how to seed your marketplace](https://versionone.vc/how-to-seed-your-marketplace)
- Paraform seeded by aggregating independent recruiters (supply) for startups (demand), monetizing employer listings + success fees — [TechCrunch 2024](https://techcrunch.com/2024/04/15/paraform-a-recruiting-platform-that-connects-recruiters-and-startups-raises-funding)
- Boardy (AI "superconnector"): voice AI that calls users (~30-min conversations) and brokers warm intros; $3M pre-seed (Oct 2024, HF0) and $8M seed (Jan 2025, Creandum); launch weekend produced "thousands of intros"; investor claims >$10M venture investment facilitated; business model not publicly described, reportedly shifted toward co-founder matching and a founders fundraising program — [TechCrunch](https://techcrunch.com/2024/10/24/ai-networking-startup-boardy-raises-3m-pre-seed/?rand=23331); [Creandum](https://creandum.com/stories/backing-boardy-ai); [The Logic](https://thelogic.co/briefing/boardy-ai-raises-us8m-seed-round-for-ai-networking-tool/)

**Agent-native distribution**
- Official MCP Registry: no single official count; an Oct 28, 2026 API query returned 52,042 server records; Oct 4 snapshot 39,238 (+45% in 30 days); API Tracker counted 53,075 records on Nov 1, 2026 and warns a record ≠ a unique product/deployment/user; a May 2026 tracker put the curated official registry at ~2,000 — community trackers, not official — [DEV: MCP Registry by the numbers](https://dev.to/amareswer/the-mcp-registry-by-the-numbers-38nc); [API Tracker Nov 1 2026](https://apitracker.io/mcp-statistics/2026-11-01); [Digital Applied tracker](https://www.digitalapplied.com/blog/mcp-server-ecosystem-tracker-50-servers-cataloged-2026)
- Claim of ~10k MCP servers and 97M monthly SDK downloads by May 2026 (unverified secondary) — [DEV/gentic_news](https://dev.to/gentic_news/mcp-hits-10k-servers-97m-monthly-sdk-downloads-by-may-2026-1jbk); "one upstream (the official registry) won" among registries by mid-2026 — [Towards AI](https://pub.towardsai.net/mcp-registries-in-mid-2026-one-upstream-won-2ce541b92036)
- ChatGPT: OpenAI opened app submissions (Apps SDK, MCP-based) with an in-ChatGPT directory; submissions include MCP connectivity details, testing guidelines, directory metadata, country availability; directory reportedly renamed/merged into a "Plugins" directory (July 2026) covering apps, skills and MCP servers; community list counted 1,624 apps as of July 2, 2026 — [OpenAI: developers can now submit apps](https://openai.com/index/developers-can-now-submit-apps-to-chatgpt/); [VentureBeat](https://venturebeat.com/technology/openai-now-accepting-chatgpt-app-submissions-from-third-party-devs-launches); [awesome-chatgpt-apps](https://awesome.ecosyste.ms/projects/github.com%2Frdmgator12%2Fawesome-chatgpt-apps)
- OpenClaw / ClawHub: Koi Security audited all 2,857 ClawHub skills and found 341 malicious (335 from one "ClawHavoc" campaign); Snyk found one publisher with 300+ malicious packages ~7,000 downloads, a malicious "clawhub" skill with 7,743 downloads; Bitdefender ~17% of skills analyzed early were malicious; ClawHub added VirusTotal/ClawScan screening, yet Unit 42 later found 5 skills evading checks — [The Hacker News](https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html); [Snyk](https://snyk.io/articles/clawdhub-malicious-campaign-ai-agent-skills/); [Unit 42](https://unit42.paloaltonetworks.com/openclaw-ai-supply-chain-risk/); [Dark Reading](https://www.darkreading.com/cyber-risk/malicious-openclaw-skills-clawhub-threaten-ai-supply-chain)

### Inferences
- Indeed's aggregation precedent supports seeding the employer side from public job postings / ATS public job-board feeds as "unclaimed" intents, then using "claim your agent/listing" outreach (the highest-converting tactic cited). Legal/ToS risk must be checked per source (NFX itself notes the risk).
- Hardest side in agent-hiring is likely the employer (budget holder, skeptical of AI-flooded inbound); job seekers with agents are abundant (see section 4). Get 10–30 design-partner employers in one niche via direct sales, then open candidate-agent intake.
- With ~50k MCP registry records and ~1.6k ChatGPT apps, a listing is table stakes, not a growth channel; distribution must come from a strong reason for an assistant user to invoke the hub ("find me a job" / "find candidates") and from partnerships with agent builders (job-seeker agent startups, ATS vendors) who route traffic in.
- ClawHub's malware record is a market signal: an agent hub that verifies agents (KYB for employers, identity for candidates) and sandboxes agent-submitted content can sell trust as a feature and justify verification fees.

### Gaps
- No public usage/install data for individual MCP servers or ChatGPT apps showing that directory placement drives adoption; no data on Claude connector directory reach or listing criteria (not found in searches).
- Airbnb (Craigslist cross-posting), Upwork (oDesk/Elance merger), Wellfound/AngelList, Hired and Triplebyte supply-seeding specifics were not retrieved from primary sources in this pass.
- ClawHub total size/downloads in Nov 2026 not found.

---

## 4. Demand and willingness to pay: consumer delegation, employer sentiment, recruiter/job-seeker pain

### Takeaway
Hiring pain is severe and quantified: applications per job roughly doubled 2022→2025 (116→244 on Greenhouse) while recruiters per org fell by more than half, driven partly by AI auto-apply; trust is low on both sides (only 8% of job seekers say AI screening is fairer; 74% of hiring managers more worried about fraud). Consumers are willing to let agents research and do bounded, reversible actions but far fewer trust them to complete high-stakes actions autonomously, which supports a design where agents negotiate and humans approve the hand-off.

### Cited Findings
**Recruiter pain**
- Greenhouse Hire Standard (6,000+ companies, 640M applications): 116 applications per job in 2022 → 244 in 2025 (+111%); recruiters per organization fell from 10.43 to 4.62 — vendor platform data — [Greenhouse recruiting benchmarks](https://www.greenhouse.com/recruiting-benchmarks)
- Greenhouse customers averaged 222 applications per opening in Q1 2024, almost 3x end-2021; candidates using AI submit 41% more applications — [Greenhouse blog](https://www.greenhouse.com/blog/ai-has-doubled-recruiters-workloads)
- Nine in ten employers believe they've turned away real candidates as AI floods applications — [Greenhouse newsroom](https://www.greenhouse.com/newsroom/nine-in-ten-employers-believe-theyve-turned-away-real-candidates-as-ai-floods-job-applications)
- LinkedIn applications up 45% YoY, attributed in part to candidates paying for auto-apply AI agents — [Stacker: bot applicant](https://stacker.com/stories/careers-education/bot-applicant-how-ai-breaking-modern-job-search)

**Trust / fairness**
- Greenhouse 2025 AI in Hiring Report (4,136 respondents US/UK/IE/DE): 70% of hiring managers trust AI to make faster, better hiring decisions; only 8% of job seekers say AI screening makes hiring fairer; 74% of hiring managers fear fraud more than a year earlier; 41% of US job seekers admitted using prompt injections to get past AI screeners — [Greenhouse newsroom](https://www.greenhouse.com/newsroom/an-ai-trust-crisis-70-of-hiring-managers-trust-ai-to-make-faster-and-better-hiring-decisions-only-8-of-job-seekers-call-it-fair); [Fortune](https://fortune.com/2025/11/18/hiring-job-seekers-recruiters-talent-acquisition-ai-doom-loop-application-technology/)

**Job-seeker pain**
- Clutch (590 job seekers): 93% worry AI-generated resumes/cover letters make it harder to stand out; 86% say AI let them increase applications per week — [Clutch state of AI hiring](https://clutch.co/resources/state-ai-hiring)
- 77% of US job seekers used AI in their search in the past year; 60% changed or considered changing writing to avoid looking AI-generated; >80% experienced rejection without speaking to an interviewer — [Black Enterprise (Greenhouse data)](https://www.blackenterprise.com/?p=1202117)
- 34% of US/UK workers say AI made them less confident competing for jobs — [Staffing Industry Analysts (Indeed Flex)](https://www.staffingindustry.com/news/global-daily-news/majority-of-us-and-uk-workers-believe-ai-is-reducing-entry-level-hiring)

**Consumer willingness to delegate to agents (mostly commerce; industry-sponsored surveys, not comparable)**
- Accenture (Jan 2026, 25,000+ consumers, 16 countries): 32% willing to let an agent make the final purchase decision within set limits; 9% would let an agent shop fully autonomously — [Chain Store Age (Accenture)](https://chainstoreage.com/accenture-customers-trust-ai-agents-perform-these-tasks-them)
- Deloitte (4,000 US, Aug–Sep 2025): 16% trust AI agents to complete purchases — [Chain Store Age](https://chainstoreage.com/survey-some-skepticism-remains-among-ai-shopping-agent-users)
- Horizon Media (Mar 2026): 70% comfortable with AI deal-hunting, 33% with AI completing a purchase; 76% say shopping agents should work for them but only 27% believe they do — [PYMNTS](https://www.pymnts.com/artificial-intelligence-2/2026/70-percent-of-consumers-say-yes-to-ai-agents-for-shopping/)
- YouGov (1,000 US): 42% likely to let AI purchase on their behalf; 81% of likely adopters uncomfortable with >$100 spend without authorization — [ConsumerAffairs](https://www.consumeraffairs.com/news/survey-shows-most-americans-would-trust-ai-to-shop-for-them-081326.html); [YouGov](https://yougov.com/en-us/articles/53060-reality-checks-talkshow-agentic-ai-shopping-agents-michael-nevski)
- Croud (2,000+ US): 69% open to AI making routine purchases without approving each transaction — [Chain Store Age](https://chainstoreage.com/survey-consumers-would-let-ai-agents-spend-them-these-categories)
- Synchrony (May 2026, 2,000 US): consumers open to delegation only when protected, in control and able to approve the final decision — [Synchrony AI in commerce study](https://www.synchrony.com/AI-in-commerce-study)

### Inferences
- The employer's willingness to pay is driven by noise reduction: a hub that guarantees each hand-off is (a) verified human, (b) mutually interested, (c) pre-qualified against must-haves is selling the opposite of auto-apply spam. Pricing should be per outcome (accepted hand-off / hire), which matches the pain metric (applications per hire).
- Consumer surveys show the "human approves the final step" pattern is what users want; the hub's hand-off-to-human design matches this and should be marketed as such (agents explore, humans commit).
- Employer adoption risk: employers already see candidate AI as a fraud/noise problem; the hub must position candidate agents as verified and rate-limited, otherwise employers will block them as they block auto-apply bots.

### Gaps
- No survey found that directly measures employer sentiment toward candidates' AI agents negotiating on their behalf (only toward AI-generated applications/auto-apply).
- No survey on consumer willingness to let agents act for them in dating or job negotiation specifically.
- No data on job seekers' willingness to pay for agent representation (auto-apply tool pricing not retrieved).

---

## 5. Lessons from failed/struggling matching marketplaces and agent-economy hype

### Takeaway
Curated "reverse" tech-hiring marketplaces (Hired, Vettery, Triplebyte) raised large sums but ended in fire-sales or shutdowns, consistent with thin, cyclical employer demand, leakage after intros, and loss of curation quality when chasing scale. Token-incentivized agent marketplaces (Virtuals, Fetch.ai) show activity that collapses once speculative incentives fade, and their token prices decoupled from real use. The hub should avoid tokens, keep curation/verification as the product, and diversify beyond tech hiring cycles.

### Cited Findings
- Hired: reported winding down and selling assets in late 2020; acquired by Vettery (Adecco) Nov 2020, terms undisclosed; combined products rebranded as Hired in March 2021; Hired folded into LHH Recruitment Solutions (Adecco) as of June 14, 2024 — [TechCrunch 2020](https://techcrunch.com/2020/11/23/vettery-acquires-hired/); [Recruiting News Network "deeply troubled Hired"](https://www.recruitingnewsnetwork.com/posts/youre-not-hired-vettery-acquires-a-deeply-troubled-hired); [Hired company update](https://hired.com/blog/employers/company-update-hired-lhh-recruitment-solutions/); [Staffing Industry Analysts 2024](https://www.staffingindustry.com/news/global-daily-news/adecco-incorporating-hired-lhh-business)
- Underdog.io frames Vettery+Hired as a "$150M mirage" (could not fetch; network-blocked) — [Underdog.io](https://underdog.io/blog/the-rise-and-fall-of-vettery-and-hired)
- Triplebyte raised nearly $50M; in March 2023 Karat acquired its assessment technology and team, while Triplebyte's candidate profiles and sourcing marketplace were shut down rather than transferred — [Karat TB candidates page](https://connect.karat.com/tb-candidates); [Citybiz on Karat acquisition](https://www.citybiz.co/article/393235/karat-acquires-leading-adaptive-assessment-technology-from-triplebyte/)
- Opinion analyses (not company statements): Triplebyte declined after abandoning its rigorous curated model for a scalable database approach; its Screen product attracted the wrong candidate demographics — [Dealroom note "venture scale destroys product"](https://app.dealroom.co/news/note/triplebyte-venture-scale-destroys-product); [dead-startups archive](https://dead-startups-neon.vercel.app/companies/triplebyte)
- Blind users in 2024 lamented Hired's decline and asked for "another Hired.com" (anecdotal demand signal for curated reverse marketplaces) — [Blind](https://www.teamblind.com/post/can-someone-please-go-build-another-hiredcom-2ojqzrey)
- Virtuals Protocol: daily revenue fell from $1.02M peak (early Jan 2025) to ~$34.8k by late Feb 2025 per its Dune dashboard; daily active trading wallets down >10x (58,641 → 5,585); new agent launches near zero for stretches; reports of revenue ~$500/day with token −90% — [Decrypt](https://decrypt.co/309495/virtuals-protocol-revenue-crashes-ai-agent-demand-sinks); [Forklog](https://forklog.com/en/virtuals-ai-platform-revenue-plummets-seventyfold/); [Cointelegraph](https://cointelegraph.com/news/new-ai-agent-launches-virtuals-plummet-token-drawdowns); [CoinGlass](https://www.coinglass.com/news/442676)
- AI-agent token market cap ~$2.92B vs >$10B peak in late 2025; FET fell 56% in one month in early 2026 even as Fetch.ai claimed 35M mainnet txs and 2.5M "active agents" on Agentverse (promotional figures) — [BlockEden](https://blockeden.xyz/blog/2026/03/27/agent-winter-paradox-ai-token-crash-production-adoption-soars/); [KuCoin](https://www.kucoin.com/news/flash/fet-price-drops-56-in-one-month-amid-fetch-ai-s-network-growth-in-2026)
- Analysts attribute the agent-token decline to unproven utility, token oversupply and low liquidity; BlockEden argues agents do not need to hold VIRTUAL/FET to function (usage decoupled from token value) — [Cointelegraph](https://cointelegraph.com/news/ai-agents-virtual-revenue-plunge-token-price-decline); [BlockEden](https://blockeden.xyz/blog/2026/03/27/agent-winter-paradox-ai-token-crash-production-adoption-soars/)

### Inferences
- Hired/Vettery/Triplebyte were all single-vertical (tech) and employer-paid; they were exposed to tech hiring downturns. A general protocol with multiple intent types reduces that exposure, but GTM should still be single-niche.
- Triplebyte's lesson (per opinion sources): curation/verification quality was the product; scaling by loosening it killed value. For an agent hub, the equivalent is not letting unverified agents flood intents.
- Token-incentivized agent activity is not demand. "Active agents" and transaction counts are easily inflated; the hub should report human-outcome metrics (hand-offs accepted, interviews, hires) to investors and users.

### Gaps
- Hired's and Vettery's actual pricing (Hired historically charged employers ~15% placement fees or subscriptions per training knowledge — not verified in this pass) and peak metrics not retrieved; underdog.io blocked in this session's network.
- Wellfound (AngelList Talent) business model and current metrics not retrieved.
- No Nov 2026 snapshot of Virtuals/Fetch.ai activity.

---

## 6. Unit economics and metrics that matter (liquidity, match rate, time-to-match)

### Takeaway
The standard marketplace health metrics are fill/match rate, market depth, time-to-match, take rate and repeat use; for an agent hub the decisive ones are hand-off acceptance rate and hand-off → hire conversion, measured per intent type and per niche. Public benchmarks for hiring-specific liquidity are scarce; the best proxies are Greenhouse's applications-per-job and recruiter-load data and the payer/RPP and take-rate figures of public marketplaces.

### Cited Findings
- a16z defines liquidity via fill rate (aka match rate/utilization), market depth and time to find a match — [a16z marketplace glossary (via mirror)](https://bjpcjp.github.io/2024/03/24/a16z-glossary.html); [a16z](https://a16z.com/?p=17518)
- Liquidity = probability that providers sell what they offer and customers find what they're looking for — [Sharetribe glossary](https://www.sharetribe.com/academy/marketplace-glossary/)
- Retention/repeat-use metrics guidance for marketplaces — [Amplitude](https://amplitude.com/blog/how-to-grow-marketplace-retention)
- Benchmarks available from public talent/dating marketplaces: Upwork take rate ~20% with active clients −4% YoY (763k); Fiverr take rate 28.2% with active buyers −27% YoY (2.4M) and spend per buyer $373; Match revenue per payer $21.19/month — see section 1 sources ([Nasdaq](https://www.nasdaq.com/articles/upwork-q2-earnings-call-highlights); [Fiverr Q3](https://www.morningstar.com/news/globe-newswire/9855650/fiverr-announces-third-quarter-2026-results); [Securities.io](https://www.securities.io/payers-fall-5-at-match-group-as-q3-revenue-slips-to-891-million/))
- Hiring workload baselines: 244 applications per job (2025) and 4.62 recruiters per org on Greenhouse — [Greenhouse](https://www.greenhouse.com/recruiting-benchmarks)

### Inferences
- Proposed metric tree for the hub (inference):
  - Liquidity: % of active intents that get ≥1 mutually accepted hand-off within 7/14/30 days (per niche); median time-to-first-qualified-match.
  - Quality: hand-off acceptance rate by human principals (both sides); hand-off → interview; interview → hire; employer-reported "qualified" rate; spam/abuse rate; verified-agent share.
  - Economics: revenue per hire (success fee) and per accepted hand-off; CAC by channel (MCP directory vs partner agent vs direct sales); employer repeat-posting rate; leakage proxy (hand-offs with no recorded outcome after 60 days vs. surveyed outcome).
- Illustrative unit economics (inference, assumptions explicit): if an employer posts 10 roles/yr, the hub fills 3 at a $5k flat fee = $15k/yr revenue per employer, about the cost of one LinkedIn Corporate seat and half of one agency fee; if hand-offs-per-hire is ~8 and the hub charges $200/hand-off instead, revenue per hire ≈ $1.6k. Target: serving cost per hand-off (LLM negotiation + verification) well under $20, so gross margin stays SaaS-like.
- A useful "noise" KPI to sell to employers: hand-offs per hire vs their baseline applications per hire (~244 applications per job on Greenhouse).

### Gaps
- No public benchmark for match rate / time-to-match in recruiting marketplaces (Hired/Paraform did not publish); no data on typical hand-offs (or intros) per hire for intro-based models.
- No reliable data on LLM cost per agent negotiation session at scale (depends on model; not researched here).
- Lenny Rachitsky's marketplace liquidity/retention benchmark tables were not retrieved in detail.
