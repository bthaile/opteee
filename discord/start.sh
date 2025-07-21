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
echo "🔍 Testing network connectivity..."

# Run Discord connectivity test first
python test_discord_connection.py

echo "📡 Additional network diagnostics..."
echo "Current DNS servers:"
cat /etc/resolv.conf

# Try alternative DNS servers
echo "nameserver 8.8.8.8" > /tmp/resolv.conf.backup
echo "nameserver 1.1.1.1" >> /tmp/resolv.conf.backup
cp /etc/resolv.conf /etc/resolv.conf.original
cp /tmp/resolv.conf.backup /etc/resolv.conf

echo "Testing DNS with Google DNS..."
nslookup discord.com || echo "DNS lookup still failed"
ping -c 1 8.8.8.8 || echo "Internet connectivity test failed"
ping -c 1 discord.com || echo "Discord.com ping failed"

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