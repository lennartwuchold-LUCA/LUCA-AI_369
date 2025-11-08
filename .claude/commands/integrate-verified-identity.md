---
description: Integrate verified identity system into LUCA admin interface
tags: [admin, identity, verification]
---

# Integrate Verified Identity System

This command integrates the verified identity system into your LUCA admin interface.

## What This Does

1. Initializes verified identity database tables
2. Registers verified identity API routes
3. Sets up admin dashboard for verification management
4. Enables global knowledge update capabilities

## Prerequisites

- LUCA backend is installed and running
- You have admin access (admin@luca-ai.com or custom admin account)
- Database is accessible

## Steps to Integrate

### 1. Initialize Database Tables

```bash
cd /home/user/LUCA-AI_369
python -m backend.init_verified_identity
```

This will create the following tables:
- `user_identities` - Verified identity records
- `global_knowledge` - Global knowledge base
- `knowledge_correction_logs` - Transparency audit trail
- `community_validations` - Community consensus validation
- `verification_requests` - Pending admin reviews

### 2. Update Backend Main File

Add verified identity routes to `backend/main.py`:

```python
# Add this import at the top
from backend.routes import verified_identity

# Add this after existing router includes
app.include_router(verified_identity.router)
```

### 3. Restart Backend

```bash
# Kill existing backend if running
pkill -f "uvicorn"

# Start backend
cd /home/user/LUCA-AI_369
python -m backend.main
```

### 4. Verify Integration

Test the API endpoints:

```bash
# Check health
curl http://localhost:8000/health

# Check verified identity routes (should return 401 if not authenticated)
curl http://localhost:8000/api/verified-identity/admin/statistics
```

## API Endpoints

### User Verification

- `POST /api/verified-identity/verification/instructions` - Get verification instructions
- `POST /api/verified-identity/verification/domain` - Verify domain ownership
- `POST /api/verified-identity/verification/signature` - Verify cryptographic signature
- `POST /api/verified-identity/verification/public-profile` - Verify public profile
- `GET /api/verified-identity/verification/status` - Get verification status

### Knowledge Management

- `POST /api/verified-identity/knowledge/update` - Update global knowledge (verified users only)
- `GET /api/verified-identity/knowledge/search` - Search global knowledge
- `GET /api/verified-identity/knowledge/subject/{identifier}` - Get knowledge about subject
- `GET /api/verified-identity/knowledge/corrections` - View correction history
- `POST /api/verified-identity/knowledge/validate` - Community validation

### Admin Endpoints

- `GET /api/verified-identity/admin/verification-requests` - View pending verifications
- `POST /api/verified-identity/admin/review-verification` - Approve/reject verification
- `GET /api/verified-identity/admin/statistics` - Admin dashboard statistics

## Verification Methods

### 1. Domain Verification

**User Process:**
1. User requests verification for `example.com`
2. System provides verification token: `luca-verify-abc123`
3. User adds DNS TXT record OR creates well-known file:
   - DNS: `_luca-verification.example.com TXT "luca-token=luca-verify-abc123"`
   - File: `https://example.com/.well-known/luca-verification.txt` containing token
4. User clicks "Verify"
5. System automatically approves if token found

### 2. Cryptographic Signature (SSH/PGP)

**User Process:**
1. User requests signature verification
2. System provides message to sign
3. User signs with SSH or PGP key:
   ```bash
   # SSH
   echo "message" | ssh-keygen -Y sign -f ~/.ssh/id_rsa -n luca

   # PGP
   echo "message" | gpg --clearsign
   ```
4. User submits public key + signature
5. System automatically verifies and approves

### 3. Public Profile (GitHub, LinkedIn, etc.)

**User Process:**
1. User requests GitHub verification
2. System provides token: `luca-verify-xyz789`
3. User adds token to GitHub bio OR creates public gist
4. User clicks "Verify"
5. System checks GitHub API and auto-approves

### 4. Manual Review (Admin)

For methods requiring manual review:
1. User submits verification request with proof
2. Admin reviews in dashboard
3. Admin approves or rejects with notes

## Global Knowledge Updates

Once verified, users can update global knowledge about themselves:

**Example Use Cases:**

1. **Correct Personal Information**
   ```json
   {
     "subject_type": "person",
     "subject_identifier": "user@example.com",
     "knowledge_scope": "personal_facts",
     "knowledge_key": "current_affiliation",
     "knowledge_value": "LUCA AI Research",
     "reason": "Correcting outdated information"
   }
   ```

2. **Update Professional Info**
   ```json
   {
     "subject_type": "person",
     "subject_identifier": "example.com",
     "knowledge_scope": "professional",
     "knowledge_key": "publications",
     "knowledge_value": "Author of 'LUCA: A New Paradigm'",
     "source_url": "https://example.com/publications"
   }
   ```

3. **Correct Public Statements**
   ```json
   {
     "subject_type": "person",
     "subject_identifier": "user@example.com",
     "knowledge_scope": "corrections",
     "knowledge_key": "misquote_correction",
     "knowledge_value": "I never said X, the correct quote is Y",
     "reason": "Correcting widely circulated misquote"
   }
   ```

## Transparency & Audit Trail

All knowledge corrections are logged in `knowledge_correction_logs`:

- Who made the correction (identity_id)
- What was changed (old_value → new_value)
- When it was changed (timestamp)
- Why it was changed (reason)
- Evidence provided (evidence_urls)

Query the transparency log:
```
GET /api/verified-identity/knowledge/corrections?subject_identifier=user@example.com
```

## Community Validation

Public knowledge can be validated by the community:

- **Confirm**: Agree with the information
- **Dispute**: Disagree and provide counter-evidence
- **Request Evidence**: Ask for supporting documentation

Confidence scores are calculated based on:
- Number of confirmations vs disputes
- Trust score of validators (weighted voting)
- Quality of evidence provided

## Trust Scores

Each verified identity has a trust score (0.0 - 1.0):

- **Initial**: 0.5 (neutral)
- **Increases**: Accurate corrections, community confirmations
- **Decreases**: Disputed corrections, false information

Users with trust score < 0.8 cannot update others' information (only their own).

## Admin Dashboard

Monitor the system:

```bash
# Get statistics
curl -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  http://localhost:8000/api/verified-identity/admin/statistics

# View pending verifications
curl -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  http://localhost:8000/api/verified-identity/admin/verification-requests
```

## Security Considerations

1. **Privacy by Design**: Only verified users can update knowledge
2. **Explicit Consent**: Users must actively verify their identity
3. **Transparency**: All corrections are publicly logged
4. **Community Governance**: Disputed information flagged for review
5. **Scope Limitation**: Only facts, not opinions

## Philosophy Integration

This system embodies LUCA's core principles:

- **3-6-9**: `if identification == true → global_knowledge_update_enabled`
- **Flow over Force**: Organic, voluntary verification
- **Symbiosis**: Global knowledge benefits everyone
- **Resonance**: Truth emerges through community consensus

## Troubleshooting

**Tables not created:**
```bash
# Check database
python -c "from backend.database import engine; from sqlalchemy import inspect; print(inspect(engine).get_table_names())"

# Re-run initialization
python -m backend.init_verified_identity
```

**Routes not found:**
```bash
# Check if route is registered
curl http://localhost:8000/docs
# Look for /api/verified-identity endpoints in Swagger UI
```

**Verification fails:**
- Check DNS propagation (may take up to 48 hours)
- Verify file is accessible publicly
- Check signature format and timestamp

## Next Steps

1. Create frontend UI for verification (see `frontend/verified_identity.html` template)
2. Set up email notifications for verification approvals
3. Integrate with LUCA consciousness system
4. Add Meshtastic node verification for mesh networks

---

**Status**: ✅ Verified Identity System Ready

For more information, see `VERIFIED_IDENTITY.md`
