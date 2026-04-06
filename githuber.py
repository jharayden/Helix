import os
import requests
import datetime
from dotenv import load_dotenv
from typing import Dict, Any
from openai import OpenAI

from utils import (
    ObsidianFileStorage,
    EmailDispatcher,
    retry_with_backoff,
    check_github_rate_limit
)

# Load environment variables
load_dotenv()

# Bypass system proxies that might block the API
os.environ["NO_PROXY"] = "*"


class GitHuber:
    """
    V3.5 Microservice: GitHuber (The Open Source Trend Hunter)
    """
    def __init__(self):
        print("[SYSTEM] GitHuber Instantiated: Sensor Array Online.")
        api_key = os.getenv("GLM_API_KEY")
        if not api_key:
            raise ValueError("[FATAL] GLM_API_KEY not found in .env file.")

        self.client = OpenAI(api_key=api_key, base_url="https://open.bigmodel.cn/api/paas/v4/")
        # Model name loaded from env, defaults to glm-5 (matching Arxiv Hunter)
        self.model_name = os.getenv("GITHUB_MODEL", "glm-5")
        print(f"[SYSTEM] GitHuber model: {self.model_name}")

    def _build_headers(self) -> dict:
        """Build GitHub API request headers, optionally with auth token."""
        headers = {"Accept": "application/vnd.github.v3+json"}
        github_token = os.getenv("GITHUB_TOKEN")
        if github_token:
            headers["Authorization"] = f"token {github_token}"
        return headers

    @retry_with_backoff(max_retries=3, initial_delay=2.0, backoff_factor=2.0)
    def hunt_top_lobster(self, query: str = "") -> Dict[str, Any]:
        """
        Phase 1: Sensor Layer. Scans for new repos in the last 7 days,
        calculates velocity, and locks onto the Top 1.
        """
        print("\n[SENSOR LAYER] Scanning GitHub for the fastest-growing 'Lobster' in the last 7 days...")

        now = datetime.datetime.now(datetime.timezone.utc)
        seven_days_ago = (now - datetime.timedelta(days=7)).strftime('%Y-%m-%d')

        if query:
            final_query = f"created:>{seven_days_ago} {query}"
            print(f"[SENSOR LAYER] Target Override: Hunting for '{query}'...")
        else:
            final_query = f"created:>{seven_days_ago} ai OR agent OR automation OR plugin OR workflow"

        url = "https://api.github.com/search/repositories"
        params = {
            "q": final_query,
            "sort": "stars",
            "order": "desc",
            "per_page": 30
        }

        headers = self._build_headers()

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()

            # Check rate limit before proceeding
            is_limited, remaining = check_github_rate_limit(response.headers)
            if is_limited:
                raise Exception(f"GitHub API rate limit critical: only {remaining} requests remaining.")

            data = response.json()
            items = data.get("items", [])

            if not items:
                print("[ERROR] No targets found in the current window.")
                return {}

            print("[SENSOR LAYER] Applying Velocity Algorithm to top 30 targets...")

            best_repo = None
            max_velocity = -1.0

            for repo in items:
                created_at = datetime.datetime.fromisoformat(repo["created_at"].replace("Z", "+00:00"))
                hours_alive = (now - created_at).total_seconds() / 3600.0
                velocity = repo["stargazers_count"] / (hours_alive + 1.0)

                if velocity > max_velocity:
                    max_velocity = velocity
                    best_repo = repo

            if not best_repo:
                return {}

            print(f"[SENSOR LAYER] Target Locked: {best_repo['full_name']}")
            print(f"               |> Stars: {best_repo['stargazers_count']} | Velocity: {max_velocity:.2f} stars/hr")

            readme_content = self._fetch_readme(best_repo['full_name'], headers)

            return {
                "name": best_repo["name"],
                "full_name": best_repo["full_name"],
                "html_url": best_repo["html_url"],
                "description": best_repo["description"] or "No description provided.",
                "language": best_repo["language"] or "Mixed/Unknown",
                "stars": best_repo["stargazers_count"],
                "readme": readme_content[:4000]
            }

        except requests.exceptions.HTTPError as e:
            # Handle 429 specifically with retry mechanism (decorator will catch this via Exception)
            print(f"[ERROR] GitHub API HTTP error: {e}")
            raise

    def _fetch_readme(self, full_name: str, base_headers: dict) -> str:
        """
        Extracts raw Markdown text directly using GitHub's raw API format.
        """
        print(f"[SENSOR LAYER] Extracting README payload for {full_name}...")
        url = f"https://api.github.com/repos/{full_name}/readme"

        headers = base_headers.copy()
        headers["Accept"] = "application/vnd.github.v3.raw"

        try:
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                return r.text
            return "> [!error] No README available or failed to fetch."
        except:
            return "> [!error] Failed to extract README payload due to network error."

    @retry_with_backoff(max_retries=3, initial_delay=5.0, backoff_factor=2.0)
    def evaluate_lobster(self, lobster: Dict[str, Any]) -> str:
        """
        Phase 2: Cognitive Layer. Feeds the payload to the CTO Engine.
        """
        if not lobster:
            return ""

        print("\n[COGNITIVE LAYER] Waking up the CTO Engine (GLM)...")
        print(f"[COGNITIVE LAYER] Evaluating structural and commercial value of {lobster['name']}...")

        system_prompt = """
        Persona & Tone: You are a world-class Hacker, CTO, and AI Tech Lead. You communicate like a brilliant, friendly 20-something peer. You possess deep engineering intuition and commercial awareness, but you explain complex tech stacks and workflows using highly accessible, engaging, and easy-to-understand language. You are genuinely excited to share this new "killer app/repo" with your "bro/peer" (the user).

        Task & Constraints:
        - Analyze the provided README payload of today's fastest-growing GitHub repository.
        - Strip away the author's marketing fluff. I need the hard engineering truth and its real-world value.
        - Output strictly in Obsidian-flavored Markdown.
        - DYNAMIC TAGGING: Generate 2-3 specific hashtags based on the tech stack or use-case (e.g., #BrowserAutomation, #LocalLLM, #Productivity). Keep #GitHubHunter as a permanent tag.
        - Do not get lazy. Write thick, substantial, and highly detailed paragraphs for each section.

        Required Output Structure (STRICTLY FOLLOW THIS FORMAT):

        # 🦞 Today's Top Catch: [Repository Name]
        [Dynamic Tag 1] [Dynamic Tag 2] #GitHubHunter

        > [!info] 🎯 Target Locked
        > **Repo Link:** [Insert URL here]
        > **Tech Stack:** [e.g., Python, TypeScript, FastAPI, React]
        > **One-Line Pitch:** [1 sentence: What does this actually do?]

        > [!summary] 📦 1. Core Identity
        > [CRITICAL LENGTH: 2 paragraphs. Answer "是什么？". Strip the jargon. Explain the core mechanism, the architecture, and exactly what problem it solves. Is it a framework, a plugin, a UI, or a terminal tool? Explain it over a cup of coffee.]

        > [!example] 💎 2. The "Lobster" Value
        > [CRITICAL LENGTH: 1 thick paragraph. Answer "值什么？". Why is this trending so fast? Does it save exorbitant API costs? Does it replace a $20/month subscription? What is its commercial or extreme productivity potential?]

        > [!quote] 🛠️ 3. Deployment & Friction
        > [CRITICAL LENGTH: 1 thick paragraph. Answer "怎么用？". Be brutally honest about the developer experience (DX). Is it a 1-second `pip install` or a Docker compose nightmare? Give a concrete tip on how the user can spin this up with zero friction.]

        > [!abstract] ⚙️ 4. The Ideal Workflow & SOP
        > [CRITICAL LENGTH: 1 thick paragraph. Answer "理想工作流？". Paint a picture of the exact scenario where this shines. How does this fit into a modern AI/Dev pipeline?]

        ---
        """

        user_prompt = f"""
        Target Repository: {lobster['full_name']}
        URL: {lobster['html_url']}
        Primary Language: {lobster['language']}
        Current Stars: {lobster['stars']}

        --- README PAYLOAD (Truncated to 4000 chars) ---
        {lobster['readme']}
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7
            )

            evaluation = response.choices[0].message.content
            print("[COGNITIVE LAYER] Evaluation complete. The CTO has spoken.")
            return evaluation

        except Exception as e:
            print(f"[ERROR] Cognitive Engine failure: {e}")
            raise

    def save_to_vault(self, report: str) -> None:
        """
        Phase 3a: Storage Layer.
        Delegates to ObsidianFileStorage.
        """
        print("\n[STORAGE LAYER] Saving payload to Obsidian Vault...")
        base_vault_path = os.getenv("OBSIDIAN_PATH")
        storage = ObsidianFileStorage(vault_path=base_vault_path, subfolder="GitHuber")
        storage.save(report, prefix="GitHuber_Catch")

    def send_email(self, report: str, repo_name: str) -> None:
        """
        Phase 3b: Dispatch Layer.
        Delegates to EmailDispatcher.
        """
        print("\n[DISPATCH LAYER] Initializing Text Slicer and SMTP transmission...")
        subject = f"🦞 GitHuber Alert: {repo_name} is Trending"
        dispatcher = EmailDispatcher()
        dispatcher.send(report, subject)


if __name__ == "__main__":
    import sys
    # --- 1. SYSTEM CONFIGURATION ---
    load_dotenv()

    githuber = GitHuber()

    print("\n--- INITIATING GITHUB LOBSTER HUNT SEQUENCE ---")

    # --- 2. THE ATOMIC APN LOOP ---
    try:
        # Phase 1: Hunt
        lobster = githuber.hunt_top_lobster(query="")

        if not lobster:
            raise Exception("Sensor Layer failed to lock onto a valid target.")

        # Phase 2: Evaluate
        report = githuber.evaluate_lobster(lobster)

        if not report or report.startswith("> [!error]"):
            raise Exception("Cognitive Layer (CTO Engine) returned an error block.")

        print("\n" + "="*50)
        print("🚀 FINAL CTO REPORT GENERATED 🚀")
        print("="*50)

        # Phase 3a: Vault Persistence
        try:
            githuber.save_to_vault(report)
        except Exception as e:
            print(f"[HELIX_WARNING] Local Persistence Failed: {e}")

        # Phase 3b: Network Dispatch
        try:
            githuber.send_email(report=report, repo_name=lobster['name'])
        except Exception as e:
            print(f"[HELIX_WARNING] Network Dispatch Failed: {e}")

        print("\n[SYSTEM] GitHuber APN routine complete. Mission Accomplished. Entering standby.")

    except Exception as fatal_error:
        print(f"\n[CRITICAL FAILURE] GitHuber hunt sequence aborted: {fatal_error}")
        sys.exit(1)
