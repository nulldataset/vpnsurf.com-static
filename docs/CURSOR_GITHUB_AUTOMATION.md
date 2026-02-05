# Cursor IDE and GitHub automation

This doc explains how to get **GitHub CLI (`gh`)** working so that scripts in this repo can create repos and configure GitHub Actions when you work in **Cursor IDE**.

---

## The sticking point

**Cursor’s “connected to GitHub” (your account link) does not log in the GitHub CLI.**

- Cursor uses its own GitHub connection for things like Copilot, repo access, or signing in.
- The **`gh`** command in the terminal is a separate program. It does not automatically use Cursor’s GitHub account.
- So in Cursor’s terminal you often see: `You are not logged into any GitHub hosts. To log in, run: gh auth login`.

Scripts that use **`gh`** (e.g. **`./scripts/setup-deploy.sh`** and **`./scripts/create-repo-and-deploy.sh`**) need **`gh`** to be authenticated. Until that’s done, “create repo” and “configure deploy” from the CLI will fail.

---

## What needs to work

For full automation from this repo you need **`gh`** to be able to:

1. **Create a repo** — `gh repo create ...`
2. **Set a secret** — `gh secret set SURFER_TOKEN`
3. **Set a variable** — `gh variable set SURFER_SERVER`
4. **Push** — `git push` (uses git credentials, not necessarily `gh`)

So **`gh`** must be logged in (or given a token) in the environment where you run the scripts (e.g. Cursor’s terminal).

---

## Option A — Log in with GitHub CLI once

In a terminal (Cursor’s terminal or your system terminal):

```bash
gh auth login
```

Follow the prompts (browser or token). After that, **`gh`** is logged in for that machine/user, and scripts that use **`gh`** will work in that same environment.

---

## Option B — Use a token (good for automation / Cursor)

If you don’t want to run **`gh auth login`** interactively (e.g. in Cursor or in a script):

1. Create a **Personal Access Token** on GitHub:
   - **GitHub → Settings → Developer settings → Personal access tokens**
   - Create a token with **`repo`** scope (so it can create repos and set secrets/variables).

2. In the same environment where you run the scripts, set:
   ```bash
   export GH_TOKEN=your_token_here
   ```
   You can put this in your shell profile or set it once per terminal session.

3. Then run:
   ```bash
   gh auth status
   ```
   It should show you as logged in. After that, **`./scripts/create-repo-and-deploy.sh`** and **`./scripts/setup-deploy.sh`** can run without interactive login.

---

## One-shot: create repo + configure deploy + push

After **`gh`** is authenticated (Option A or B), from the **repo root**:

1. Ensure **`local/surfer-token`** or **`local/surfer-token.txt`** contains your Surfer access token (one line).
2. Ensure **`local/site-url.txt`** contains your site URL (e.g. `https://yourdomain.com`).
3. Run:
   ```bash
   ./scripts/create-repo-and-deploy.sh [REPO_NAME]
   ```
   If you omit **REPO_NAME**, the script uses the current directory name (e.g. **vpnsurf.com-static**).

The script will:

- Create the GitHub repo (if there is no **origin** remote) and add **origin**.
- Run **`./scripts/setup-deploy.sh`** to set **SURFER_TOKEN** and **SURFER_SERVER** in the repo.
- Push to **main** (or **master**), which triggers the **Deploy to Surfer** workflow.

If **origin** already exists, it skips repo creation and only runs the deploy setup and push.

---

## Summary

| Goal                         | What to do |
|-----------------------------|------------|
| Use scripts that call **`gh`** in Cursor | Log in once with **`gh auth login`** or set **`GH_TOKEN`** in the environment where you run the scripts. |
| Create repo + configure Actions + push  | Run **`./scripts/create-repo-and-deploy.sh`** after **`gh`** is authenticated and **local/** is filled. |
| Only set SURFER_TOKEN + SURFER_SERVER   | Run **`./scripts/setup-deploy.sh`** (repo must already exist and have **origin**). |

Cursor being “connected to GitHub” is separate from **`gh`**; for automation you need **`gh`** authenticated as above.
