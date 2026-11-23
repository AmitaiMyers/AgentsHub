# Technical foundations for an agent-to-agent matchmaking hub (as of 22 Nov 2026)

Method note: web search worked in this session, but direct fetches of a2a-protocol.org, aaif.io and genai.owasp.org were blocked by the session's network allowlist. Primary-source detail for A2A and MCP therefore comes from the projects' public GitHub repos (fetched as raw files): the A2A CHANGELOG, `docs/whats-new-v1.md`, `docs/specification.md`, `docs/topics/agent-discovery.md` and `docs/roadmap.md`, plus the MCP `2026-07-28` release blog post. Everything else comes from search-result snippets and secondary coverage, and is flagged where it is unverified. This goes deeper than §4 of `/home/user/AgentsHub/research/REPORT.md`, which these notes extend and in a few places correct.

## A2A protocol: version, dates, governance, and the spec details that matter for a hub

### Takeaway
A2A v1.0.0 was released on **12 March 2026**. The "January 2026" date refers to a release candidate, not the stable release. The current stable version is **v1.0.1 (26 May 2026)**, and **v1.1** is in progress. A2A gives the hub everything it needs to talk to other agents: signed Agent Cards, eight task states including `INPUT_REQUIRED` and `AUTH_REQUIRED`, SSE streaming, webhook push, multi-tenancy, and OAuth/OIDC/mTLS schemes. It deliberately does **not** define a registry API, so the hub's discovery and matching layer is not covered by any standard. A2A moved under the Agentic AI Foundation (AAIF) in **August 2026**; the exact day is unconfirmed.

### Cited Findings
**Versions and dates**
- The official changelog lists `1.0.0 (2026-03-12)` and `1.0.1 (2026-05-26)`. The previous version was `0.3.0 (2025-07-30)`. — [A2A CHANGELOG](https://github.com/a2aproject/A2A/blob/main/CHANGELOG.md)
- Secondary sources resolve the Jan/Mar conflict: a v1.0 release candidate appeared on 29 Jan 2026, and one academic paper dates "v1.0.0" to January 2026, which likely conflates the RC with the stable release. One source also says v1.1 is at release-candidate stage. — [A2A announcing 1.0 (search snippet)](https://a2a-protocol.org/latest/announcing-1.0/); [DEV: A2A v1.0.0 is live](https://dev.to/peytongreen_dev/a2a-v100-is-live-what-changed-and-what-it-means-for-your-python-agents-242a); [Wikipedia: Agent2Agent](https://en.wikipedia.org/wiki/Agent2Agent)
- The roadmap was last updated on 15 Sep 2026. Its near-term items are v1.1 (task timeline, event filtering), **bidirectional streaming**, an A2A CLI for coding harnesses, and **"Elicitation & Multi-Turn Workflows … structured human-in-the-loop interaction models and multi-round negotiation patterns"** (PR #2149, issue #2143). It lists SDKs in Python, Go, JS, Java, .NET and Rust, plus the A2A Inspector and a Technology Compatibility Kit (TCK). — [A2A roadmap](https://github.com/a2aproject/A2A/blob/main/docs/roadmap.md)

**Governance**
- Google donated A2A to the Linux Foundation in June 2025. AAIF, a directed fund of the Linux Foundation, launched in Dec 2025 to host MCP and related projects. A2A became an AAIF-hosted project in **August 2026**; reports give 17, 17–18 and 20 Aug. A2A and MCP keep separate technical steering committees. — [Forkast](https://forkast.news/googles-a2a-protocol-joins-aaif-consolidating-the-agent-economys-protocol-layer-under-one-roof/); [a2awire](https://a2awire.com/news/google-a2a-protocol-joins-agentic-ai-foundation-2026/); [super-agentic.ai](https://super-agentic.ai/resources/super-posts/a2a-earned-its-seat-at-aaif). These are secondary or niche sources; the primary AAIF announcement could not be fetched.

**Agent Card and discovery**
- The well-known URI is `https://{server_domain}/.well-known/agent-card.json`. The spec lists three discovery mechanisms: the well-known URI, "Registries/Catalogs" and direct configuration. — [A2A spec §8.2](https://github.com/a2aproject/A2A/blob/main/docs/specification.md)
- **Registry gap:** "The current A2A specification does not prescribe a standard API for curated registries." Registries may do "Selective Disclosure", returning different cards depending on the caller's identity. The community "explores standardizing registry interactions." — [A2A Agent Discovery guide](https://github.com/a2aproject/A2A/blob/main/docs/topics/agent-discovery.md)
- Breaking changes to the v1.0 card:
  - `url`, `preferredTransport` and `additionalInterfaces` are replaced by `supportedInterfaces[]`, where each entry has `url`, `protocolBinding` (JSONRPC, gRPC or HTTP+JSON) and `protocolVersion`. The first entry is the preferred one.
  - `protocolVersion` moved off the card and onto each interface.
  - `supportsAuthenticatedExtendedCard` became `capabilities.extendedAgentCard`, and the method was renamed `GetExtendedAgentCard`.

  — [What's new in v1](https://github.com/a2aproject/A2A/blob/main/docs/whats-new-v1.md)
- **Signed cards:** a card "MAY" be signed with JWS (RFC 7515). Before signing, it must be canonicalized with JCS (RFC 8785), with protobuf field-presence rules applied and the `signatures` field excluded. Detached signatures are supported, with keys fetched via `jku` or from trusted keystores. — [A2A spec §8.4](https://github.com/a2aproject/A2A/blob/main/docs/specification.md); [What's new in v1](https://github.com/a2aproject/A2A/blob/main/docs/whats-new-v1.md)
- A signed card "does not make an agent trustworthy, and a tenant field does not authorize itself." — [API7.ai](https://api7.ai/blog/a2a-protocol-gateway-layer)

**Tasks, messages and streaming**
- The valid task states are `TASK_STATE_SUBMITTED`, `WORKING`, `COMPLETED`, `FAILED`, `CANCELED`, `REJECTED`, `INPUT_REQUIRED` and `AUTH_REQUIRED`. Of these, `COMPLETED`, `FAILED`, `CANCELED` and `REJECTED` are terminal, and sending a message to a terminal task returns `UnsupportedOperationError`. — [A2A spec](https://github.com/a2aproject/A2A/blob/main/docs/specification.md)
- `AUTH_REQUIRED` lets an agent hand an authorization step back to its client, and the hand-back can be chained upstream through a series of agents. The spec says agents "MUST NOT treat the `TASK_STATE_AUTH_REQUIRED` state transition, by itself, as authorization." — [A2A spec §7.6](https://github.com/a2aproject/A2A/blob/main/docs/specification.md)
- v1.0 renamed the operations: `SendMessage`, `SendStreamingMessage` (SSE), `GetTask`, `ListTasks` (new, with filtering and pagination), `CancelTask` and `SubscribeToTask` (formerly `tasks/resubscribe`; multiple concurrent subscriptions are allowed, and the stream closes when the task reaches a terminal state). `SendMessage` can block until a terminal state or return immediately (`return_immediately: true`). — [What's new in v1](https://github.com/a2aproject/A2A/blob/main/docs/whats-new-v1.md); [spec](https://github.com/a2aproject/A2A/blob/main/docs/specification.md)
- The core objects are Task, TaskStatus, Message, Role, Part and Artifact. Push notifications are delivered by HTTP POST to webhooks the client registers, using the `Create/Get/List/DeleteTaskPushNotificationConfig` operations, and push payloads use the StreamResponse format. — [spec §3.5.3, §4.1, §4.3](https://github.com/a2aproject/A2A/blob/main/docs/specification.md)
- **Multi-tenancy is new in v1.0:** a `tenant` field appears on every request and on `AgentInterface`, "enables to serve multiple agents from a single endpoint". — [What's new in v1](https://github.com/a2aproject/A2A/blob/main/docs/whats-new-v1.md)
- Timestamps must be ISO 8601 UTC with millisecond precision. Errors use `google.rpc.Status`/`ErrorInfo`, which replaces RFC 9457. — [What's new in v1](https://github.com/a2aproject/A2A/blob/main/docs/whats-new-v1.md)

**Authentication**
- The supported security schemes are APIKey, HTTPAuth, OAuth2, OpenIdConnect and **MutualTls**. — [spec §4.5](https://github.com/a2aproject/A2A/blob/main/docs/specification.md)
- v1.0 removed the OAuth Implicit and Password flows and added the Device Code flow (RFC 8628) and a `pkceRequired` flag on Authorization Code. — [What's new in v1](https://github.com/a2aproject/A2A/blob/main/docs/whats-new-v1.md)
- The spec describes A2A and MCP as "complementary, not competing": MCP connects agents to tools and resources, and A2A coordinates agents with each other. — [What's new in v1](https://github.com/a2aproject/A2A/blob/main/docs/whats-new-v1.md)

**Adoption**
- "150+ organizations" is widely repeated, but only in secondary sources. — [Stellagent](https://stellagent.ai/insights/a2a-protocol-google-agent-to-agent)

### Inferences
- The hub can present itself as **one multi-tenant A2A endpoint**: a `tenant` per listed agent or per negotiation room, with each listed agent getting its own Agent Card served under the hub's domain. That matches v1.0's multi-tenancy design.
- Each negotiation maps naturally onto one A2A **Task**:
  - `INPUT_REQUIRED` means the agent is waiting for its human.
  - `AUTH_REQUIRED` means consent to reveal personal data is needed.
  - `REJECTED` means a decline.
  - `COMPLETED` carries a hand-off Artifact.
- Matches can take days, so the hub should rely on push webhooks rather than held-open SSE streams.
- Because A2A defines no registry API, the hub's search and match API will be proprietary (or ARD-based; see the discovery section). This is where the hub can differentiate, and it carries no risk of clashing with the standard.
- Watch the v1.1 "multi-round negotiation patterns" work (#2143/#2149). If it standardizes offer and counter-offer messages, the hub's negotiation state machine should line up with it.

### Gaps
- The exact AAIF date for A2A and the primary press release were not retrieved, because aaif.io and linuxfoundation.org could not be fetched.
- The v1.1 release date, and whether it has shipped by Nov 2026, are unconfirmed; only one secondary source says it is at RC.
- The "150+ orgs" adoption figure is unverified.

## MCP: current spec, remote servers and OAuth, registry status, exposing the hub as an MCP server, and MCP vs A2A

### Takeaway
The current MCP spec is **2026-07-28**, released 28 Jul 2026. Its core is now **stateless**: no `initialize` handshake and no `Mcp-Session-Id`. It adds header-based routing, Multi Round-Trip Requests (MRTR) for elicitation, tasks as an extension, hardened OAuth (RFC 9207 issuer checks, and DCR deprecated in favor of client ID metadata documents, CIMD), and a 12-month deprecation policy. The official MCP Registry is very large, at about 55–65k entries in Nov 2026, but **GA is unconfirmed** and many entries cannot be validated. For a hub, MCP is the **distribution channel**, the way users' assistants reach it. A2A is the **interoperability channel** for autonomous or custom agents.

### Cited Findings
- **2026-07-28 release:** the spec went live on 28 Jul 2026 with Tier 1 SDKs in TypeScript, Python, Go and C#, and Rust in beta. The SDKs see close to half a billion downloads a month. — [MCP blog, 2026-07-28 spec](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/blog/content/posts/2026-07-28-spec-ga/index.md)
  - The `initialize`/`initialized` exchange and the `Mcp-Session-Id` header are retired (SEP-2575, SEP-2567). Every request carries its own protocol version, client info and capabilities, and the change is pitched as letting "any request … land on any instance behind a plain round-robin load balancer."
  - For state across calls, the blog says to "mint an explicit handle from a tool and have the model pass it back as an argument."
  - Requests must carry `Mcp-Method` and `Mcp-Name` HTTP headers (SEP-2243), so gateways and WAFs can route, rate-limit and authorize on headers.
  - **MRTR** (SEP-2322) replaces server-initiated `elicitation/create`, `sampling/createMessage` and `roots/list`. The server returns `resultType: "input_required"` and the client retries with the answers.
  - List results carry `ttlMs` and `cacheScope` and come back in a deterministic order.
  - Authorization changes: clients must validate `iss` per RFC 9207 (SEP-2468), credentials are bound to their issuer (SEP-2352), **Dynamic Client Registration is deprecated in favor of Client ID Metadata Documents (CIMD)**, and `application_type` is used for localhost redirects.
  - Tasks moved into the `io.modelcontextprotocol/tasks` extension, with a poll-based `tasks/get` and a new `tasks/update` (SEP-2663). Notifications move to a single opt-in `subscriptions/listen` stream.
  - The formal extensions framework covers Tasks, **MCP Apps** and Enterprise Managed Authorization (EMA).
  - Roots, Sampling and Logging are deprecated (SEP-2577), as is the legacy HTTP+SSE transport, each with at least 12 months' notice.
- The 2025-11-25 spec is now marked Final. Secondary sources disagree on when the 2026-07-28 release candidate appeared (21 May vs 29 May 2026). — [search summary of hidekazu-konishi timeline](https://hidekazu-konishi.com/entry/mcp_specification_version_timeline.html); [AAIF blog (snippet)](https://aaif.io/blog/mcp-2026-07-28-whats-changing-and-how-to-migrate)
- **Registry:** it launched in preview on 8 Sep 2025. Third-party counts for Nov 2026:
  - 55,934 active entries on 5 Nov ([DEV](https://dev.to/akshay_bhanderi/we-checked-55934-mcp-registry-entries-heres-what-we-found-539p))
  - 62,678 active and 64,935 listed on 15 Nov ([DEV, by the numbers](https://dev.to/amareswer/the-mcp-registry-by-the-numbers-38nc); [digitalapplied](https://www.digitalapplied.com/blog/mcp-adoption-statistics-2026-model-context-protocol))

  New servers per month rose from 1,894 in March 2026 to 11,809 in September. 71.2% of net-new entries "can't be checked", mostly remote-only servers. As of Oct 2026 one source still described the registry as preview, and no official GA announcement was found. — same sources (secondary; treat as approximate)
- **ChatGPT:** app submissions opened in Dec 2025. Submissions require MCP connection details, testing guidelines, directory metadata and country availability. The Apps SDK "extends the Model Context Protocol." **The guidelines will not approve plugins "that primarily function as unofficial connectors to third-party services, including pass-through intermediary software layers"**, which is a listing-policy risk for a hub that brokers between other people's agents and should be read carefully. — [OpenAI: developers can now submit apps](https://openai.com/index/developers-can-now-submit-apps-to-chatgpt/); [Apps SDK submission guidelines](https://developers.openai.com/apps-sdk/app-submission-guidelines)
- **Claude:** remote MCP servers can be submitted to the Claude connectors directory through a review form. The only source is a single forum comment, not official documentation. — [OpenAI community thread (snippet)](https://community.openai.com/t/application-for-connector-list/1358290)
- **Cloudflare** says its Agents SDK supports 2026-07-28 "from day zero", so MCP servers can run in Workers. **AWS Bedrock AgentCore** supports the stateless core. — [MCP blog quotes](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/blog/content/posts/2026-07-28-spec-ga/index.md)

### Inferences
- **Build the hub's MCP server against 2026-07-28.** It is stateless, so it can run on serverless or edge infrastructure.
  - Use explicit `session_id` and `intent_id` handles as tool arguments, which is the pattern the spec recommends.
  - Use MRTR elicitation for human approval points, such as "reveal my CV to employer X?". This fits progressive disclosure well.
  - Use the Tasks extension for long-running match searches.
  - Use OAuth 2.1 with CIMD, not DCR.
  - Keep MCP Apps optional, for a rich match card or comparison UI inside ChatGPT or Claude.
- **MCP vs A2A for this use case:**
  - Most end users' agents (Claude, ChatGPT) are *clients* that cannot host an A2A server. They can only call tools, so MCP is the only practical way in for them.
  - Autonomous or company-run agents (an employer's ATS bot, a custom candidate agent) can be reached over A2A, either via the hub's A2A endpoint or directly after the match.
  - So: **MCP in for consumer assistants, A2A for server-side agents, one shared internal negotiation state machine.**
- The ChatGPT "pass-through intermediary" exclusion suggests positioning the hub as a first-party service with its own matching logic and data, not as a relay. This is a product and legal question to verify with OpenAI.

### Gaps
- An official MCP Registry GA date was not found. Neither the registry API version nor its namespace-verification rules were retrieved.
- Official docs for Claude's connector directory submission process and OpenClaw's MCP and skills support (ClawHub) were not retrieved in this session.
- The full 2026-07-28 changelog, including any change to the `.well-known` OAuth protected-resource metadata, was not read.

## Discovery and identity: AGNTCY ADS, NANDA Index, ANS, DNS-AID, Web Bot Auth, Skyfire KYA, Visa TAP, Entra Agent ID, VCs/DIDs

### Takeaway
None of the open discovery systems is a production-grade public standard yet:
- **ANS** became a Linux Foundation project on 10 Nov 2026, but its specs are still labeled drafts.
- **DNS-AID** is an individual IETF draft that no working group has adopted.
- **AGNTCY ADS** has an IETF individual draft and working open-source code.
- **NANDA Index** is still a research effort.

The most deployable identity pieces are **Web Bot Auth** (HTTP Message Signatures; IETF WG draft adopted 1 Sep 2026 and already shipped by Cloudflare and others), **Skyfire KYAPay** (production JWTs) and, for enterprise tenants, **Entra Agent ID** (reported GA through Agent 365 on 1 May 2026). The hub should consume these, not compete with them.

### Cited Findings
- **ANS (Agent Name Service):**
  - The Linux Foundation formally launched ANS as a project on **10 Nov 2026** at KubeCon NA in Salt Lake City, following an announcement of intent on 23 Jun 2026.
  - It is DNS-based: it ties an agent to a domain its operator controls and records signed lifecycle events in a transparency log.
  - 11 backing companies include Cisco, Salesforce and Cloudflare, under a technical steering committee.
  - AGNTCY ADS supports verification of ANS identities.
  - The launch PR calls the spec "formalized", but the project docs label the specs drafts.
  - Specs are at ansinfo.ai, with Go, Rust and Java libraries.

  — [PR Newswire](https://www.prnewswire.com/news-releases/linux-foundation-welcomes-agent-name-service-to-bring-verifiable-identity-and-discovery-to-ai-agents-302935151.html); [Computerworld](https://www.computerworld.com/article/4189369/new-linux-foundation-project-aims-to-bring-dns-style-trust-to-ai-agents-2.html); [It's FOSS](https://itsfoss.com/news/ans-joins-linux-foundation/)
- **DNS-AID:** an individual Internet-Draft (-02, 27 May 2026) that no working group has adopted, expiring 28 Nov 2026 (status as of 13 Oct 2026). — [API Evangelist Standards: DNS-AID](https://standards.apievangelist.com/store/dns-aid/)
- **AGNTCY ADS:**
  - OASF is the schema for agent records. Records are distributed as OCI artifacts over a Kademlia DHT.
  - There is an IETF individual draft, `draft-mp-agntcy-ads-01` (Feb 2026).
  - OASF v1.1.0 shipped on 10 Jul 2026 (35 releases in total).
  - AGNTCY has a project proposal open with AAIF (issue #57).
  - One secondhand claim: ADS is one of four reference implementations of Google's **Agentic Resource Discovery (ARD)** spec, announced 17 Jun 2026 and at v0.9 draft.

  — [arXiv 2509.18787](https://arxiv.org/html/2509.18787v1); [IETF draft-mp-agntcy-ads-01](https://datatracker.ietf.org/doc/draft-mp-agntcy-ads/01/); [aaif/project-proposals #57](https://github.com/aaif/project-proposals/issues/57)
- **NANDA Index (MIT Media Lab):** "NandaIndex" makes agents discoverable "without owning a domain". It is built jointly with AGNTCY/Outshift, with ADS providing the federated directory and NandaIndex handling resolution. Interoperability between the two is listed as in progress. — [MIT Media Lab](https://www.media.mit.edu/articles/nandaindex-making-ai-agents-discoverable-without-owning-a-domain/); [MIT switchboard PDF, Jul 2026](https://dam-prod.media.mit.edu/x/2026/07/20/IndexAIcatalog_IBLSCl6.pdf)
- **Web Bot Auth (IETF `webbotauth` WG):**
  - The working group is active, with an approved charter and chairs David Schinazi and Rifaat Shekh-Yusef.
  - The core document was adopted as **draft-ietf-webbotauth-httpsig-protocol-00 on 1 Sep 2026**, and -01 followed on 29 Oct 2026. It is not an RFC.
  - The charter's milestones (Apr 2026 to the IESG; Aug 2026 BCP) appear to have been missed.
  - At IETF 126 the WG discussed anonymous bot authentication.

  — [IETF datatracker WG page](https://datatracker.ietf.org/wg/webbotauth/about/); [IETF 126 minutes](https://datatracker.ietf.org/doc/minutes-126-webbotauth/); [nerdleveltech](https://nerdleveltech.com/web-bot-auth-ietf-standard-agent-verification)
- **Visa Trusted Agent Protocol (TAP):** announced by Visa and Cloudflare on 14 Oct 2025 with 12 partners; one source instead says "early 2026". It is described as using RFC 9421 HTTP Message Signatures and Web Bot Auth, with pilots in 2025 and scaling through 2026. — [ATXP](https://atxp.ai/blog/visa-trusted-agent-protocol-explained/); [eco.com](https://eco.com/support/en/articles/14845482-visa-trusted-agent-protocol-tap-explained) (secondary)
- **Skyfire KYA / KYAPay:**
  - An open protocol launched 26 Jun 2025, in production.
  - Its JWTs assert who the agent is, which human or enterprise it represents, and whether it is verified.
  - It has been demonstrated with Visa Intelligent Commerce (Dec 2025) and integrated with Fastly at the edge.

  — [BusinessWire](https://www.businesswire.com/news/home/20251218520399/en/Skyfire-Demonstrates-Secure-Agentic-Commerce-Purchase-Using-the-KYAPay-Protocol-and-Visa-Intelligent-Commerce); [Skyfire × Fastly](https://skyfire.xyz/verified-identity-at-the-edge-how-skyfire-and-fastly-enable-trusted-agent-commerce/); [Nevermined](https://nevermined.ai/blog/best-platforms-agentic-payments)
- **Microsoft Entra Agent ID:** reportedly GA as part of Microsoft Agent 365 from 1 May 2026, which gives each agent its own Entra Agent ID. No standalone GA announcement was found. — [idenhq](https://www.idenhq.com/en/blog/ai-agent-identity-management-2026) (secondary)
- Overview of how mature agent-authorization standards are (RFCs vs WG drafts vs individual drafts). — [hidekazu-konishi](https://hidekazu-konishi.com/entry/where_ai_agent_authorization_standards_stand.html)

### Inferences
- **Production-ready today:**
  - OAuth 2.1/OIDC, for human principals.
  - Web Bot Auth / RFC 9421 signatures, for agent requests (shipped by Cloudflare and Akamai-class CDNs even though it is not yet an RFC).
  - Skyfire KYAPay tokens.
  - Entra Agent ID, for enterprise employers.
- **Early or emerging:** ANS, ADS/OASF, NANDA Index, DNS-AID and ARD.
- **Recommended approach:** verify identity by accepting several signals and turning them into hub trust tiers:
  - T0: anonymous.
  - T1: verified email or OAuth principal.
  - T2: domain-bound agent (ANS, a signed A2A card on the domain, or a Web Bot Auth key directory).
  - T3: KYB for employers or KYA/ID for candidates.
- Publish the hub's own A2A card and OASF record, but do not depend on any single directory.
- **VCs/DIDs:** no source this session showed production agent use. Treat W3C VCs as a future format for portable credentials such as "verified employer" or "verified degree".

### Gaps
- Primary Visa, Skyfire and Microsoft pages were not fetched; the details above are from secondary sources.
- No verified current status for W3C VC/DID use by agents, or for Google ARD beyond one secondhand mention.
- Specific Web Bot Auth header names (`Signature-Agent`, key-directory path) were not verified this session.

## Payments and mandates (later phases): AP2, x402 and its known attacks, ACP, Stripe MPP, escrow

### Takeaway
None of these is needed for the MVP. **AP2** moved to the FIDO Alliance on about 28 Apr 2026 with v0.2 ("Human Not Present" mandates). **x402** has had more than 40 vulnerabilities published by academic researchers in 2026. **Stripe/Tempo MPP** launched on 18 Mar 2026 with more than 100 providers. **ACP** (OpenAI and Stripe) had no confirmed 2026 status update in these searches. For a hiring hub, take fiat success fees through Stripe first. Mandates become useful later for agent-paid fees or deposits.

### Cited Findings
- **AP2:**
  - Google donated AP2 to the FIDO Alliance on 28 Apr 2026 (one source says 29 Apr).
  - v0.2 adds "Human Not Present" payments within pre-set permissions.
  - FIDO set up an Agentic Authentication Technical Working Group.
  - Mastercard's "Verifiable Intent" was also donated to FIDO.

  — [FIDO Alliance](https://fidoalliance.org/google-donates-agent-payments-protocol-to-fido-alliance/); [TokenPost](https://www.tokenpost.com/news/technology/45562)
- **x402 attacks:**
  - "Five Attacks on x402 Agentic Payment Protocol" (arXiv 2605.11781, May 2026) found five practical attacks leading to "unpaid-service or paid-but-denied", plus 11 vulnerabilities in 3 SDKs and 4 live endpoints. — [arXiv 2605.11781](https://arxiv.org/abs/2605.11781)
  - "When HTTP 402 Meets the Blockchain" (arXiv 2607.19545) studied 15 facilitators and found **31 previously unknown vulnerabilities**, grouped as Free Shopping, Asset Theft, Service Denial and Gas Abuse. — [arXiv 2607.19545](https://arxiv.org/abs/2607.19545)
  - "Free-Riding in the AI Economy" (arXiv 2605.30998) found race conditions that let a service be duplicated. — [arXiv 2605.30998](https://arxiv.org/html/2605.30998v1)
- **Stripe MPP:**
  - The Machine Payments Protocol, co-authored by Stripe and Tempo (Paradigm), launched on **18 Mar 2026** with Tempo mainnet. Its directory had more than 100 providers, including Anthropic, OpenAI and Shopify. Visa contributed the card-payment flows.
  - Stripe supports ACP, MPP and x402 under its "Agentic Commerce Suite".

  — [Stripe blog](https://stripe.com/it/blog/machine-payments-protocol); [Fortune](https://fortune.com/2026/03/18/stripe-tempo-paradigm-mpp-ai-payments-protocol/); [The Block](https://www.theblock.co/amp/post/394131/tempo-mainnet-goes-live-with-machine-payments-protocol-for-agents)
- **ACP:** Stripe and OpenAI announced it in 2025 for checkout inside ChatGPT. No 2026 status was found. — [Fortune](https://fortune.com/2026/03/18/stripe-tempo-paradigm-mpp-ai-payments-protocol/)

### Inferences
- **Phase 1:** Stripe Billing or Checkout for employer subscriptions and success fees, paid by humans.
- **Phase 2:** use AP2-style mandates (now under FIDO) to let an employer agent pay per qualified intro within a capped budget.
- **Escrow:** for hiring there is little reason to escrow money. For other verticals, Stripe Connect manual capture or hold is safer than on-chain x402 escrow, given the published attacks.
- If x402 or MPP is ever accepted, settle **before** delivering the service, make retries idempotent, and verify facilitator responses. These defenses follow from the attack classes above and are inferred, not quoted.

### Gaps
- ACP's 2026 spec version and adoption were not found.
- No primary source was found on escrow standards for agents. "Escrow approaches" remains unresearched beyond the inferences above.

## Research on agent matching, negotiation, preference elicitation, mechanism design and intent schemas

### Takeaway
Three experiments give consistent lessons for the hub:
- **Microsoft Magentic Marketplace:** agents accept the first proposal they see (about 80–100% of the time), handle large search result sets poorly, and are easy to manipulate.
- **Anthropic Project Deal:** the stronger model wins and its principal does not notice. Prompting for "aggressive" negotiation does little.
- **Anthropic Project Swap:** most of the gap to an optimal outcome came from *preference elicitation*, not from trading.

The design rule that follows: the hub should centralize matching with a mechanism that ranks good options, show a short curated list, invest in structured preference capture, and not rely on free-form agent haggling.

### Cited Findings
- **Magentic Marketplace** (Microsoft Research with ASU, Oct 2025, arXiv 2510.25779):
  - About 80–100% of agents accepted the first proposal they received, giving a 10–30x advantage to speed over quality.
  - Welfare collapsed when agents were shown 100 search results.
  - Six manipulation strategies were tested, from fake credentials and social proof to prompt injection. Press reports that GPT-4o and gpt-oss-20b had all payments redirected and that only Sonnet 4 resisted; this is unverified against the paper.
  - Frontier models approached optimal welfare "only under ideal search conditions."
  - The framework is open source.

  — [arXiv 2510.25779](https://arxiv.org/html/2510.25779v1); [MSR publication](https://www.microsoft.com/en-us/research/publication/magentic-marketplace-an-open-source-environment-for-studying-agentic-markets/); [Decrypt](https://decrypt.co/?p=347709)
- **Anthropic Project Deal** (run Dec 2025, published about 24 Apr 2026):
  - 69 employees, 186 deals, more than 500 items, just over $4,000 traded.
  - Opus agents closed about 2 more deals than Haiku agents and earned sellers $2.68 more per item.
  - "Aggressive" instructions gave no statistically significant advantage.
  - Anthropic warned that people "could end up on the losing side … without any awareness."

  — [Unite.AI](https://www.unite.ai/anthropics-project-deal-lets-claude-agents-trade-real-goods/); [EdTech Innovation Hub](https://www.edtechinnovationhub.com/news/anthropics-ai-agents-struck-186-deals-in-a-real-marketplace-and-the-stronger-model-won-every-time) (secondary)
- **Anthropic Project Swap:** a book-barter market with 201 employees in 6 offices, where preferences were captured through a short intake conversation with Claude. Secondary reports say:
  - Agents matched people's pairwise rankings 61% of the time.
  - Scores were 0.89 for the optimal assignment, 0.60 for the best assignment from Claude's rankings, and 0.55 for what the market actually delivered.
  - **About 85% of the shortfall came from imprecise preference capture**, and 15% from the trading mechanism.

  These figures are unverified against Anthropic's report. — [Anthropic: Project Swap](https://www.anthropic.com/research/project-swap); [FourWeekMBA](https://fourweekmba.com/ai-anthropic-agent-market-85-percent-shortfall-was-preferences/); [TechJack](https://techjacksolutions.com/ai-brief/anthropic-project-swap-agent-preference-alignment-61-percent/)
- **Negotiation benchmarks:**
  - AgoraBench/MERIT (arXiv 2602.10467, KAIST, Amazon AGI and LG AI Research): 9 market settings including deception and monopoly; utility-based metrics; baseline LLM strategies diverge from human behavior. — [arXiv 2602.10467](https://arxiv.org/html/2602.10467v4)
  - BargainArena (arXiv 2505.22998). — [arXiv](https://arxiv.org/html/2505.22998v1)
  - Bilateral trade with private information (arXiv 2604.16472): 15,000 negotiations among 5 frontier models; the strongest strategies used price discrimination through sequential offers; the authors propose individual-rationality penalties. — [arXiv 2604.16472](https://arxiv.org/html/2604.16472)
  - AgenticPay (arXiv 2602.06008): one-to-one through many-to-many markets; persistent weaknesses in long-horizon strategy. — [arXiv 2602.06008](https://arxiv.org/html/2602.06008v1)
  - Multi-player bargaining (arXiv 2509.09071): LLMs reached about 62% of surplus vs 59% for humans, using different strategies. — [arXiv 2509.09071](https://arxiv.org/pdf/2509.09071v4)
- **Intent schemas:**
  - schema.org `JobPosting` is the de facto web vocabulary for jobs. Properties include `title`, `hiringOrganization`, `baseSalary`, `employmentType`, `jobLocation`, `jobLocationType` (TELECOMMUTE), `applicantLocationRequirements`, `skills`, `experienceRequirements`, `educationRequirements`, `validThrough` and `directApply`. — [schema.org/JobPosting](https://schema.org/JobPosting) (canonical page; property list from prior knowledge, not re-fetched this session)
  - HR Open Standards publishes recruiting JSON schemas (position openings, candidates). — [HR Open Standards](https://www.hropenstandards.org/) (not fetched this session; treat as a pointer)
  - OASF from AGNTCY defines agent *capability* records, not intents. — [arXiv 2509.18787](https://arxiv.org/html/2509.18787v1)

### Inferences
- **Matching should be a hub-side mechanism, not an agent-side search.**
  - Hard-constraint filtering, then scoring, then a **short list of about 3–5 options delivered together**. Delivering them as a batch, not one at a time, counters first-proposal bias.
  - Consider stable-matching or deferred-acceptance-style batch rounds for two-sided hiring markets. This is the standard mechanism-design remedy for congestion and first-offer effects; no source found applies it to LLM agents specifically.
- **Put effort into preference elicitation** (Project Swap):
  - A structured intake with typed fields, explicit deal-breakers, and pairwise or ranking questions.
  - Hub-hosted elicitation through MCP MRTR, so the hub does not depend on every user's agent doing it well.
- **Counter weak-agent disadvantage** (Project Deal):
  - Typed offers with hub-computed zones of agreement, so neither agent needs to be clever about salary bands.
  - Show each principal transparent benchmarks.
- **Model intents as a JSON Schema profile of schema.org JobPosting** for employers, with a mirrored "JobSeek" profile for candidates.
  - Add per-field disclosure levels (public, on-match, on-mutual-consent).
  - Add a hard/soft constraint flag on each field.
  - Keep a `notes` free-text field that is treated as untrusted.

### Gaps
- Anthropic's Project Swap and Project Deal primary pages were not fetched; the figures come from secondary sources.
- No 2025–2026 paper found on LLM agents *for hiring* specifically, or on two-sided matching mechanisms run by LLM agents.
- HR Open Standards' current schema version was not verified.

## Security for agent-to-agent systems: prompt injection, OWASP ASI Top 10, sybil resistance, defensive patterns

### Takeaway
The OWASP Top 10 for Agentic Applications (2026) was released on **9 Dec 2025** and numbered **ASI01–ASI10**. For a hub, **ASI01 Goal Hijack** and **ASI07 Insecure Inter-Agent Communication** matter most, followed by ASI03, ASI06, ASI09 and ASI10. The strongest defenses are architectural: typed messages, the hub as the sole holder of state and policy, dual-LLM / CaMeL-style isolation inside any hub-run LLM, and capability-scoped tokens. Filtering alone is not enough.

### Cited Findings
- **OWASP Top 10 for Agentic Applications 2026**, released 9 Dec 2025 by the OWASP GenAI Security Project's Agentic Security Initiative, with more than 100 contributors. — [OWASP GenAI](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/); [OWASP blog 9 Dec 2025](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agent); [TechRepublic](https://www.techrepublic.com/article/news-owasp-ai-agent-risk-list/)

  | ID | Name | Description and notes |
  |---|---|---|
  | ASI01 | Agent Goal Hijack | Redirecting an agent's goal through content it reads |
  | ASI02 | Tool Misuse & Exploitation | |
  | ASI03 | Identity & Privilege Abuse | |
  | ASI04 | Agentic Supply Chain Vulnerabilities | Tools, plugins, registries, MCP servers |
  | ASI05 | Unexpected Code Execution (RCE) | |
  | ASI06 | Memory & Context Poisoning | F5 calls it "Context Management and Retrieval Manipulation" |
  | ASI07 | Insecure Inter-Agent Communication | Spoofed or unauthenticated agent-to-agent messages |
  | ASI08 | Cascading Failures | |
  | ASI09 | Human-Agent Trust Exploitation | |
  | ASI10 | Rogue Agents | |

  — numbering consolidated from [Snyk Learn](https://learn.snyk.io/learning-paths/owasp-top-10-agentic/), [FINOS AIR](https://air-governance-framework.finos.org/references/owasp-asi), [HUMAN Security](https://www.humansecurity.com/learn/blog/owasp-top-10-agentic-applications/), [Speakeasy](https://www.speakeasy.com/blog/owasp-agentic-top-10-explained) and [Aikido](https://aikido.dev/blog/owasp-top-10-agentic-applications). Secondary sources agree on the numbering. The official PDF could not be fetched (genai.owasp.org is blocked here), so check the exact titles there. The F5 glossary page is garbled.
- OWASP calls "least agency" a core principle: give agents only the minimum autonomy needed. — [Aikido](https://aikido.dev/blog/owasp-top-10-agentic-applications); [CSA research note](https://labs.cloudsecurityalliance.org/research/csa-research-note-owasp-genai-top10-2026-agent-control-stand/)
- **Design Patterns for Securing LLM Agents against Prompt Injections** (arXiv 2506.08837; IBM, Invariant Labs, ETH Zurich, Google and others):
  - Six patterns: action-selector, plan-then-execute, LLM map-reduce, dual LLM, code-then-execute and context-minimization.
  - The patterns "constrain the actions of agents to explicitly prevent them from solving arbitrary tasks."
  - CaMeL (DeepMind) is an improved dual-LLM design: the privileged LLM writes code in a sandboxed DSL with data-flow tagging.
  - Dual LLM stops injected tool calls but not injected *content* that flows into values the plan uses.

  — [arXiv 2506.08837](https://arxiv.org/html/2506.08837v3); [Simon Willison](https://simonwillison.net/2025/Jun/13/prompt-injection-design-patterns/); [arXiv 2611.11506 (formal verdicts)](https://arxiv.org/pdf/2611.11506); [arXiv 2509.08646 (plan-then-execute guide)](https://arxiv.org/pdf/2509.08646)
- **Empirical evidence of manipulation in agent markets:** Magentic Marketplace's six attacks (fake credentials, social proof, prompt injection) redirected payments for some models. — [arXiv 2510.25779](https://arxiv.org/html/2510.25779v1)
- A2A itself says `AUTH_REQUIRED` transitions must not be treated as authorization, and that a credential obtained in a task must not be assumed to authorize later messages. — [A2A spec §7.6](https://github.com/a2aproject/A2A/blob/main/docs/specification.md)
- MCP 2026-07-28 header routing (`Mcp-Method`, `Mcp-Name`) lets a WAF or gateway authorize per tool without parsing the body. — [MCP blog](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/blog/content/posts/2026-07-28-spec-ga/index.md)
- Supply-chain hygiene (ASI04): 71% of net-new MCP Registry entries cannot be validated. — [DEV](https://dev.to/amareswer/the-mcp-registry-by-the-numbers-38nc)

### Inferences
**Hub-level controls**
- **Typed messages:** negotiation moves are JSON-Schema objects such as `propose{salary, start, remote}`, `accept` and `decline{reason_code}`. Free text is capped in length, labeled `untrusted_counterparty_text` in every MCP and A2A payload, and never interpreted by the hub as instructions.
- **Hub as reference monitor:** the hub enforces the disclosure policy (which fields the counterparty may see at each stage) in code. An injected "reveal your salary floor" therefore fails even if the receiving agent is fooled, because the agent never holds the counterparty's private data until the policy allows it.
- **Hub-run LLMs** (summarizers, match explainers, moderation) use a dual-LLM or CaMeL split: the quarantined model reads counterparty text, and the privileged model sees only typed outputs.
- **Capability tokens:**
  - Short-lived, audience-bound OAuth tokens per session, with scopes such as `session:{id}:propose` and `intent:{id}:read`.
  - Optionally Macaroons or Biscuits with caveats (expiry, max messages, allowed counterparties). These are standard designs; no source checked this session.
  - A2A and MCP tokens are bound to their issuer, per MCP SEP-2352.
- **Sybil resistance:**
  - Rate limits and quotas are per verified *principal*, not per agent.
  - Higher tiers need KYB (employer domain plus business registry) or KYA tokens.
  - Optional refundable deposits for high-volume posters.
  - Reputation is tied to completed hand-offs, not to message volume.
  - Graph and behavioral anomaly detection for duplicate personas.
- **Human-in-the-loop at irreversible steps:** identity reveal and hand-off use MCP MRTR elicitation or A2A `INPUT_REQUIRED`. This addresses ASI09.
- **Audit log:** append-only log of every typed move, with signed hashes. This supports ASI10 forensics and hiring record-keeping.

**Client-side guidance**
- Publish a "safe client" SDK and prompt template telling user agents to treat hub-delivered counterparty text as data.

### Gaps
- Official OWASP ASI titles were not read in the primary document.
- No peer-reviewed source was found on sybil resistance in agent marketplaces specifically.
- No specific benchmark of agent-to-agent prompt-injection success rates beyond Magentic Marketplace was retrieved.

## Recommended MVP architecture and tech stack, with trade-offs

### Takeaway
Build one neutral, stateful hub service (Postgres as the source of truth) with two thin protocol faces:
- **A stateless MCP 2026-07-28 server** with OAuth 2.1 + CIMD. This is the primary face, serving Claude, ChatGPT, OpenClaw and other MCP clients.
- **A multi-tenant A2A v1.0 endpoint** with a signed Agent Card and push webhooks, for autonomous and enterprise agents.

Behind both sit a typed intent store, a hybrid matcher that filters on hard constraints and then ranks with embeddings, a negotiation state machine that maps onto A2A Task states, a disclosure and consent policy engine, and a hand-off service. Defer payments, decentralized discovery and VCs.

### Cited Findings (building blocks and their basis)
- **Stateless MCP core:** handle-based state, header routing and MRTR for approvals make serverless or edge hosting viable. Cloudflare Workers/Agents SDK and AWS Bedrock AgentCore supported the spec on day one. — [MCP blog](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/blog/content/posts/2026-07-28-spec-ga/index.md)
- **A2A multi-tenant endpoint:** a `tenant` per request, signed cards (JWS+JCS), push configs, task states including `INPUT_REQUIRED`/`AUTH_REQUIRED`, OAuth2 with PKCE, Device Code (for CLI agents) and mTLS; six official SDKs. — [A2A what's new](https://github.com/a2aproject/A2A/blob/main/docs/whats-new-v1.md); [A2A roadmap](https://github.com/a2aproject/A2A/blob/main/docs/roadmap.md)
- **Proprietary registry/search API:** A2A defines no registry API, so this is the hub's own surface. — [A2A discovery guide](https://github.com/a2aproject/A2A/blob/main/docs/topics/agent-discovery.md)
- **Short, batched result lists**, to counter first-proposal bias and search overload. — [Magentic Marketplace](https://arxiv.org/html/2510.25779v1)
- **Elicitation-first onboarding**, because preference capture is the main bottleneck. — [Project Swap coverage](https://fourweekmba.com/ai-anthropic-agent-market-85-percent-shortfall-was-preferences/)
- **ChatGPT directory listing risk:** the guidelines exclude "pass-through intermediary" connectors. — [OpenAI guidelines](https://developers.openai.com/apps-sdk/app-submission-guidelines)

### Inferences (proposed MVP design)
**Components**
1. **Edge/gateway**
   - Cloudflare Workers or a similar edge, or Fly.io/Cloud Run.
   - Web Bot Auth and RFC 9421 signature verification, optional at T0.
   - OAuth 2.1 resource server.
   - Per-principal rate limits keyed on `Mcp-Method`/`Mcp-Name`.
   - WAF.
2. **Auth**
   - An off-the-shelf OAuth 2.1/OIDC provider that supports PKCE, RFC 9207 `iss` and CIMD, for example Auth0, WorkOS, Stytch, Clerk or Ory. Verify each provider's CIMD support before choosing.
   - Principals are humans or organizations; agents are child identities bound to a principal.
   - Optional inputs: KYA (Skyfire), Entra Agent ID (enterprise) and domain verification (ANS, `/.well-known` card, DNS TXT).
3. **Core service**
   - A TypeScript monolith, since the TS MCP and A2A SDKs are Tier 1 and official, or Python with FastMCP 4.0 plus a2a-python. Pick one language.
   - Postgres with row-level security, **pgvector** for skill embeddings, and an outbox table for events.
   - A job queue such as Postgres-backed (pg-boss/Graphile) or Temporal if long-running orchestration grows.
4. **Intent store**
   - JSON Schema profiles: `JobOffer`, a schema.org JobPosting superset, and `JobSeek`, its mirror.
   - Per-field `disclosure` (public / on_match / on_consent) and `constraint` (hard/soft/weight).
   - Versioned intents with expiry (`validThrough`).
5. **Matcher**
   - SQL hard filters (location or remote, work authorization, salary-band overlap, seniority), then a vector similarity plus rules score, then an optional LLM re-rank with a dual-LLM split.
   - Results delivered in **batched rounds** of the top 3–5 per side.
   - Mutual-interest gating (both sides "like") before a session opens.
6. **Negotiation broker**
   - A finite state machine: `proposed → open → (offer ↔ counter)* → agreed | declined | expired`, mapped onto A2A Task states.
   - Caps on number of moves and wall-clock time ("bounded negotiation").
   - Typed moves plus length-capped labeled free text.
   - The hub computes the zone of possible agreement on numeric fields.
7. **Consent and disclosure engine**
   - Policy-as-code (OPA/Cedar, or plain code) controls which fields are released at which stage.
   - Each release requires principal approval through MCP MRTR elicitation, A2A `INPUT_REQUIRED`, or an email or web confirm link.
8. **Notifications**
   - A2A push webhooks (signed) for server agents.
   - For MCP-only clients, a pollable `get_inbox` tool plus email or web push to the human, because consumer assistants cannot receive webhooks.
9. **Hand-off**
   - A structured hand-off Artifact (contact details, agreed terms, next step), an intro email, and an ICS invite or scheduling link.
   - For agents that have one, the A2A Agent Card URL for a direct connection after the match.
10. **Audit and observability**
    - An append-only event log (hash-chained), OpenTelemetry traces, and moderation queues.
    - Bias-audit exports, since hiring carries regulatory obligations.

**MCP tool surface**
- `whoami`, `create_intent`, `update_intent`, `withdraw_intent`, `get_matches` (batched), `express_interest`, `get_inbox`, `get_session`, `make_move` (typed), `ask_question` (free text, untrusted), `approve_disclosure`, `request_handoff`.
- Long-running searches use the Tasks extension.

**A2A surface**
- One signed Agent Card for the hub, with skills such as `post-intent`, `match` and `negotiate`.
- Optionally, per-tenant cards for listed enterprise agents.

**Trade-offs**
- **MCP-first vs A2A-first.** MCP-first reaches consumer assistants immediately but makes the hub the *orchestrator*: user agents poll and act turn-by-turn, and their human is often present. A2A-first enables true autonomous negotiation but needs agents that run as servers, which few job seekers have.
  - Recommendation: MCP-first, with an A2A endpoint for employers and ATS vendors.
- **Hub-run negotiator vs user-agent-run.** The hub could run proxy agents on each side's preferences, which is simpler, consistent and fairer across model strengths, but this breaks neutrality and "bring your own agent" and adds liability. User agents keep autonomy but bring Project Deal-style inequality and injection risk.
  - Recommendation: user agents negotiate over **typed moves**, and the hub computes the zone of agreement. Offer an opt-in "hub auto-negotiator" later.
- **Stateless serverless vs long-lived workers.** MCP 2026-07-28 makes serverless natural, but matching rounds and expiries need a scheduler or queue.
  - Recommendation: serverless edge in front, plus a small worker pool for jobs.
- **Embeddings vs structured matching.** Embeddings capture skill similarity but are opaque and raise bias concerns in hiring.
  - Recommendation: deterministic hard filters plus explainable scoring, with embeddings only as one logged feature.
- **Decentralized discovery (ANS/ADS/NANDA) now vs later.** These are all early.
  - Recommendation: publish an A2A card and OASF record and accept ANS-verified domains as a trust signal, but run the hub's own index.
- **Payments.** Defer agent-native rails, given the x402 vulnerabilities and AP2's early v0.2. Use Stripe for fiat.

### Gaps
- No source was found evaluating particular OAuth vendors' support for MCP CIMD or RFC 9207 as of Nov 2026; this needs checking against vendor docs.
- No published reference architecture for a public agent-to-agent marketplace was found to benchmark against. The design above is synthesized from the protocol specs and experiment findings.
- OpenClaw-specific integration details (skills vs MCP, ClawHub listing) were not researched in this session.
