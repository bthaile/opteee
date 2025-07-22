#!/bin/bash

echo " OPTEEE - HuggingFace Deployment Test Environment"
echo "================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_step() {
    echo -e "${BLUE}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN} $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check prerequisites
print_step "Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi
print_success "Docker is installed"

if ! command -v python &> /dev/null; then
    print_error "Python is not installed. Please install Python 3.9+ first."
    exit 1
fi
print_success "Python is installed"

# Step 1: Create .env file if it doesn't exist
print_step "Setting up environment variables..."

if [ ! -f .env ]; then
    print_warning ".env file not found. Creating template..."
    cat > .env << 'EOF'
# API Keys for OPTEEE Application
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here
CLAUDE_API_KEY=your-claude-api-key-here

# Application Settings
PORT=7860
PYTHONPATH=/app
EOF
    print_warning "Created .env template. Please add your actual API keys before proceeding."
    echo "You can get your API keys from:"
    echo "  - OpenAI: https://platform.openai.com/api-keys"
    echo "  - Anthropic: https://console.anthropic.com/"
    echo ""
    echo "Press any key to continue once you've added your API keys..."
    read -n 1 -s
else
    print_success "Found .env file"
fi

# Check if API keys are set
source .env
if [[ "$OPENAI_API_KEY" == "your-openai-api-key-here" ]]; then
    print_warning "OpenAI API key not set in .env file"
fi

# Step 2: Prepare production files (simulate GitHub Actions)
print_step "Preparing production files (simulating GitHub Actions)..."

# Create startup script exactly like GitHub Actions
print_step "Creating startup.sh script..."
cat > startup.sh << 'EOF'
#!/bin/bash
set -e

echo "===== Starting application ====="
date

# Print environment for debugging
echo "Current directory: $(pwd)"
echo "Current user: $(whoami)"

# Run the FastAPI application
python main.py
EOF

chmod +x startup.sh
print_success "Created startup.sh script"

# Update README for HuggingFace (simulate GitHub Actions)
print_step "Creating HuggingFace README..."
cat > README.md << 'EOF'
---
title: opteee
emoji: 🔥
colorFrom: blue
colorTo: red
sdk: docker
app_port: 7860
pinned: false
env:
  - PYTHONPATH=/app
---

# Options Trading Knowledge Search

This application provides semantic search across a collection of options trading transcripts and videos.

## Features

- Semantic search using sentence-transformers
- FAISS vector database for fast retrieval
- Direct links to specific timestamps in relevant videos
EOF

print_success "Created HuggingFace README.md"

# Step 3: Stop any existing containers
print_step "Stopping any existing containers..."
docker stop opteee-hf-test 2>/dev/null || true
docker rm opteee-hf-test 2>/dev/null || true
print_success "Cleaned up existing containers"

# Step 4: Build Docker image exactly like HuggingFace
print_step "Building Docker image (exactly like HuggingFace deployment)..."
docker build -t opteee-hf-test . --no-cache

if [ $? -eq 0 ]; then
    print_success "Docker image built successfully"
else
    print_error "Docker build failed"
    exit 1
fi

# Step 5: Run the container exactly like HuggingFace
print_step "Starting application (exactly like HuggingFace environment)..."

docker run -d \
    --name opteee-hf-test \
    -p 7860:7860 \
    --env-file .env \
    opteee-hf-test

if [ $? -eq 0 ]; then
    print_success "Container started successfully"
else
    print_error "Container failed to start"
    exit 1
fi

# Step 6: Wait for application to start
print_step "Waiting for application to initialize..."
sleep 10

# Step 7: Test the application
print_step "Testing the application..."

echo ""
echo "🧪 Running health checks..."

# Test health endpoint
health_response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:7860/api/health)
if [ "$health_response" = "200" ]; then
    print_success "Health check passed"
else
    print_error "Health check failed (HTTP $health_response)"
fi

# Test frontend
frontend_response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:7860)
if [ "$frontend_response" = "200" ]; then
    print_success "Frontend accessible"
else
    print_error "Frontend not accessible (HTTP $frontend_response)"
fi

# Test chat API
echo ""
echo "🤖 Testing chat API..."
chat_response=$(curl -s -X POST http://localhost:7860/api/chat \
    -H "Content-Type: application/json" \
    -d '{"query":"What are call options?","provider":"openai","num_results":3}')

if [ $? -eq 0 ]; then
    print_success "Chat API responded"
    echo "Sample response preview:"
    echo "$chat_response" | python -m json.tool | head -20
else
    print_error "Chat API failed"
fi

# Step 8: Show logs
echo ""
print_step "Showing application logs..."
docker logs --tail=50 opteee-hf-test

# Step 9: Final status
echo ""
echo "================================================="
echo "🎉 HuggingFace Test Environment Ready!"
echo ""
echo "Your application is running at: http://localhost:7860"
echo "API documentation: http://localhost:7860/docs"
echo ""
echo "This matches exactly how HuggingFace will deploy your app."
echo ""
echo "Commands to manage the test environment:"
echo "  • View logs:     docker logs -f opteee-hf-test"
echo "  • Stop app:      docker stop opteee-hf-test"
echo "  • Remove app:    docker rm opteee-hf-test"
echo "  • Rebuild:       docker build -t opteee-hf-test . --no-cache"
echo ""
echo "If everything works here, it will work on HuggingFace! " 