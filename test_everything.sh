#!/bin/bash
# Comprehensive LUCA Pipeline Test
# Tests EVERY component systematically

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         COMPREHENSIVE PIPELINE DIAGNOSTICS                   ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

test_component() {
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo -n "Testing $1... "
    if eval "$2" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ PASS${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        echo -e "${RED}❌ FAIL${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        echo "  Error output:"
        eval "$2" 2>&1 | head -5 | sed 's/^/    /'
        return 1
    fi
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. BACKEND TESTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

test_component "Backend imports" "python3 -c 'import sys; sys.path.insert(0, \"backend\"); from main import app'"
test_component "Backend database" "python3 -c 'import sys; sys.path.insert(0, \"backend\"); from database import get_db, engine'"
test_component "Backend models" "python3 -c 'import sys; sys.path.insert(0, \"backend\"); from models import User, ChatHistory'"
test_component "Backend routes" "python3 -c 'import sys; sys.path.insert(0, \"backend\"); from routes import auth_router, chat_router'"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2. FRONTEND TESTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

test_component "Frontend index.html exists" "test -f frontend/index.html"
test_component "Frontend chat.html exists" "test -f frontend/chat.html"
test_component "Frontend login.html exists" "test -f frontend/login.html"
test_component "Frontend dashboard exists" "test -f frontend/neurodiversity-dashboard.html"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3. LUCA CORE TESTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

test_component "LUCA Framework import" "python3 -c 'from luca import initialize_luca_system'"
test_component "LUCA Framework init" "python3 -c 'from luca import initialize_luca_system; luca = initialize_luca_system()'"
test_component "LUCA status report" "python3 -c 'from luca import initialize_luca_system; luca = initialize_luca_system(); status = luca.get_status_report()'"
test_component "LUCA quality score" "python3 -c 'from luca import initialize_luca_system; luca = initialize_luca_system(); assert luca.quality_score >= 369/370'"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4. INFO-BLOCK-ENGINE TESTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

test_component "Engine import" "python3 -c 'import sys; sys.path.insert(0, \"luca_369_370\"); from core import InfoBlockEngine'"
test_component "Engine init" "python3 -c 'import sys; sys.path.insert(0, \"luca_369_370\"); from core import InfoBlockEngine; engine = InfoBlockEngine()'"
test_component "Engine generate" "python3 -c 'import sys; sys.path.insert(0, \"luca_369_370\"); from core import InfoBlockEngine; engine = InfoBlockEngine(); blocks = engine.generate_response(\"test\")'"
test_component "Formatter import" "python3 -c 'import sys; sys.path.insert(0, \"luca_369_370\"); from core import BlockFormatter'"
test_component "Validator import" "python3 -c 'import sys; sys.path.insert(0, \"luca_369_370\"); from core import QualityValidator'"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5. INTEGRATION TESTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

test_component "Cross-system import" "python3 -c 'from luca import initialize_luca_system; import sys; sys.path.insert(0, \"luca_369_370\"); from core import InfoBlockEngine'"
test_component "Both systems work" "python3 -c 'from luca import initialize_luca_system; import sys; sys.path.insert(0, \"luca_369_370\"); from core import InfoBlockEngine; luca = initialize_luca_system(); engine = InfoBlockEngine()'"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "6. UNIT TESTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

test_component "Pytest available" "python3 -c 'import pytest'"
test_component "Info-Block tests" "python3 -m pytest luca_369_370/tests/test_info_blocks.py -q"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "7. DEMO TESTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

test_component "Framework demo exists" "test -f examples/framework_369_370_demo.py"
test_component "Info-Block demo exists" "test -f luca_369_370/examples/demo_responses.py"
test_component "Info-Block demo runs" "timeout 5 python3 luca_369_370/examples/demo_responses.py"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "8. SCRIPTS & UTILITIES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

test_component "Pipeline test exists" "test -f test_pipeline.py"
test_component "Start script exists" "test -f start_luca.sh"

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    TEST SUMMARY                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Total Tests: $TOTAL_TESTS"
echo -e "Passed:      ${GREEN}$PASSED_TESTS${NC}"
echo -e "Failed:      ${RED}$FAILED_TESTS${NC}"
echo ""

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║           ✅ ALL TESTS PASSED ✅                             ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
    exit 0
else
    echo -e "${RED}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║           ❌ SOME TESTS FAILED ❌                            ║${NC}"
    echo -e "${RED}╚══════════════════════════════════════════════════════════════╝${NC}"
    exit 1
fi
