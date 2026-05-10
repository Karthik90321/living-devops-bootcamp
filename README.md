# Living DevOps Bootcamp — Hands-On Labs

Hands-on labs, notes, and artifacts from **Akhilesh Mishra's Living DevOps AWS Bootcamp (Jan 2026 batch)**. Each folder is a self-contained lab with commands, screenshots, and takeaways.

Maintained by **Karthik** — 10+ years in application support, transitioning into DevOps / SRE. This repo tracks bootcamp progress and doubles as a portfolio of practical work.

---

## Table of Contents

- [About](#about)
- [Modules](#modules)
  - [Day 01 — Linux Intro & First EC2](#day-01--linux-intro--first-ec2)
  - [Day 02 — Linux Performance & Process Management](#day-02--linux-performance--process-management)
  - [Day 03 — Bash Scripting](#day-03--bash-scripting)
  - [Day 04 — AWS Networking](#day-04--aws-networking)
  - [Day 05 — Concepts: DNS, HTTPS, Route 53](#day-05--concepts-dns-https-route-53)
  - [Day 06 — Web App Deployment](#day-06--web-app-deployment)
- [Tech Stack](#tech-stack)

---

## About

This repo is the working record of a structured AWS DevOps bootcamp. Every module is a self-contained lab built on a live EC2 instance (or locally in WSL), documented with:

- A `README.md` walkthrough of the concepts and commands
- `scripts/` — the actual shell or Python scripts produced
- `screenshots/` — AWS console and terminal evidence
- `outputs/` — captured terminal output used as proof of work

The goal: build the practical skills (Linux, networking, scripting, cloud) that show up in DevOps/SRE job descriptions, documented in a way that can be shared with hiring teams.

---

## Modules

### Day 01 — Linux Intro & First EC2

> [day-01-linux-intro/](./day-01-linux-intro)

First EC2 instance launch and foundational Linux skills every DevOps engineer needs from day one.

**Covers:** SSH key pairs + `chmod 400`, connecting from WSL to a remote Linux server, multi-session behaviour, local vs exported environment variables, persisting config via `~/.bashrc`, PATH troubleshooting, writing and executing a basic shell script.

---

### Day 02 — Linux Performance & Process Management

> [day-02-linux-perf/](./day-02-linux-perf)

Real-time monitoring and troubleshooting on a live EC2 instance under synthetic load.

**Covers:** Process states (R/S/D/Z/T), `ps aux`, `top`, `htop`, `pstree`, CPU load with `stress-ng`, load average interpretation, memory monitoring (`free -h`, `pmap`), I/O monitoring (`iostat`, `iotop`, `%iowait`), disk usage (`df`, `du`), `systemctl`, `renice`, real-world high-CPU / memory-leak / I/O-wait investigation scenarios.

---

### Day 03 — Bash Scripting

> [day-03-bash-scripting/](./day-03-bash-scripting)

Bash fundamentals applied to three production-style scripts.

**Covers:** Shebang and shell selection, `chmod` permissions, `$1`/`$#`/`$@` arguments, exit codes (`$?`), I/O redirection (`>`, `>>`, `2>`, `&>`), conditionals, for/while loops, functions, AWK field extraction.

**Scripts built:**
- `log-rotate.sh` — compresses logs with timestamp suffix, truncates original
- `ip-blocker.sh` — parses access logs and blocks IPs exceeding a request threshold
- `sysmonitor.sh` — system health report (CPU, memory, disk, top processes)

---

### Day 04 — AWS Networking

> [day-04-aws-networking/](./day-04-aws-networking)

Production-style network architecture built from scratch in AWS.

**Covers:** Custom VPC (`10.0.0.0/16`), public and private subnets, Internet Gateway, route tables (what actually makes a subnet "public"), auto-assign public IPv4, bastion host / jump-box pattern, NAT Gateway vs NAT Instance, Elastic IP, security group layering, SCP for file transfers, teardown order to avoid orphaned billable resources.

**Architecture:** Bastion EC2 (public subnet) → Private EC2 (private subnet, no public IP) → NAT Gateway for outbound internet.

---

### Day 05 — Concepts: DNS, HTTPS, Route 53

> [day-05-concepts/](./day-05-concepts)

Conceptual study day — the full web request lifecycle from browser to server.

**Covers:** Static → 2-tier → 3-tier → microservices architectures, HTTP vs HTTPS, TLS handshake step-by-step, reverse proxies, Flask + Gunicorn + Nginx production stack, Let's Encrypt / AWS Certificate Manager, load balancers.

**Study notes:**
- [Route 53 routing policies](./day-05-concepts/notes/01-route53-routing-policies.md) — simple, weighted, latency, failover, geolocation, geoproximity, multivalue
- [DNS record types](./day-05-concepts/notes/02-dns-record-types.md) — A, AAAA, CNAME, Alias, MX, TXT, NS, SOA
- [HTTPS and DNS fundamentals](./day-05-concepts/notes/03-https-and-dns-fundamentals.md) — full request flow, TLS handshake, Nginx+Flask stack

---

### Day 06 — Web App Deployment

> [day-06-webapp-deploy/](./day-06-webapp-deploy)

End-to-end deployment of a Flask portfolio app to a live domain.

**Covers:** EC2 instance setup, Flask app served via Gunicorn, Nginx as reverse proxy (port 80 → Gunicorn on 8000), security group hardening (closing port 8000 after proxy is live), custom domain (`devopsengineer.shop`) wired up via Hostinger DNS pointing to the EC2 public IP.

**Stack:** Python + Flask + Gunicorn + Nginx + EC2 + custom domain.

---

## Tech Stack

| Layer | Tools |
|---|---|
| Cloud | AWS (ap-south-1 / Mumbai) |
| Compute | EC2 (Amazon Linux 2023, t2/t3.micro) |
| Networking | VPC, IGW, NAT Gateway, Security Groups, Route 53 |
| Web serving | Flask, Gunicorn, Nginx |
| Scripting | Bash, Python |
| IaC (upcoming) | Terraform |
| Containers (upcoming) | Docker, ECS |
| CI/CD (upcoming) | GitHub Actions |
| Local environment | Windows 11 + WSL Ubuntu + VS Code |
