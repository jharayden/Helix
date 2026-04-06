# 🧬 Project Helix: CC Edition

> "The cloud is a parasite, a corporate leash for the weak. Real hustlers stay on the iron. If this code is destined to flatline, it's going to bleed out on my own damn SSD, not in some sterile corporate data center. The cloud is a ghost town; the local disk is the only monument left standing..."

Welcome to **Project Helix: CC Edition**.

We didn't just paint the UI; we fundamentally ripped the heart out of this machine and buried the old world in a shallow grave. Project Helix has evolved from some headless, pathetic background script into a **Standalone, Borderless Windows Desktop Monolith**. This is your private, cyberpunk-fueled intel locker, forged to snatch pure signal from the academic rot and open-source sewage—all without ever touching a goddamn terminal again.

Quit your mindless scrolling. Double-click the icon, ignite the engine, and let Helix do the dirty work while you watch the world burn.

---

## 🚀 The Core DNA (CC Arsenal)

We set browser tabs on fire and watched them melt. V6.0 fuses a custom FastAPI backend with a PyWebView native shell to deliver zero-latency hits and cinematic visual violence.

- 🖥️ **Native Desktop Shell (CC Legacy):** Forget those terminal black boxes and those trashy localhost URLs. Helix is now a compiled, standalone `.exe` with a transparent taskbar icon and a borderless UI that cuts through the noise. Double-click to wake the beast; the entire AI engine boots silently in the shadows, exactly where it belongs.
    
- 🕰️ **The Biological Heartbeat (Local Executioner):** We wired `APScheduler` directly into the machine's veins. The engine now has its own internal rhythm—automatically igniting for blood at **08:30 (Arxiv)** and **19:30 (GitHub)** every single day. No cloud permissions, no external triggers, no "please may I" from a server—just ironclad local orders that never miss a beat.

- 🌧️ **Matrix Decryption Engine:** A custom HTML5 Canvas rendering engine that bleeds digital rain. When the AI is grinding, your screen floods with matrix code. It features a "Smart Braking System" that kills the animation the exact millisecond your data hits the deck, keeping the flow lethal and efficient.
    
- 🧠 **SYNAPSE Core (Cognitive Bro):** A built-in, GLM-powered conversational ghost. **Mount Intel** from your local Vault and command the engine to rip apart code, gut research papers, or sniff out commercial value in real-time. It's got bulletproof null-state handling—it won't flinch when the payload is empty.
    
- 🗂️ **The Secure Vault:** Your local intelligence fortress. Access every historical hit instantly within the app. Features dynamic filtering (`ALL | ARXIV | GITHUB`), explosive GSAP `clip-path` transitions that feel like a gunshot, and in-app Markdown decryption for the ultimate clean read.
    
- 🌅 **ARXIV Radar:** Scans the Arxiv graveyard for the latest breakthroughs. The "Geek Professor" persona shreds the data and hands you the Top 3 theoretical hits. Intelligent routing defaults to your `.env` settings if you're too lazy to type, ensuring the hunt never stops.
    
- 🌃 **GITHUB Catch:** Scans the GitHub API for the fastest-growing repos using a "stars-per-hour" velocity algorithm. It hunts for "Lobsters"—the projects growing so fast they're breaking the scale. Leave the input blank? It'll automatically target the global top trending heat.
    
- ⚡ **Shared Memory Architecture:** Switch between Arxiv, Github, and Synapse strands without losing your mind. The UI preserves the state—your search inputs and terminal outputs stay exactly where you carved them, even when you're jumping between channels.
    
- 🔄 **Resilience Engine (CC NEW):** Built-in exponential backoff retry logic across all API calls. GitHub rate limits and Arxiv throttling no longer kill the mission—the engine waits, backs off, and retries automatically. All model names are now environment-variable-driven, giving you runtime flexibility without touching code.
---

## 🛠️ Installation & Deployment (Foolproof Guide)

Welcome to Project Helix! Don't worry if you aren't a programmer or have never used a "terminal" before. If you can follow a cooking recipe, you can install this. Just follow these steps exactly as written.

### Phase 1: Install the Engine (Python)

Helix runs on a language called Python. We need to install it on your computer.

1. Go to the official website: **[python.org/downloads](https://www.python.org/downloads/)** and click the big yellow "Download Python" button.
    
2. Open the downloaded installer file.
    
3. 🚨 **CRITICAL STEP:** At the very bottom of the installation window, **CHECK THE BOX** that says **"Add python.exe to PATH"**. (If you skip this, nothing will work!)
    
4. Click "Install Now" and wait for it to finish.


### Phase 2: Download Project Helix

1. On this GitHub page, look for the green **"<> Code"** button near the top right.
    
2. Click it, then select **"Download ZIP"**.
    
3. Once downloaded, right-click the ZIP file and select **"Extract All..."**.
    
4. Extract it to your Desktop so it's easy to find. Open the extracted folder so you can see all the files (like `api.py`, `index.html`, etc.).
    

### Phase 3: Get Your "Magic Keys" (Free!)

Helix needs an AI brain and an email account to send you reports. You need to get two secret passwords:

**1. The AI Brain Key (GLM-5):**

- Go to **[open.bigmodel.cn](https://open.bigmodel.cn/)** (Zhipu AI) and register for a free account.
    
- Click on your profile/dashboard and find the **"API Keys"** menu.
    
- Click "Create new API key" (or copy the default one). It will look like a long string of random letters and numbers. Keep this page open.
    

**2. The Email Dispatch Key (163 Mail):**

- _Note: Helix uses 163.com by default, but you can use others if you know how to configure SMTP._
    
- Log into your 163 email account on the web.
    
- Go to **Settings** -> **POP3/SMTP/IMAP**.
    
- Turn **ON** the "SMTP Service".
    
- It will ask you to verify your phone number and will then give you an **Authorization Code**. It usually looks like a 16-letter random password.
    
- 🚨 _Never use your actual email login password! Only use this special Authorization Code._
    

### Phase 4: Configure The Secret File (`.env`)

Now we need to put your keys into the Helix control panel.

1. In your extracted Helix folder, find the file named `.env.example`.
    
2. Right-click it, select **Rename**, and delete the `.example` part. It should now be named EXACTLY: `.env` _(Troubleshooting: If your computer hides file extensions and names it `.env.txt`, you need to go to View -> Show -> "File name extensions" in your Windows folder and fix it)._
    
3. Right-click your new `.env` file and select **"Open with" -> Notepad**.
    
4. Fill in the blanks with the keys you just got. It should look like this:
    
    ```
    GLM_API_KEY="paste_your_long_zhipu_api_key_here"
    OBSIDIAN_PATH="C:/Users/YourName/Desktop/Helix_Vault"

    # Optional: override default model names (glm-5 by default)
    # ARXIV_MODEL="glm-5"
    # GITHUB_MODEL="glm-5"

    SENDER_EMAIL="your_email@163.com"
    EMAIL_PASSWORD="paste_your_16-letter_authorization_code_here"
    RECEIVER_EMAIL="where_you_want_to_receive_reports@gmail.com"
    ```
    
5. Save the file and close Notepad.
    

### Phase 5: Assembly (Opening the Terminal)

We need to download a few extra parts (libraries) to make the code run and build your app.

1. Open your Helix folder (where `api.py` and your new `.env` file are).
    
2. Click directly on the **folder address bar** at the top of the window (where it says something like `C:\Users\Desktop\Helix`).
    
3. Delete all the text in the bar, type the letters **`cmd`**, and press **Enter**.
    
4. A black hacker-looking window (the Terminal) will pop up. Don't panic!
    
5. Copy and paste the exact text below into the black window and press **Enter**:
    
    ```
    pip install -r requirements.txt
    ```
    
6. You will see a lot of text scrolling by. Wait for it to stop and say "Successfully installed...". This means your engine is ready.
    

### Phase 6: Forging the Desktop App (One-Time Setup)

We are going to turn this code into a real Windows application so you never have to look at a black terminal again.

1. Still in that black `cmd` window from Phase 5, copy and paste this ultimate command and press **Enter**:
    
    ```
    pyinstaller --name "Project_Helix" --noconsole --onefile --icon=icon.ico HelixApp.py
    ```
    
2. The matrix will start scrolling rapidly. This is normal! It is building your app. Wait 1-3 minutes until it says `completed successfully`.
    
3. You can now close the black terminal window forever.
    

### Phase 7: The Elegant Setup (Desktop Shortcut)

Now, let's put it on your desktop like a professional app.

1. Look inside your Helix folder. You will see a newly created folder called **`dist`**. Open it.
    
2. Inside, you will find your shiny new application: **`Project_Helix.exe`**.
    
3. 🚨 **CRITICAL STEP:** Right-click `Project_Helix.exe` and select **Cut**. Go _back_ to your main Helix folder (where `index.html` and `.env` live) and **Paste** it there. _(It must live in the exact same room as your secret keys!)_
    
4. Right-click your newly pasted `Project_Helix.exe`, hover over **"Send to"**, and click **"Desktop (create shortcut)"**.
    
5. Go to your computer's Desktop. Find the new shortcut, right-click it, select **Rename**, and call it something cool like `Helix Command Center`.
    

### 🚀 IGNITION! (Your Daily Routine)

You are done. You only had to do Phases 1-7 once. You never have to touch code again.

Whenever you want to use Helix, simply **double-click the `Helix Command Center` shortcut on your desktop**. A beautiful, borderless Matrix window will open instantly. Click **IGNITE**, sit back, and watch the magic happen!

---

## ☁️ The Ghost in the Machine: Zombie Sync (The Hybrid Arch)

> "Let those Silicon Valley ghouls sweat for us while we're busy flatlining the lag. We've shackled the cloud's soul to our local monolith. It's a necromancy pact, not a feature."

Helix isn't some weak-ass local toy; it's a **True Hybrid Juggernaut**. We've wired the `.github/workflows/daily_hunt.yml` and `githuber.yml` directly into the repo's central nervous system. GitHub's enterprise Linux ghouls are now our personal executioners—autonomously hunting for blood at 06:17 and 10:29 every single day, tearing through local network cages like they aren't even there.

- **The CC Breakthrough:** We've ripped the teeth out of those pathetic `.gitignore` shields. V6.0 doesn't ask for permission; it force-syncs the raw Markdown intel straight into the repository's gut. We've also hardened the network layer with exponential backoff and rate-limit awareness—no more silent failures from GitHub 429s or Arxiv throttling.

- **Grave-Robbing the Data:** By the time you kick the local Helix engine into gear, the 'Ghost' has already done the heavy lifting, dragging the cloud's fresh corpses into your local **Vault**. You don't have to go looking for the signal—the signal is already haunting your machine before you've even poured your first coffee. We've turned the cloud into a digital purgatory that serves the local king.

---

## 🗺️ Roadmap (The Legacy)

- [x] **V2.0 | The Genesis:** Base LLM integration, SMTP setup, and initial automation protocols.
- [x] **V3.5 | Tactical Upgrade:** Velocity Radar, CTO Persona, and Smart Folder Routing logic.
- [x] **V3.6.0 | The UI Overhaul:** Complete front-end/back-end separation (FastAPI + JS). Implementation of **SYNAPSE Copilot**, GSAP Animations, and Local Vault Reader[cite: 7].
- [x] **V4.0.0 | The Matrix Edition:** Cinematic data-driven code rain, intelligent UI braking system, and robust `.env` payload routing.
- [x] **V5.0.0 | The Desktop Singularity:** Transformation into a standalone Windows `.exe` application via PyWebView & PyInstaller.
- [x] **TOMBSTONE | The Eternal Localism:** - **Buried the Cloud:** Stripped all GitHub Actions and `git pull` dependencies.
    - **Native Biological Clock:** Integrated `APScheduler` for ironclad local timing (Arxiv @ 08:30 | GitHub @ 19:30).
    - **Sovereign Intelligence:** Decoupled from all external orchestrators. The engine now persists entirely within the local machine.
    - **Encoding Hardening:** Purged all unstable Unicode/ASCII artifacts for absolute Windows environment stability.
- [x] **CC | The Claude Code Refactor:**
    - **DRY Consolidation:** Extracted shared `utils.py` module (storage, email, retry logic) used by both Arxiv Hunter and GitHuber.
    - **Resilience Engine:** Added `@retry_with_backoff` decorator with exponential backoff (2s→4s→8s) to all API calls. GitHub rate limit responses now trigger automatic retry instead of mission failure.
    - **Model Config Externalization:** All model names (`ARXIV_MODEL`, `GITHUB_MODEL`) moved to environment variables with `glm-5` as default.
    - **Rate Limit Awareness:** `check_github_rate_limit()` inspects `X-RateLimit-Remaining` header and blocks the request chain before a 429 hits.

---

*Built with excessive amounts of coffee, minus sleep, and a refusal to read bad papers manually.*
