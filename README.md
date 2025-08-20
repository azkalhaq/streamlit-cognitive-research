# Streamlit App — Install & Open in Canvas (LMS)

A concise guide to install, run, deploy, and embed your Streamlit app inside Canvas (Instructure) for teaching/research use.

---

## 1) Prerequisites

* **Python** 3.10+ (3.11 recommended)
* **Git** (to clone your repo)
* **OpenAI API key** (if your app uses OpenAI) — keep it secret
* **Canvas access** with permission to add Modules/Pages

> **Tip:** If you don’t have admin rights in Canvas, ask your instructor/admin to add the external URL or embed for you.

---

## 2) Quick Start (Local)

```bash
# 1) Clone your repository
git clone <YOUR_REPO_URL>
cd <YOUR_REPO_FOLDER>

# 2) Create and activate a virtual env
# Windows (PowerShell)
python -m venv .venv
. .\.venv\Scripts\Activate.ps1

# macOS/Linux (bash/zsh)
python3 -m venv .venv
source .venv/bin/activate

# 3) Install dependencies
pip install -U pip
pip install -r requirements.txt

# 4) Set secrets (example for OpenAI)
# Windows (PowerShell)
$env:OPENAI_API_KEY="sk-..."

# macOS/Linux (bash/zsh)
export OPENAI_API_KEY="sk-..."

# 5) Run the app
streamlit run app.py
```

Your app will start on `http://localhost:8501`.

---

## 3) Configuration & Secrets

Use **Streamlit Secrets** in production (and keep them **out** of Git):

**Create** `.streamlit/secrets.toml` (do **not** commit):

```toml
OPENAI_API_KEY = "sk-..."
OPENAI_MODEL = "gpt-4o"  # optional
```

In your code:

```python
import os, streamlit as st
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
if not api_key:
    st.error("No OPENAI_API_KEY set. Add it to environment or .streamlit/secrets.toml")
    st.stop()

client = OpenAI(api_key=api_key)
```

Optional `.streamlit/config.toml`:

```toml
[server]
headless = true
port = 8501
address = "0.0.0.0"
enableCORS = true
enableXsrfProtection = true
[browser]
gatherUsageStats = false
```

**Common gotchas**

* Use `os.getenv("OPENAI_API_KEY")` (not `os.getenv["..."]`).
* Error `The api_key client option must be set...` ⇒ the env var name must be **OPENAI\_API\_KEY**.

---

## 4) Deploying (Get a Public HTTPS URL)

To embed in Canvas, your app needs a **public HTTPS** URL. Options:

### A) Streamlit Community Cloud (simple)

1. Push your app to GitHub.
2. Create an app from the repo.
3. Add secrets in the app settings.
4. Deploy → you’ll get a `https://your-app.streamlit.app` URL.

### B) Render / Railway / Fly.io / other PaaS

* Create a new **Web Service** pointing to your repo.
* Start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
* Add environment variables (e.g., `OPENAI_API_KEY`).

### C) Temporary tunnel (testing only)

```bash
# From a separate terminal
ngrok http 8501
```

Copy the public HTTPS URL from ngrok.

> **Security:** Never hard-code secrets in your repo. Use platform secrets or `st.secrets`.

---

## 5) Open **Inside Canvas** (Instructure)

You have three paths—pick the simplest that fits your needs.

### Option 1 — Add as an External URL (Module)

1. Deploy your app (get a public HTTPS URL).
2. Canvas → **Modules** → **+** → **External URL**.
3. Paste your app URL. For reliability, check **“Load in a new tab”**.

### Option 2 — Embed on a Canvas Page (iframe)

**Requirements:** Your app must allow being framed by your Canvas domain (e.g., `https://canvas.<youruni>.edu`). Modern browsers rely on **Content-Security-Policy** (`frame-ancestors`). Many servers set restrictive defaults.

**Recommended approach:** Put your Streamlit behind **Nginx** and set headers to allow Canvas framing.

**Nginx reverse-proxy example:**

```nginx
server {
    server_name your-app.example.com;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_set_header Host $host;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Allow embedding within Canvas
        proxy_hide_header X-Frame-Options;  # remove Streamlit's default if present
        add_header Content-Security-Policy "frame-ancestors 'self' https://<YOUR_CANVAS_DOMAIN>" always;
        add_header X-Frame-Options "ALLOW-FROM https://<YOUR_CANVAS_DOMAIN>" always; # legacy; CSP is authoritative
    }
}
```

Then in Canvas → **Pages** → **Edit** → **HTML Editor**, insert:

```html
<iframe src="https://your-app.example.com" width="100%" height="900" allow="clipboard-read; clipboard-write"></iframe>
```

> If you still see a blank frame or a refusal, your headers aren’t set correctly or your hosting platform injects stricter defaults. Check browser devtools → **Network** → Response headers.

### Option 3 — LTI 1.3 External Tool (advanced)

For SSO and course-aware context, wrap your app as an **LTI 1.3** tool using an LTI library (e.g., Node `ltijs`, Python `pylti1p3`). Steps (high level):

1. Host your app + LTI layer.
2. Create a **Developer Key** in Canvas; enter redirect/launch URLs.
3. Install the tool in the course (as an **External Tool**).
4. Validate launch flow; consume user/course claims as needed.

This is beyond a quick README—use only if you need deep Canvas integration.

---

## 6) Troubleshooting

* **`TypeError: 'function' object is not subscriptable`**

  * Use `os.getenv("VAR")`, not `os.getenv["VAR"]`.
* **`openai.OpenAIError: The api_key client option must be set...`**

  * Ensure the env var name is exactly `OPENAI_API_KEY`.
  * In Streamlit Cloud/Render, add it in the service’s **Environment/Secrets**.
* **Canvas shows a blank iframe**

  * Your app is blocking framing. Add `Content-Security-Policy: frame-ancestors 'self' https://<YOUR_CANVAS_DOMAIN>` at the proxy.
  * Remove/override `X-Frame-Options: DENY/SAMEORIGIN` with `proxy_hide_header` (Nginx) or equivalent.
* **Mixed content / not HTTPS**

  * Canvas pages are HTTPS; your app must also be HTTPS.
* **Port issues on PaaS**

  * Use `--server.address 0.0.0.0` and read `$PORT` if required by your host.

---

## 7) Project Layout (example)

```
.
├─ app.py
├─ requirements.txt
├─ README.md
└─ .streamlit/
   ├─ config.toml
   └─ secrets.toml   # DO NOT COMMIT
```

---

## 8) License

Add a license if you plan to share/distribute your code (e.g., MIT, Apache-2.0).

---

## 9) Credits

* Built with [Streamlit](https://streamlit.io)
* Integrates with OpenAI API (optional)
