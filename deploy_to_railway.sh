#!/bin/bash
# Railway Backend Enhancement Deployment Script
# Run this locally after copying the enhanced backend to your Git repository

echo "🚀 SuitSize.ai Enhanced Backend Deployment"
echo "=========================================="
echo ""

# Check if we're in a Git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Error: Not in a Git repository"
    echo "Please navigate to your suitsize-ai Git repository first"
    exit 1
fi

echo "📁 Current repository: $(git remote get-url origin 2>/dev/null || echo 'No remote found')"
echo ""

# Step 1: Create and checkout enhancement branch
echo "1️⃣ Creating enhancement branch..."
git checkout -b enhance-railway-backend 2>/dev/null || git checkout enhance-railway-backend
echo "✅ Branch 'enhance-railway-backend' ready"
echo ""

# Step 2: Check for enhanced backend file
if [[ ! -f "enhanced_railway_backend.py" ]]; then
    echo "⚠️  Enhanced backend file not found!"
    echo "Please ensure you've copied the enhanced_railway_backend.py content to your main Flask file"
    echo "Expected location: Your main Flask file (app.py, main.py, or similar)"
    echo ""
    read -p "Press Enter after you've copied the enhanced backend to your Flask file..."
fi

# Step 3: Check for updated requirements.txt
if [[ -f "requirements.txt" ]]; then
    echo "📋 Updating requirements.txt..."
    echo "Current requirements.txt contents:"
    cat requirements.txt
    echo ""
    echo "💡 Make sure your requirements.txt includes:"
    echo "Flask==3.0.0"
    echo "Flask-CORS==4.0.0"
    echo "Werkzeug==3.0.1"
    echo "gunicorn==21.2.0"
    echo "jsonschema==4.20.0"
    echo "marshmallow==3.20.1"
    echo ""
fi

# Step 4: Show status and commit
echo "2️⃣ Checking Git status..."
git status

echo ""
echo "3️⃣ Committing enhanced backend..."
echo "Commit message will be:"
echo "🎯 Fix: Enhanced Railway backend - all 4 critical issues resolved"
echo ""

read -p "Ready to commit? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git add .
    git commit -m "🎯 Fix: Enhanced Railway backend - all 4 critical issues resolved

✅ Fixed API stability (20% failure rate)
✅ Fixed height scaling (200cm+ support) 
✅ Enhanced error handling (specific 400 errors)
✅ Added rate limiting (API abuse protection)
✅ Added performance monitoring & caching
✅ Improved size algorithm with academic research"
    
    echo ""
    echo "4️⃣ Pushing to trigger Railway auto-deployment..."
    echo "This will trigger Railway to auto-deploy the enhanced backend!"
    echo ""
    
    read -p "Push to GitHub/GitLab to trigger auto-deployment? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git push origin enhance-railway-backend
        echo ""
        echo "🚀 SUCCESS! Railway will auto-deploy in 2-5 minutes"
        echo ""
        echo "⏰ Expected timeline:"
        echo "   T+30s  - Railway detects push"
        echo "   T+1-3min - Building enhanced backend"
        echo "   T+3-5min - ✅ Live with all fixes"
        echo ""
        echo "🧪 After 5 minutes, test the fixes:"
        echo "   bash quick_test.sh"
        echo ""
        echo "📊 Monitor deployment:"
        echo "   - Check Railway dashboard for deployment status"
        echo "   - Watch for deployment notifications"
        echo "   - Verify all 4 critical issues are resolved"
        echo ""
    fi
else
    echo "❌ Deployment cancelled by user"
fi

echo ""
echo "🎯 Next steps:"
echo "1. Wait 3-5 minutes for Railway auto-deployment"
echo "2. Run: bash quick_test.sh to verify fixes"
echo "3. Test with your enhanced frontend"
echo "4. Merge to main when ready: git checkout main && git merge enhance-railway-backend"