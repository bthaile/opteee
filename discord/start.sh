#!/bin/bash

echo "🚀 Starting OPTEEE Discord Bot Health Server..."

# Start the health server in the background
python health_server.py &
HEALTH_PID=$!

echo "✅ Health server started (PID: $HEALTH_PID)"

# Wait a moment for health server to initialize
sleep 2

echo "🤖 Starting Discord bot..."

# Test network connectivity
echo "🔍 DNS and network check..."

# Check DNS configuration
echo "DNS servers:"
cat /etc/resolv.conf

# Test DNS resolution manually
echo "Testing Discord DNS resolution:"
nslookup discord.com || echo "nslookup not available"

# Quick connectivity test
python test_discord_connection.py || echo "Network test completed"

echo "📡 Starting Discord bot with DNS fix applied..."

# Start the Discord bot in the foreground
python discord_bot.py &
BOT_PID=$!

echo "✅ Discord bot started (PID: $BOT_PID)"

# Function to handle cleanup on exit
cleanup() {
    echo "🛑 Shutting down services..."
    kill $HEALTH_PID 2>/dev/null
    kill $BOT_PID 2>/dev/null
    wait $HEALTH_PID 2>/dev/null
    wait $BOT_PID 2>/dev/null
    echo "✅ Cleanup completed"
    exit 0
}

# Set up signal handling
trap cleanup SIGTERM SIGINT

echo "🎉 All services running!"
echo "   Health server: http://localhost:${PORT:-8080}"
echo "   Discord bot: Connected to Discord"
echo ""
echo "Use Ctrl+C to stop all services"

# Wait for both processes
wait $BOT_PID 