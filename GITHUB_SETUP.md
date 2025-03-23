# Setting Up GitHub Actions for Hugging Face Deployment

This repository includes a GitHub Actions workflow to automatically deploy to Hugging Face Spaces.

## Setup Instructions

1. **Generate a Hugging Face Access Token**:
   - Go to https://huggingface.co/settings/tokens
   - Click "New token"
   - Set a name (e.g., "GitHub Actions")
   - Select "Write" access
   - Click "Generate token"
   - Copy the token immediately (you won't be able to see it again)

2. **Add the Token to GitHub Secrets**:
   - Go to your GitHub repository
   - Click "Settings" > "Secrets and variables" > "Actions"
   - Click "New repository secret"
   - Name: `HF_TOKEN`
   - Value: paste your Hugging Face token
   - Click "Add secret"

3. **Verify Workflow File**:
   - The workflow file is located at `.github/workflows/deploy-to-huggingface.yml`
   - Make sure the `SPACE_NAME` in the workflow file matches your Hugging Face Space: "bthaile/opteee"

4. **Push to GitHub**:
   - When you push to the `main` branch, the workflow will automatically run
   - You can also manually trigger the workflow from the "Actions" tab on GitHub

5. **Check Deployment Status**:
   - Go to the "Actions" tab on GitHub to see workflow status
   - If successful, your code will be deployed to your Hugging Face Space

## Troubleshooting

- **Error: "Permission denied"**: Check that your Hugging Face token has write access
- **Error: "Repository not found"**: Verify the `SPACE_NAME` in the workflow file
- **Error: "Unable to checkout"**: Make sure your repository includes the vector store data

## Important Notes

- This workflow uses `--force` to push, which will overwrite any changes made directly on Hugging Face
- Make sure to commit and push your vector store data to GitHub for it to be deployed 