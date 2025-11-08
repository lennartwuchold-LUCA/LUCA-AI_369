# Quick Start: LUCA Verified Identity

Get verified identity up and running in 5 minutes!

## 🚀 One-Command Setup

```bash
./setup_verified_identity.sh
```

This script will:
- ✅ Check dependencies
- ✅ Install required packages
- ✅ Initialize database tables
- ✅ Verify integration
- ✅ Test database connection

## 📋 Manual Setup (Alternative)

If you prefer to set up manually:

### 1. Install Dependencies

```bash
pip install dnspython cryptography python-gnupg requests
```

### 2. Initialize Database

```bash
python -m backend.init_verified_identity
```

### 3. Restart Backend

```bash
python -m backend.main
```

## 🎯 Verify It's Working

### Check API Docs

Visit: http://localhost:8000/docs

Look for `/api/verified-identity` endpoints.

### Test the API

```bash
# Health check
curl http://localhost:8000/health

# Get system info (should show "Verified Identity System")
curl http://localhost:8000/api/info
```

### Admin Statistics (requires auth)

```bash
# Login as admin first
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@luca-ai.com",
    "password": "Ypsilon369Admin!"
  }'

# Use the token to get statistics
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/verified-identity/admin/statistics
```

## 📖 Usage Examples

### Example 1: Verify Your GitHub Profile

```bash
# 1. Get instructions
curl -X POST http://localhost:8000/api/verified-identity/verification/instructions \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"method": "github", "identifier": "your-username"}'

# Response will include a verification token like "luca-verify-abc123"

# 2. Add the token to your GitHub bio at github.com/settings/profile

# 3. Verify
curl -X POST http://localhost:8000/api/verified-identity/verification/public-profile \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "github",
    "username": "your-username"
  }'
```

### Example 2: Update Global Knowledge

```bash
# After verification, update knowledge about yourself
curl -X POST http://localhost:8000/api/verified-identity/knowledge/update \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "subject_type": "person",
    "subject_identifier": "you@example.com",
    "knowledge_scope": "professional",
    "knowledge_key": "current_role",
    "knowledge_value": "LUCA AI Developer",
    "source_url": "https://github.com/your-username"
  }'
```

### Example 3: Search Global Knowledge

```bash
# No auth required for search
curl "http://localhost:8000/api/verified-identity/knowledge/search?query=LUCA&limit=10"
```

## 🔍 Troubleshooting

### "Module not found" error

```bash
# Make sure you're in the LUCA-AI_369 directory
cd /home/user/LUCA-AI_369

# Reinstall dependencies
pip install -r requirements.txt
```

### Tables not created

```bash
# Delete database and reinitialize
rm luca.db
python -m backend.database  # Initialize base tables
python -m backend.init_verified_identity  # Initialize verified identity tables
```

### Port already in use

```bash
# Kill existing process
pkill -f uvicorn

# Or use a different port
PORT=8080 python -m backend.main
```

### API returns 404

Make sure `backend/main.py` includes:

```python
from backend.routes import verified_identity
app.include_router(verified_identity.router)
```

## 📚 Learn More

- **Full Documentation**: `VERIFIED_IDENTITY.md`
- **API Reference**: http://localhost:8000/docs
- **Claude Command**: Run `/integrate-verified-identity` in Claude

## 🎓 Next Steps

1. **Verify Your Identity**: Try one of the verification methods
2. **Update Knowledge**: Add correct information about yourself
3. **Explore the API**: Check out all endpoints in Swagger UI
4. **Read the Docs**: Deep dive into `VERIFIED_IDENTITY.md`

## 💡 Quick Tips

- **Start Simple**: Begin with GitHub verification (easiest)
- **Provide Evidence**: Always include source URLs
- **Be Patient**: DNS verification can take up to 48 hours
- **Ask Admin**: Complex verifications may need admin approval
- **Community**: Validate others' contributions for higher trust score

## 🆘 Need Help?

- Check `VERIFIED_IDENTITY.md` for detailed guides
- View API docs at http://localhost:8000/docs
- Run the Claude command: `/integrate-verified-identity`

---

**Built with ❤️ by the LUCA AI Community**

*"Flow over Force - Let Truth Emerge Naturally"*
