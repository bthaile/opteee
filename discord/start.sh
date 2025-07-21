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

# Check current DNS configuration
echo "Current DNS servers:"
cat /etc/resolv.conf

# Try to configure reliable DNS servers (may fail if read-only)
echo "Attempting to configure DNS servers..."
if ! echo "nameserver 8.8.8.8" > /etc/resolv.conf 2>/dev/null; then
    echo "⚠️ Cannot modify /etc/resolv.conf - using system DNS"
else
    echo "nameserver 8.8.4.4" >> /etc/resolv.conf
    echo "nameserver 1.1.1.1" >> /etc/resolv.conf
    echo "✅ DNS servers configured"
    echo "Updated DNS servers:"
    cat /etc/resolv.conf
fi

# Test DNS resolution manually
echo "Testing Discord DNS resolution:"
NSLOOKUP_OUTPUT=$(nslookup discord.com 2>&1)
echo "$NSLOOKUP_OUTPUT"

# Check if nslookup actually resolved (not just returned exit code 0)
if echo "$NSLOOKUP_OUTPUT" | grep -q "No answer\|can't find\|NXDOMAIN\|not found"; then
    echo "❌ DNS resolution failed - server responds but no answer for discord.com"
    
    # Try adding Discord IPs to /etc/hosts as fallback
    echo "Attempting to add Discord IPs to /etc/hosts..."
    if echo "162.159.133.233 discord.com" >> /etc/hosts 2>/dev/null; then
        echo "162.159.134.233 gateway.discord.gg" >> /etc/hosts 2>/dev/null
        echo "162.159.135.233 discordapp.com" >> /etc/hosts 2>/dev/null
        echo "✅ Added Discord IPs to /etc/hosts"
        echo "Updated /etc/hosts entries:"
        grep discord /etc/hosts || echo "No Discord entries found"
        echo "Testing resolution after hosts update:"
        getent hosts discord.com || echo "getent failed"
        nslookup discord.com || echo "nslookup still using DNS server"
    else
        echo "⚠️ Cannot modify /etc/hosts - will attempt direct IP connection"
        echo "Current /etc/hosts permissions:"
        ls -la /etc/hosts
    fi
elif echo "$NSLOOKUP_OUTPUT" | grep -q "Address:.*[0-9]"; then
    echo "✅ DNS lookup successful - Discord resolved to IP"
else
    echo "⚠️ DNS lookup unclear - will attempt connection anyway"
fi

# Quick connectivity test
python test_discord_connection.py || echo "Network test completed"

echo "📡 Starting Discord bot with DNS configuration..."

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