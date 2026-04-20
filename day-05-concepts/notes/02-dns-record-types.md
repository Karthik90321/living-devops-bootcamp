# Common DNS Record Types

DNS records tell resolvers what to return for a given domain name. Each record type answers a different question.

## The record types that matter

### A record — "what's the IPv4?"
- Maps `example.com` → `13.235.1.2`
- The most basic record. Required for any domain pointing to a specific IP.
- **Example:** `bootcamp.example.com  A  13.235.1.2`

### AAAA record — "what's the IPv6?"
- Same as A but returns an IPv6 address.
- Rarely configured manually — most small apps still rely on IPv4.
- **Example:** `example.com  AAAA  2606:4700::1111`

### CNAME — "this domain is an alias for that domain"
- Maps one domain name to another domain name (not an IP).
- Resolver follows the chain: user asks for `www.example.com`, gets back `example.com`, then resolves that.
- **Cannot be used on the root domain** (`example.com` — the apex). Only subdomains (`www.example.com`, `blog.example.com`).
- **Example:** `www.example.com  CNAME  example.com`

### Alias (Route 53–specific)
- AWS's invention to work around CNAME's apex limitation.
- Looks like an A record to the outside world but maps to an AWS resource (ALB, CloudFront, S3 bucket) by name.
- AWS auto-updates the target IPs behind the scenes.
- **Use when** pointing your apex domain at a load balancer — CNAME can't do it, Alias can.
- **Example:** `example.com  A (Alias)  my-alb-123.ap-south-1.elb.amazonaws.com`

### MX record — "where do I deliver email for this domain?"
- Tells mail servers where to route `@example.com` mail.
- Has a priority number — lower = preferred. Multiple MX records = failover.
- **Example:** `example.com  MX  10 mail.example.com`

### TXT record — "arbitrary text data"
- Free-form text, used for verification and policy.
- Common uses:
  - Domain ownership verification (Google, AWS, Let's Encrypt ask you to add a TXT record to prove you own the domain)
  - SPF (`v=spf1 include:_spf.google.com ~all`) — anti-spam email policy
  - DKIM and DMARC — email authentication
- **Example:** `example.com  TXT  "v=spf1 include:_spf.google.com ~all"`

### NS record — "who are the authoritative name servers for this domain?"
- Points to the servers that have the real DNS records for this domain.
- When you "move a domain to Route 53," what actually happens: you update the NS records at your registrar (Hostinger, GoDaddy) to point to AWS's name servers.
- **Example:** `example.com  NS  ns-123.awsdns-45.com`

### SOA record — "who's in charge of this zone?"
- Administrative metadata about a DNS zone (primary NS, admin email, serial number, refresh interval).
- Auto-created. You rarely touch this.

### PTR record — reverse DNS
- Maps an IP back to a domain name. Used by mail servers to verify senders.
- Typically managed by your IP owner (AWS for EC2 public IPs), not you directly.

## Quick comparison

| Record | Maps what to what? | Common use |
|---|---|---|
| A | domain → IPv4 | Point domain to an EC2/server |
| AAAA | domain → IPv6 | IPv6 support |
| CNAME | subdomain → another domain | Alias subdomains (`www → apex`) |
| Alias (AWS) | apex → AWS resource name | Apex domain to ALB/CloudFront |
| MX | domain → mail server | Receive email |
| TXT | domain → text | Verify ownership, SPF, DKIM |
| NS | domain → name servers | Delegate DNS to another provider |

## The CNAME-at-apex problem (why Alias exists)

DNS RFC forbids CNAME on a root domain. So if your root is `example.com` and your ALB is `my-alb.elb.amazonaws.com`:

- ❌ `example.com  CNAME  my-alb.elb.amazonaws.com` — **illegal**
- ❌ `example.com  A  <some ALB IP>` — **works today, breaks tomorrow** when AWS rotates the ALB's IPs
- ✅ `example.com  A (Alias)  my-alb.elb.amazonaws.com` — AWS handles IP rotation

This is a huge reason Route 53 is preferred for apps hosted in AWS.

## TTL — the forgotten field

Every DNS record has a TTL (time to live, in seconds). Resolvers cache the answer for that long before asking again.

- **Low TTL (60s)** — changes propagate fast. Useful before a migration. Increases DNS query volume.
- **High TTL (3600s or more)** — changes are slow to propagate (hours). Lower query volume, lower cost.

**Rule of thumb:** lower TTL a day or two before you plan a DNS change, then raise it back after.

## Interview questions

1. Why can't you use a CNAME on `example.com` but you can on `www.example.com`?
2. What's the difference between a CNAME and a Route 53 Alias record?
3. You added an A record but your users still see the old IP. What's happening?
4. How would you prove you own a domain to a third-party service without giving them your credentials?
5. What does the MX priority number mean?

## Sources

- AWS Route 53 developer guide: Supported DNS record types
- Byte Byte Go: "DNS Records Explained" (recommended)