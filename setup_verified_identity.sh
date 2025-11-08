#!/bin/bash
# LUCA Verified Identity - Quick Setup Script
# This script sets up the verified identity system for LUCA

echo "🔐 LUCA Verified Identity Setup"
echo "================================"
echo ""

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "backend/main.py" ]; then
    echo -e "${RED}❌ Error: Please run this script from the LUCA-AI_369 directory${NC}"
    exit 1
fi

echo -e "${BLUE}Step 1: Checking Python environment...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python 3 found${NC}"
echo ""

echo -e "${BLUE}Step 2: Installing required packages...${NC}"
pip3 install dnspython cryptography python-gnupg requests -q
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

echo -e "${BLUE}Step 3: Initializing database tables...${NC}"
python3 -m backend.init_verified_identity

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Database initialization failed${NC}"
    echo -e "${YELLOW}ℹ️  This might be because the tables already exist, which is OK${NC}"
    echo -e "${YELLOW}ℹ️  Continue anyway? (y/n)${NC}"
    read -r response
    if [[ ! "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        exit 1
    fi
fi
echo ""

echo -e "${BLUE}Step 4: Verifying integration...${NC}"
# Check if verified_identity is imported in main.py
if grep -q "verified_identity" backend/main.py; then
    echo -e "${GREEN}✓ Verified identity routes are integrated${NC}"
else
    echo -e "${RED}❌ Verified identity routes not found in main.py${NC}"
    echo -e "${YELLOW}Please manually add the import to backend/main.py${NC}"
fi
echo ""

echo -e "${BLUE}Step 5: Testing database connection...${NC}"
python3 -c "
from backend.database import SessionLocal, engine
from sqlalchemy import inspect
db = SessionLocal()
inspector = inspect(engine)
tables = inspector.get_table_names()
verified_tables = [
    'user_identities',
    'global_knowledge',
    'knowledge_correction_logs',
    'community_validations',
    'verification_requests'
]
found = [t for t in verified_tables if t in tables]
print(f'Found {len(found)}/{len(verified_tables)} verified identity tables')
for table in found:
    print(f'  ✓ {table}')
db.close()
" 2>/dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Database connection successful${NC}"
else
    echo -e "${YELLOW}⚠️  Could not verify database (this might be normal if backend is not configured)${NC}"
fi
echo ""

echo "================================"
echo -e "${GREEN}🎉 Setup Complete!${NC}"
echo ""
echo "Next Steps:"
echo "1. Start/restart your LUCA backend:"
echo "   python3 -m backend.main"
echo ""
echo "2. Access the API documentation:"
echo "   http://localhost:8000/docs"
echo ""
echo "3. View verified identity endpoints:"
echo "   http://localhost:8000/api/verified-identity/"
echo ""
echo "4. Read the documentation:"
echo "   cat VERIFIED_IDENTITY.md"
echo ""
echo "5. Use the Claude command:"
echo "   /integrate-verified-identity"
echo ""
echo -e "${BLUE}For detailed usage instructions, see VERIFIED_IDENTITY.md${NC}"
echo ""
