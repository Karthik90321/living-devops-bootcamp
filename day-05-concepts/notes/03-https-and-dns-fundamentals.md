# HTTPS and DNS Fundamentals

How a browser actually loads `https://example.com`. This is what happens between the user hitting Enter and the page rendering.

## Part 1: DNS — finding the server

### The question
Browser needs to turn `example.com` into an IP address it can connect to.

### The resolution chain

1. **Browser cache** — was this domain resolved recently? If yes, use that IP.
2. **OS cache** — same check at the OS level.
3. **Local resolver** (usually your ISP or `8.8.8.8`/`1.1.1.1`). This is the workhorse.
4. If the resolver doesn't have it cached:
   - Ask a **root name server** — "who handles `.com`?"
   - Ask the **TLD name server** — "who handles `example.com`?"
   - Ask the **authoritative name server** (Route 53, Cloudflare, etc.) — "what's the A record for `example.com`?"
   - Get the IP back, cache it per the TTL.
5. Resolver returns the IP to the OS, which returns it to the browser.

### Key insight: recursive vs iterative

- **Recursive resolver** (your ISP's DNS) takes one question and walks the whole chain on your behalf.
- **Authoritative servers** only answer questions about their own zone and don't recurse.

### Why it matters for DevOps

- DNS changes don't propagate instantly — TTL governs how long old answers stay cached
- If your site's "broken" for some users but not others, DNS caching is often the cause
- `dig example.com` and `nslookup example.com` are the tools you'll use daily
- `dig +trace example.com` walks the full resolution chain so you can see where it breaks

## Part 2: TCP + TLS handshake — setting up the secure connection

Once the browser has the IP, it connects. For HTTPS this is a layered handshake.

### The TCP handshake (3 messages)

1. **Client → Server:** SYN — "I want to talk"
2. **Server → Client:** SYN-ACK — "OK, I hear you"
3. **Client → Server:** ACK — "Great, talking now"

TCP connection established. For plain HTTP, the browser starts sending the request right away.

### The TLS handshake (modern TLS 1.3, simplified)

1. **Client Hello** — browser sends supported cipher suites, a random number, and the server name it's asking about (SNI)
2. **Server Hello** — server picks a cipher, sends its **certificate**, its public key, and a random number
3. **Certificate verification** — browser validates the cert:
   - Is it signed by a trusted CA (Certificate Authority)?
   - Does the domain in the cert match the site I'm visiting?
   - Is it still valid (not expired)?
   - Has it been revoked?
4. **Key exchange** — both sides derive a shared symmetric key using their random numbers + the server's public key (Diffie-Hellman)
5. **Finished** — both sides send a message encrypted with the new key. If each can decrypt the other, the handshake is done.

From here on, all traffic is encrypted with the symmetric key.

### Why a symmetric key, not the public key?
Public-key crypto is slow. It's used only to securely establish a shared symmetric key, then the real traffic uses fast symmetric crypto (AES).

## Part 3: The certificate — the trust anchor

### What's in a TLS certificate?
- **Subject** — the domain(s) it covers (e.g., `example.com`, `*.example.com`)
- **Issuer** — which CA signed it (Let's Encrypt, DigiCert, AWS ACM...)
- **Public key** — the server's public key
- **Validity period** — start and end dates
- **Signature** — the CA's cryptographic sign-off

### How trust works
Your browser ships with a list of trusted root CAs. When a cert is signed by one of those (or a chain that leads back to one), it's trusted. If not, the browser shows the "not secure" warning.

### Free certs — Let's Encrypt
- Free, 90-day validity, auto-renewable
- Uses the ACME protocol — a bot on your server can request, validate, and renew certs automatically
- The 90-day window is intentional: short cert life = smaller blast radius if compromised

### AWS Certificate Manager (ACM)
- Free if you use the cert with AWS services (ALB, CloudFront, API Gateway)
- Not free to export for use outside AWS
- Auto-renews
- Validation is DNS-based (add a CNAME to prove ownership) or email-based

## Part 4: Encryption in transit vs encryption at rest

These solve different problems:

| | In transit | At rest |
|---|---|---|
| What it protects | Data moving over the network | Data stored on disk |
| Tool | TLS certificate, HTTPS | AES encryption, KMS |
| Keys managed by | Both endpoints (ephemeral session keys) | The storage system |
| Example | Browser ↔ Nginx ↔ Flask | EBS volume, S3 bucket, RDS DB |

**Critical:** a cert only secures the pipe. Once data lands on disk, that's an at-rest problem. Solve both.

## Part 5: Why Nginx sits in front of Flask

Akhilesh mentioned this in class. Summary:

- **Flask's dev server is not production-grade** — single-threaded, no TLS, no static file optimization.
- **Gunicorn** runs Flask in production — multi-worker, handles concurrency.
- **Nginx sits in front** because it:
  1. Terminates TLS (handles the cert, encryption)
  2. Serves static files (CSS, images, videos) far faster than Flask
  3. Buffers slow clients (prevents them from tying up Flask workers)
  4. Acts as a reverse proxy — one external endpoint, multiple backends
  5. Can compress responses, cache, rate-limit

So the stack is: `Browser → Nginx (port 443, TLS) → Gunicorn (localhost:8000) → Flask app`.

Traffic between Nginx and Gunicorn on the same machine doesn't need encryption — it never leaves the VM.

## The full flow, end-to-end

User types `https://example.com/products` and hits Enter:

1. Browser → DNS resolver: "what's the IP for `example.com`?"
2. DNS resolver walks the chain, returns `13.235.1.2`
3. Browser opens TCP connection to `13.235.1.2:443`
4. TCP handshake (3 messages)
5. TLS handshake — Nginx sends cert, browser validates, shared key established
6. Browser sends `GET /products` encrypted with the shared key
7. Nginx decrypts the request, proxies it to Gunicorn on `localhost:8000`
8. Gunicorn hands it to Flask
9. Flask returns HTML, Gunicorn returns it to Nginx
10. Nginx encrypts the response with the shared key and sends it back
11. Browser decrypts, renders the page

All of that in ~200ms. Wild.

## Interview questions

1. What's the difference between a recursive and an authoritative DNS server?
2. Your website loads for you but not for a colleague. What do you check first?
3. Walk me through what happens when a user visits `https://example.com`.
4. Why does HTTPS need both asymmetric and symmetric encryption?
5. When would you terminate TLS at the load balancer vs at the application?
6. What's the difference between Let's Encrypt and AWS Certificate Manager? When would you pick each?
7. Explain encryption in transit vs encryption at rest with a concrete example.

## Sources

- Byte Byte Go YouTube channel — "How HTTPS Works", "How DNS Works"
- Cloudflare Learning Center — DNS and SSL articles
- Let's Encrypt documentation — certificate lifecycle