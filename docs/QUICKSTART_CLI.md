# Quick start: new site from template (CLI)

Short path to a new static site on Cloudron Surfer using this template, **GitHub CLI (gh)**, and the **local/** config. Use this when you want one new GitHub repo per site and to configure deploy from the command line.

---

## Prerequisites

- **GitHub account** and **GitHub CLI** installed and logged in (`gh auth login`).
- **Cloudron** with a **Surfer** app installed and a domain assigned.
- **Surfer access token:** In the Surfer app open `https://<your-domain>/_admin/` → Settings → Access Token → create and copy the token.

---

## 1. Create a new repo from this template

Either use the GitHub website or the CLI.

**Option A — GitHub website**

- On the template repo page, click **Use this template** → **Create a new repository**. Name it (e.g. `my-site`), create it, then clone:

  ```bash
  git clone https://github.com/YOUR_USERNAME/my-site.git
  cd my-site
  ```

**Option B — GitHub CLI**

- Replace `YOUR_USERNAME` and `TEMPLATE_REPO` with the template owner and repo name (e.g. the org or user who owns this template and the repo name).

  ```bash
  gh repo create my-site --template YOUR_USERNAME/TEMPLATE_REPO --clone --private
  cd my-site
  ```

---

## 2. Add your site content

Put your static site in **`public/`** (e.g. extract a theme or template zip into `public/`, or replace `public/index.html` and add pages). Optional: run **`./build.sh`** if you use Chatwoot or banner ads.

---

## 3. Configure deploy from local files

1. **Copy the sample files** (remove the `.sample` suffix):

   ```bash
   cp local/surfer-token.sample local/surfer-token
   cp local/site-url.txt.sample local/site-url.txt
   ```

2. **Edit the files** (use Cursor or any editor):

   - **`local/surfer-token`** — One line: the Surfer access token you copied from the Surfer app.
   - **`local/site-url.txt`** — One line: your site URL, e.g. `https://yourdomain.com`.

3. **Run the setup script** (sets the GitHub repo secret and variable for Actions):

   ```bash
   ./scripts/setup-deploy.sh
   ```

   You should see: `Setting GitHub repository secret SURFER_TOKEN and variable SURFER_SERVER...` and then `Done. You can push to main/master to deploy.`

---

## 4. Deploy

If you added or changed files:

```bash
git add .
git commit -m "Add site and configure deploy"
git push -u origin main
```

If you are only deploying the placeholder (no content changes), the clone already has the template commit — just run:

```bash
git push -u origin main
```

(Use `master` if your default branch is `master`.)

GitHub Actions will run the **Deploy to Surfer** workflow and upload **`public/`** to your Surfer app. The site will be live at the URL in **`local/site-url.txt`**.

---

## Summary

| Step | What you do |
|------|----------------|
| 1 | Create new repo from template (web or `gh repo create ... --template ...`), clone, `cd` into it. |
| 2 | Add content to `public/`. Optionally run `./build.sh`. |
| 3 | Copy `local/*.sample` to `local/surfer-token` and `local/site-url.txt`, edit with your token and URL, run `./scripts/setup-deploy.sh`. |
| 4 | Commit, push to `main` (or `master`). Actions deploys to Surfer. |

The files **`local/surfer-token`** and **`local/site-url.txt`** are gitignored and never committed. Only the setup script reads them to configure the repo once.
