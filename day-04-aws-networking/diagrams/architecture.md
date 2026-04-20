# Day 04 — Network Architecture
;
Internet
                                  │
                          ┌───────┴───────┐
                          │ Internet GW   │  jan26-igw
                          │ (jan26-igw)   │
                          └───────┬───────┘
                                  │
      ┌───────────────────── VPC: jan26-vpc ─────────────────────┐
      │                     CIDR: 10.0.0.0/16                     │
      │                                                            │
      │   ┌────────────────────────────────────────────────────┐  │
      │   │ Public Subnet: jan26-public-subnet (10.0.1.0/24)   │  │
      │   │ Route: 0.0.0.0/0 → IGW   (jan26-public-rt)         │  │
      │   │                                                    │  │
      │   │    ┌───────────────┐    ┌───────────────┐          │  │
      │   │    │ jan26-bastion │    │  jan26-nat    │← EIP     │  │
      │   │    │ (Public IP)   │    │ (NAT Gateway) │          │  │
      │   │    │ SG: bastion-sg│    │               │          │  │
      │   │    └───────┬───────┘    └───────▲───────┘          │  │
      │   │            │                    │                  │  │
      │   └────────────┼────────────────────┼──────────────────┘  │
      │                │                    │                     │
      │                │ SSH                │ outbound only       │
      │                ▼                    │                     │
      │   ┌────────────┴────────────────────┴─────────────────┐  │
      │   │ Private Subnet: jan26-private-subnet (10.0.2.0/24)│  │
      │   │ Route: 0.0.0.0/0 → NAT (jan26-private-rt)         │  │
      │   │                                                   │  │
      │   │    ┌───────────────┐                              │  │
      │   │    │ jan26-private │                              │  │
      │   │    │ (No Public IP)│                              │  │
      │   │    │ SG: allow SSH │                              │  │
      │   │    │ from bastion  │                              │  │
      │   │    │ SG only       │                              │  │
      │   │    └───────────────┘                              │  │
      │   └───────────────────────────────────────────────────┘  │
      └──────────────────────────────────────────────────────────┘
## Traffic flows

| From | To | Path | Works? |
|---|---|---|---|
| My laptop | Bastion | Internet → IGW → Public RT → Public Subnet | ✅ |
| My laptop | Private EC2 (direct) | — (no public IP, no route) | ❌ |
| Bastion | Private EC2 | VPC internal (default local route) | ✅ |
| Private EC2 | Internet (outbound) | Private RT → NAT → IGW → Internet | ✅ |
| Internet | Private EC2 (inbound) | — (NAT is outbound-only, no inbound path) | ❌ |

## Security layers

1. **Route tables** — network-level. Private subnet has no route to IGW, only to NAT.
2. **Security groups** — instance-level stateful firewall. Bastion accepts SSH only from my IP. Private accepts SSH only from the bastion's security group.
3. **No public IP on private EC2** — physically can't be addressed from the internet.

