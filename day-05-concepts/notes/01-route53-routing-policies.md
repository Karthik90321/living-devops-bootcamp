# Route 53 Routing Policies

Route 53 is AWS's DNS service. A **routing policy** decides which IP/record it returns when someone queries your domain. Different policies solve different problems.

## The six policies

### 1. Simple
- One record, one answer. No intelligence.
- Used when you have a single resource (one EC2, one load balancer) and don't care about geography or health.
- **Use when:** prototyping, dev environments, single-region apps.

### 2. Weighted
- Return multiple IPs, each with a weight (e.g., 80% to server A, 20% to server B).
- DNS returns answers in that ratio over many queries.
- **Use when:** blue/green deployments, A/B testing a new version, gradual migration to a new backend.

### 3. Latency-based
- Route users to the region with the lowest network latency from their location.
- AWS measures latency continuously between its regions and the user's resolver.
- **Use when:** you have infrastructure in multiple AWS regions and want to serve users from the closest one. Requires having resources in multiple regions.

### 4. Failover
- Primary record answers normally. If a health check on the primary fails, secondary takes over.
- Requires Route 53 health checks to be configured.
- **Use when:** active-passive disaster recovery. One region serves, another is warm standby.

### 5. Geolocation
- Route based on the user's **country or continent**, not latency.
- Different from latency-based — a user in Nepal might have lowest latency to Mumbai, but you could force them to a specific server based on their country.
- **Use when:** legal/compliance reasons (GDPR data residency), content licensing per region, localized content.

### 6. Geoproximity (requires Route 53 Traffic Flow)
- Like geolocation but more granular — you can bias traffic toward or away from a region using a "bias" value.
- **Use when:** you want fine-tuned global traffic shaping. Less common for beginners.

### 7. Multivalue Answer
- Returns up to 8 healthy records at random, like a poor-man's load balancer at the DNS level.
- Each record can have its own health check.
- **Use when:** simple HA across a few EC2s without setting up an actual load balancer. Low-traffic apps only.

## Quick comparison

| Policy | Key benefit | Needs health checks? |
|---|---|---|
| Simple | Easiest | No |
| Weighted | Traffic splitting | Optional |
| Latency | Speed for global users | Optional |
| Failover | Active-passive DR | **Required** |
| Geolocation | Compliance/localization | Optional |
| Geoproximity | Fine-grained control | Optional |
| Multivalue | Basic HA without LB | Optional (recommended) |

## Interview-relevant distinctions

- **Latency vs geolocation:** latency routes by measured network speed; geolocation routes by the user's physical country/continent. Different use cases.
- **Failover vs multivalue:** failover is 1→1 (primary fails, go to backup). Multivalue is 1→N (return multiple healthy answers).
- **Weighted is DNS-level, not load-balancer-level:** traffic distribution happens in DNS responses, not in an ALB. A single user might hit server A on one page load and server B on the next — DNS caching affects consistency.

## When NOT to use Route 53 policies

If you have an ALB fronting your EC2s, most distribution happens at the **ALB**, not DNS. Route 53 just points the domain to the ALB (as an Alias record). You'd only use weighted/latency DNS policies when distributing across *different* ALBs in different regions, not within one.

## Sources

- AWS docs: Choosing a routing policy
- Byte Byte Go: "How DNS Works" (recommended by Akhilesh)