# Streamlit App


## 1) Prerequisites

* **Python** 3.10+ (3.11 recommended)
* **Git** (to clone your repo)
* **OpenAI API key** (if your app uses OpenAI) — keep it secret
* **Canvas access** with permission to add Modules/Pages

> **Tip:** If you don’t have admin rights in Canvas, ask your instructor/admin to add the external URL or embed for you.

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

App will start on `http://localhost:8501`.



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



## 4) Project Layout (example)

```
.
├─ app.py
├─ requirements.txt
├─ README.md
└─ .streamlit/
   ├─ config.toml
   └─ secrets.toml   # DO NOT COMMIT
```



## 5) License

Add a license if you plan to share/distribute your code (e.g., MIT, Apache-2.0).



## 6) Credits

* Built with [Streamlit](https://streamlit.io)
* Integrates with OpenAI API (optional)
