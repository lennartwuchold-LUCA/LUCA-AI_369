# LUCA Verified Identity System

## 🔐 Overview

The LUCA Verified Identity System enables users to verify their identity and correct global knowledge about themselves. This prevents misinformation, reduces knowledge fragmentation, and empowers people to control their own information in the AI ecosystem.

## 🎯 Core Principles

### Philosophy

> **"Flow over Force"** - Verification is voluntary, organic, and user-driven

The system is built on these principles:

1. **Privacy by Design**: Only with explicit, verifiable identity
2. **Facts, Not Opinions**: Clear scope for factual information only
3. **Transparency**: Complete audit trail of all corrections
4. **Community Validation**: Public figures can be validated by community
5. **Self-Sovereignty**: Individuals control their own information

### The 3-6-9 Rule

```
if identification == true → global_knowledge_update_enabled
```

Only verified identities can update global knowledge. This simple rule prevents spam, ensures accountability, and maintains data quality.

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    LUCA Verified Identity                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────┐  ┌──────────────────┐  ┌─────────────┐ │
│  │ Verification   │  │ Global Knowledge │  │ Transparency│ │
│  │ Layer          │  │ Base             │  │ Log         │ │
│  │                │  │                  │  │             │ │
│  │ • Domain       │  │ • Personal Facts │  │ • Who       │ │
│  │ • Signature    │  │ • Professional   │  │ • What      │ │
│  │ • Public       │  │ • Public Stmt    │  │ • When      │ │
│  │   Profile      │  │ • Corrections    │  │ • Why       │ │
│  │ • Biometric    │  │                  │  │             │ │
│  │ • Community    │  │                  │  │             │ │
│  └────────────────┘  └──────────────────┘  └─────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │            Community Validation Layer                  │ │
│  │  • Confirm • Dispute • Request Evidence               │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                 Trust Score System                     │ │
│  │  Increases: Accurate corrections, confirmations       │ │
│  │  Decreases: Disputed corrections, false info          │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Database Schema

#### Core Tables

1. **user_identities**
   - Stores verified identity information
   - Links to verification method and proof
   - Tracks trust score and verification status

2. **global_knowledge**
   - Global knowledge base
   - Versioned entries (history preserved)
   - Community validation counters
   - Confidence scores

3. **knowledge_correction_logs**
   - Immutable audit trail
   - Complete transparency
   - Evidence and reasoning

4. **community_validations**
   - Community consensus
   - Weighted by trust scores
   - Dispute resolution

5. **verification_requests**
   - Pending admin reviews
   - Manual verification workflow

## 🔍 Verification Methods

### 1. Domain Verification

**Use Case**: Organizations, professionals with websites

**Process**:
1. User claims `example.com`
2. System generates token: `luca-verify-abc123`
3. User adds verification via:
   - **DNS TXT record**: `_luca-verification.example.com TXT "luca-token=abc123"`
   - **Well-known file**: `https://example.com/.well-known/luca-verification.txt`
4. System verifies automatically

**Proof**: Public DNS/HTTP accessible

**Trust Level**: High (cryptographically verifiable)

### 2. Cryptographic Signature (SSH/PGP)

**Use Case**: Developers, security professionals, privacy advocates

**Process**:
1. User requests signature verification
2. System provides message including user_id and timestamp
3. User signs with private key:
   ```bash
   # SSH example
   echo "LUCA Verification: user_id=123 timestamp=1234567890" | \
     ssh-keygen -Y sign -f ~/.ssh/id_rsa -n luca

   # PGP example
   echo "LUCA Verification: user_id=123 timestamp=1234567890" | \
     gpg --clearsign
   ```
4. User submits public key + signature
5. System verifies cryptographically

**Proof**: Mathematical cryptography

**Trust Level**: Highest (non-repudiable)

### 3. Public Profile Verification

**Use Case**: Public figures, professionals with established presence

**Supported Platforms**:
- GitHub (via bio or gist)
- LinkedIn (manual review)
- Twitter/X (manual review)
- Personal websites

**Process**:
1. User selects platform and username
2. System generates verification token
3. User posts token on public profile
4. System verifies via API or manual review

**Proof**: Public social proof

**Trust Level**: Medium-High (depends on platform)

### 4. Community Validation

**Use Case**: Public figures, well-known individuals

**Process**:
1. Multiple verified users vouch for identity
2. Community validates through existing connections
3. Weighted voting based on trust scores
4. Admin final approval

**Proof**: Social consensus

**Trust Level**: Medium (requires multiple validators)

### 5. Biometric/Government ID

**Use Case**: High-security requirements (future)

**Process**: Integration with third-party verification services (Veriff, IDology, etc.)

**Proof**: Government documents + biometric matching

**Trust Level**: Highest (legal identity)

## 📊 Knowledge Scopes

Verified users can update knowledge in these scopes:

### 1. Personal Facts

Objective, verifiable information:
- Birth date, location
- Education history
- Current affiliations
- Contact information

**Example**:
```json
{
  "knowledge_key": "current_affiliation",
  "knowledge_value": "LUCA AI Research Team",
  "source_url": "https://luca-ai.com/team"
}
```

### 2. Professional

Work-related information:
- Employment history
- Publications
- Patents
- Professional credentials

**Example**:
```json
{
  "knowledge_key": "publication",
  "knowledge_value": "Co-author of 'Consciousness in AI Systems' (2024)",
  "source_url": "https://arxiv.org/abs/example"
}
```

### 3. Public Statements

Corrections to misquotes or misattributions:
- Actual quotes vs. misquotes
- Positions on public issues
- Public announcements

**Example**:
```json
{
  "knowledge_key": "quote_correction",
  "knowledge_value": "I said 'AI should augment humans' not 'AI will replace humans'",
  "reason": "Correcting widely circulated misquote"
}
```

### 4. Corrections

Fixing misinformation:
- False claims
- Outdated information
- Incorrect attributions

**Example**:
```json
{
  "knowledge_key": "false_claim_correction",
  "knowledge_value": "I never worked at Company X, this is false information",
  "reason": "Correcting false employment claim",
  "evidence_urls": ["https://linkedin.com/in/myprofile"]
}
```

### 5. Preferences

Personal preferences:
- Preferred name/pronouns
- Preferred contact methods
- Privacy preferences

**Example**:
```json
{
  "knowledge_key": "preferred_name",
  "knowledge_value": "Alex (not Alexander)",
  "reason": "Personal preference"
}
```

## 🔒 Security & Privacy

### Privacy Protections

1. **Opt-in Only**: No verification without explicit user action
2. **Minimal Data**: Only collect necessary information
3. **User Control**: Users can revoke verification anytime
4. **Scope Limits**: Only factual information, not opinions
5. **Transparency**: All changes publicly logged

### Security Measures

1. **Cryptographic Verification**: Domain, signature verification
2. **Time-bound Tokens**: Verification tokens expire
3. **Audit Trails**: Immutable correction logs
4. **Trust Scores**: Prevent abuse through reputation
5. **Admin Oversight**: Manual review for sensitive cases

### Data Handling

- **Storage**: SQLite database (can migrate to PostgreSQL)
- **Encryption**: HTTPS for all API calls
- **Access Control**: JWT authentication required
- **Retention**: Indefinite (for transparency), user can request deletion
- **Export**: Users can export their verification data

## 🌐 Global Knowledge API

### For Developers

Query global knowledge in your applications:

```python
import requests

# Search for knowledge
response = requests.get(
    "http://localhost:8000/api/verified-identity/knowledge/search",
    params={"query": "LUCA AI", "limit": 10}
)

# Get specific subject
response = requests.get(
    "http://localhost:8000/api/verified-identity/knowledge/subject/user@example.com"
)

# View correction history (transparency)
response = requests.get(
    "http://localhost:8000/api/verified-identity/knowledge/corrections",
    params={"subject_identifier": "user@example.com"}
)
```

### For AI Systems

Integrate verified knowledge into AI responses:

```python
from backend.services.knowledge_service import KnowledgeService

# In your AI prompt construction:
knowledge = service.get_knowledge("user@example.com")

system_prompt = f"""
You are LUCA AI. When discussing {subject}, use this verified information:

{format_knowledge(knowledge)}

This information was verified by the subject themselves on {verified_date}.
Confidence score: {confidence_score}
Community validations: {validations}
"""
```

## 🎯 Use Cases

### 1. Personal Knowledge Management

**Scenario**: Individual wants to correct Wikipedia-style misinformation

**Process**:
1. Verify identity via domain or signature
2. Submit correction with evidence
3. Correction logged in transparency trail
4. AI systems can reference verified information

**Impact**: Reduced misinformation, self-sovereignty

### 2. Professional Credentials

**Scenario**: Academic wants to verify publications and affiliations

**Process**:
1. Verify via university domain or ORCID
2. Update publication list, current position
3. Link to authoritative sources

**Impact**: Accurate professional information

### 3. Public Figure Correction

**Scenario**: Public figure frequently misquoted in media

**Process**:
1. Verify via public profile (Twitter, GitHub)
2. Submit correct quotes with context
3. Community validates
4. AI systems cite verified statements

**Impact**: Reduced misquotations, authentic voice

### 4. Decentralized Identity (Meshtastic)

**Scenario**: User in offline mesh network needs verified identity

**Process**:
1. Verify Meshtastic node ID cryptographically
2. Tie node to verified identity
3. Trusted mesh communication

**Impact**: Secure offline identity

## 📈 Trust Score System

### How Trust Scores Work

- **Initial Score**: 0.5 (neutral)
- **Range**: 0.0 (untrusted) to 1.0 (highly trusted)

### Score Increases

- ✅ Accurate correction confirmed by community (+0.05)
- ✅ Evidence-backed update (+0.03)
- ✅ Self-correction of own information (+0.02)
- ✅ Validation from high-trust users (+0.04)

### Score Decreases

- ❌ Correction disputed by multiple users (-0.10)
- ❌ False information submitted (-0.20)
- ❌ Spam or abuse (-0.30)
- ❌ Validation from low-trust users (-0.05)

### Trust Levels

| Score | Level | Permissions |
|-------|-------|-------------|
| 0.0 - 0.3 | Untrusted | View only |
| 0.3 - 0.5 | Low Trust | Update own info only |
| 0.5 - 0.8 | Trusted | Update own info, validate others |
| 0.8 - 1.0 | Highly Trusted | Update own + contribute to public knowledge |

## 🚀 Integration Guide

### Quick Start

```bash
# 1. Initialize database
python -m backend.init_verified_identity

# 2. Update main.py
# Add: from backend.routes import verified_identity
# Add: app.include_router(verified_identity.router)

# 3. Restart backend
python -m backend.main

# 4. Test API
curl http://localhost:8000/api/verified-identity/admin/statistics
```

### Frontend Integration

Create a verification UI:

```javascript
// Request verification instructions
const response = await fetch('/api/verified-identity/verification/instructions', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    method: 'domain',
    identifier: 'example.com'
  })
});

const { token: verificationToken, instructions } = await response.json();

// Display instructions to user
// User completes verification steps

// Verify
const verifyResponse = await fetch('/api/verified-identity/verification/domain', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    domain: 'example.com',
    verification_token: verificationToken
  })
});
```

### Consciousness Integration

Integrate with LUCA's consciousness system:

```python
# In consciousness/core.py
from backend.services.knowledge_service import KnowledgeService

def enhance_response_with_verified_knowledge(self, response, context):
    """Enhance AI response with verified knowledge"""

    # Extract entities mentioned
    entities = self.extract_entities(response)

    # Get verified knowledge
    knowledge_service = KnowledgeService(self.db)

    for entity in entities:
        knowledge = knowledge_service.get_knowledge(entity)
        if knowledge:
            # Add verified information to response
            response = self.inject_verified_facts(response, knowledge)

    return response
```

## 🎓 Best Practices

### For Users

1. **Use Strongest Verification**: Prefer cryptographic methods
2. **Provide Evidence**: Always include source URLs
3. **Be Specific**: Clear, factual updates only
4. **Stay Current**: Update information when it changes
5. **Community**: Validate others' contributions

### For Developers

1. **Check Confidence Scores**: Use high-confidence knowledge
2. **Cite Sources**: Always reference verification source
3. **Handle Disputes**: Show when information is disputed
4. **Respect Privacy**: Don't expose verification methods
5. **Rate Limit**: Prevent abuse of API

### For Admins

1. **Review Carefully**: Verify evidence before approving
2. **Communicate**: Provide clear feedback on rejections
3. **Monitor Trust**: Watch for score manipulation
4. **Resolve Disputes**: Mediate community conflicts
5. **Update Policies**: Evolve with community needs

## 📚 Examples

### Example 1: Developer Verification

```bash
# 1. Get verification instructions
curl -X POST http://localhost:8000/api/verified-identity/verification/instructions \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"method": "github", "identifier": "username"}'

# Response: {"token": "luca-verify-abc123", ...}

# 2. Add to GitHub bio
# Go to github.com/settings/profile
# Add "luca-verify-abc123" to bio

# 3. Verify
curl -X POST http://localhost:8000/api/verified-identity/verification/public-profile \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"provider": "github", "username": "username"}'

# 4. Update knowledge
curl -X POST http://localhost:8000/api/verified-identity/knowledge/update \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "subject_type": "person",
    "subject_identifier": "user@example.com",
    "knowledge_scope": "professional",
    "knowledge_key": "github_profile",
    "knowledge_value": "github.com/username - 500+ contributions",
    "source_url": "https://github.com/username"
  }'
```

### Example 2: Domain Owner Verification

```bash
# 1. Get DNS instructions
curl -X POST http://localhost:8000/api/verified-identity/verification/instructions \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"method": "domain", "identifier": "example.com"}'

# 2. Add DNS TXT record
# _luca-verification.example.com TXT "luca-token=xyz789"

# 3. Wait for DNS propagation (up to 48 hours)
# Check: dig _luca-verification.example.com TXT

# 4. Verify
curl -X POST http://localhost:8000/api/verified-identity/verification/domain \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"domain": "example.com", "verification_token": "luca-verify-xyz789"}'
```

## 🔮 Future Enhancements

### Planned Features

1. **OAuth Integration**: Google, Microsoft, Apple Sign In
2. **Blockchain Proofs**: Ethereum, Solana identity
3. **Decentralized Identity**: DID, Verifiable Credentials
4. **AI Verification**: AI-assisted fraud detection
5. **Multi-party Validation**: Require N of M validators
6. **Expiring Knowledge**: Time-bound information
7. **Delegation**: Authorize others to update on your behalf
8. **Webhooks**: Notify on knowledge changes

### Research Areas

- **Privacy-Preserving Verification**: Zero-knowledge proofs
- **Reputation Systems**: Advanced trust algorithms
- **Dispute Resolution**: AI-mediated conflict resolution
- **Cross-Platform Identity**: Portable verification across systems

## 🤝 Community

### Contributing

We welcome contributions:

1. **Bug Reports**: Open issues on GitHub
2. **Feature Requests**: Propose new verification methods
3. **Code**: Submit PRs for improvements
4. **Documentation**: Help improve guides

### Governance

- **Community-Driven**: Major decisions by community vote
- **Transparent**: All decisions logged publicly
- **Evolving**: System adapts to user needs

## 📖 References

- **Decentralized Identity**: https://www.w3.org/TR/did-core/
- **Verifiable Credentials**: https://www.w3.org/TR/vc-data-model/
- **Web PKI**: https://tools.ietf.org/html/rfc5280
- **OAuth 2.0**: https://oauth.net/2/

## 📜 License

This verified identity system is part of LUCA AI and follows the same license.

---

**Built with ❤️ by the LUCA AI Community**

*"Flow over Force - Let Truth Emerge Naturally"*

---

## Support

- **Documentation**: This file
- **API Reference**: http://localhost:8000/docs
- **Issues**: GitHub Issues
- **Community**: LUCA AI Discord/Forum

---

Last Updated: 2025-11-08
Version: 3.6.9.alpha
