# Deployment Guide: Reflex on Vercel

Reflex applications consist of two parts: a **Next.js Frontend** and a **FastAPI Backend**. Vercel is optimized for the frontend, while the backend typically requires a persistent server or a cloud provider that supports Python.

## Step 1: Prepare your Backend

Since Vercel is primarily for static sites and serverless functions, the most reliable way to deploy a Reflex backend is using **Reflex Cloud**, **Railway**, or **Render**.

1.  **Reflex Cloud (Recommended):**
    - Run `reflex deploy` in your terminal. This handles both frontend and backend automatically.
2.  **External Host (Railway/Render):**
    - Create a new service from your GitHub repo.
    - Set the start command to: `reflex run --env prod --backend-only`.
    - Note your backend URL (e.g., `https://your-backend.railway.app`).

## Step 2: Deploy Frontend to Vercel

1.  **Export the Frontend:**
    In your local terminal, run:
    ```bash
    reflex export --frontend-only
    ```
    This creates a `frontend.zip` file containing the Next.js app.
2.  **Upload to GitHub:**
    Commit the changes and push them:
    ```bash
    git add .
    git commit -m "Add deployment guide"
    git push origin main
    ```
3.  **Vercel Setup:**
    - Go to [Vercel](https://vercel.com) and click **"Add New Project"**.
    - Import your `MusicTasteAnalyzer` repository.
    - **Environment Variables:** Add the following:
        - `API_URL`: The URL of your backend (from Step 1).
        - `SPOTIPY_CLIENT_ID`: Your Spotify Client ID.
        - `SPOTIPY_CLIENT_SECRET`: Your Spotify Client Secret.
        - `SPOTIPY_REDIRECT_URI`: Your production redirect URI (must match Spotify Dashboard).
4.  **Deploy:** Click **Deploy**.

## Step 3: Update Spotify Dashboard

Ensure your **Redirect URI** in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) matches your Vercel deployment URL (e.g., `https://your-app.vercel.app/callback`).

> [!IMPORTANT]
> Reflex state management relies on websockets. Ensure your backend host supports persistent websocket connections for the best experience.
