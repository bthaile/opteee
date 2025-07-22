# Deploying OPTEEE Discord Bot to HuggingFace Spaces

This guide explains how to deploy the Discord bot as a **separate HuggingFace Space** that connects to your main OPTEEE API.

## 🎯 Architecture Overview

```
Discord Users
     ↓
Discord Bot (HF Space #2)
     ↓ API calls
OPTEEE Web App (HF Space #1)
```

##  Step-by-Step Setup

### 1. Create New HuggingFace Space for Discord Bot

1. Go to [HuggingFace Spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. **Space name**: `opteee-discord-bot` (or your preference)
4. **License**: Same as your main project
5. **SDK**: Docker
6. **Hardware**: CPU basic (free tier is sufficient)
7. Click **"Create Space"**

### 2. Configure HuggingFace Space Secrets

In your **new Discord bot Space** settings:

1. Go to **Settings** → **Variables and secrets**
2. Add the following **Repository secrets**:

```bash
# Required
DISCORD_TOKEN=your_discord_bot_token_here

# Optional (with defaults)
OPTEEE_API_URL=https://bthaile-opteee.hf.space
DEFAULT_PROVIDER=openai
DEFAULT_RESULTS=5
```

### 3. Set up GitHub Secrets

In your **GitHub repository** settings:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add these **Repository secrets**:

```bash
HF_TOKEN=your_huggingface_write_token
DISCORD_SPACE_NAME=bthaile/opteee-discord-bot
```

### 4. Copy Files to Root Directory

The GitHub Actions workflow is set up to deploy from the `discord/` directory. Make sure these files are present:

```
discord/
├── discord_bot.py           Main bot code
├── health_server.py         Health monitoring
├── start.sh                Startup script
├── Dockerfile              Container definition
├── requirements.txt        Python dependencies
├── README.md               HF Space metadata
└── .github/
    └── workflows/
        └── deploy-discord-bot.yml   Deployment workflow
```

### 5. Test Local Deployment (Optional)

Before deploying to HuggingFace, test locally:

```bash
cd discord/
docker build -t opteee-discord-bot .
docker run --env-file .env -p 8080:8080 opteee-discord-bot
```

Visit: `http://localhost:8080` - You should see the bot status page.

### 6. Deploy to HuggingFace

**Option A: Automatic (Recommended)**
```bash
# Any push to discord/ folder will trigger deployment
git add discord/
git commit -m "Update Discord bot"
git push
```

**Option B: Manual**
```bash
# Go to GitHub Actions tab → "Deploy Discord Bot to Hugging Face Space" → "Run workflow"
```

## 🎉 Post-Deployment

### Verify Deployment
1. Visit your HF Space URL: `https://huggingface.co/spaces/yourusername/opteee-discord-bot`
2. You should see the bot status page
3. Check the **Logs** tab for any errors

### Test Discord Bot
```bash
# In your Discord server
!health                                    # Test API connection
!search What is gamma in options trading?  # Test basic search functionality
!search_advanced 8 Explain covered calls  # Test advanced search with more results
```

## 🔧 Configuration Options

### Environment Variables (HF Space Secrets)

| Variable | Default | Description |
|----------|---------|-------------|
| `DISCORD_TOKEN` | **Required** | Discord bot token |
| `OPTEEE_API_URL` | `https://bthaile-opteee.hf.space` | Main API endpoint |
| `DEFAULT_PROVIDER` | `openai` | AI provider (openai/claude) |
| `DEFAULT_RESULTS` | `5` | Default search results |

### Monitoring

- **Bot Status**: `https://yourspace.hf.space/`
- **Health Check**: `https://yourspace.hf.space/health`
- **HF Logs**: Space → Logs tab
- **Discord Logs**: Check bot responses in Discord

## 🛠 Troubleshooting

### Common Issues

**Bot not responding in Discord:**
- Check HF Space logs for errors
- Verify `DISCORD_TOKEN` is set correctly
- Ensure bot has proper Discord permissions

**API connection failed:**
- Verify `OPTEEE_API_URL` points to your main API
- Test the main API health: `https://bthaile-opteee.hf.space/api/health`

**Deployment failed:**
- Check GitHub Actions logs
- Verify `HF_TOKEN` has write permissions
- Confirm `DISCORD_SPACE_NAME` is correct

### Getting Help

1. **HF Space Logs**: Check the Logs tab in your Space
2. **GitHub Actions**: Check workflow run logs
3. **Discord Bot Logs**: Use `!health` command to test connectivity

## ✨ Benefits of This Setup

 **Free Hosting**: Both services run free on HuggingFace  
 **Auto-Deployment**: GitHub push → automatic deployment  
 **Independent Scaling**: Each service manages its own resources  
 **Easy Monitoring**: Health endpoints and logging  
 **No Infrastructure**: HuggingFace handles everything  

Your Discord bot is now running as a completely separate service that connects to your main OPTEEE API!  