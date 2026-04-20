# Day 05 — Concepts: Application Architectures, DNS, HTTPS, Route 53

**Feb 4, 2026 session of the Living DevOps Bootcamp.** Mostly conceptual — the intended hands-on demo was postponed to Day 06 due to a payment issue on the instructor's side. This folder captures the study work assigned.

## What was covered in the session

- Application architectures: static → 2-tier → 3-tier → microservices
- Why deploy a single app on EC2 with ports 80 and 443 open
- Elastic IP for a static public address
- HTTP vs HTTPS — what encryption in transit actually protects
- Flask + Gunicorn + Nginx production stack
- Python virtualenv and `requirements.txt`
- Reverse proxies and why Nginx sits in front of Flask
- Free TLS certs via Let's Encrypt and AWS Certificate Manager
- Load balancers as managed Nginx-fronted services
- Route 53 hosted zones, NS records, and routing policies

## Assigned study work

Three reading/study tasks were given. This folder contains my notes on each:

1. **[Route 53 routing policies](notes/01-route53-routing-policies.md)** — simple, weighted, latency, failover, geolocation, geoproximity, multivalue
2. **[DNS record types](notes/02-dns-record-types.md)** — A, AAAA, CNAME, Alias, MX, TXT, NS, SOA
3. **[HTTPS and DNS fundamentals](notes/03-https-and-dns-fundamentals.md)** — full request flow, TLS handshake, certs, Nginx+Flask stack

Recommended source: the **Byte Byte Go** YouTube channel for concise system design videos on these topics.

## Key takeaways in one paragraph

A user hitting `https://example.com` triggers a chain: their browser asks a DNS resolver for the IP, which walks from root → TLD → authoritative name server (Route 53 in our case) and returns the answer. The browser then opens a TCP connection and performs a TLS handshake, verifying the server's certificate against its list of trusted CAs. The TLS handshake establishes a shared symmetric key (because public-key crypto is too slow for bulk traffic), and the actual HTTP request flows encrypted. On the server, Nginx terminates TLS and proxies the decrypted request to Gunicorn on localhost, which runs the Flask app. The reverse path carries the response back, re-encrypted at Nginx. This whole dance — DNS resolution + TCP + TLS + HTTP — typically completes in ~200ms.
