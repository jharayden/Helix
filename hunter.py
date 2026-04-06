import os
import urllib.request
import datetime
import smtplib
from dotenv import load_dotenv

# The Nuclear Bypass: Completely blind Python to Windows Registry proxies
os.environ["NO_PROXY"] = "*"
urllib.request.getproxies = lambda: {}

import arxiv
from openai import OpenAI
from typing import List, Dict

from utils import ObsidianFileStorage, EmailDispatcher, retry_with_backoff

# Load environment variables
load_dotenv()


class ArxivHunter:
    """
    The Orchestrator (Control Layer): Dictates the standard operating procedure (SOP).
    """
    def __init__(self, glm_api_key: str) -> None:
        # Action Layer (Sensors): The deterministic interface to query the Arxiv database.
        self.arxiv_client = arxiv.Client()

        # Cognitive Layer (Brain): The GLM API configuration.
        # Model name is loaded from environment variable, defaults to glm-5.
        model_name = os.getenv("ARXIV_MODEL", "glm-5")
        self.llm_client = OpenAI(
            api_key=glm_api_key,
            base_url="https://open.bigmodel.cn/api/paas/v4/"
        )
        self.model_name = model_name
        print(f"[SYSTEM] Arxiv Hunter Instantiated: Telemetry Online. (Model: {self.model_name})")

    @retry_with_backoff(max_retries=3, initial_delay=2.0, backoff_factor=2.0)
    def hunt_papers(self, query: str, max_results: int = 3) -> List[Dict[str, str]]:
        """
        Phase 2: Hunt. Executes API GET requests to Arxiv.
        Now upgraded to extract direct URLs for Zotero integration.
        """
        print(f"[ACTION LAYER] Executing search query: '{query}'...")

        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )

        results: List[Dict[str, str]] = []
        for paper in self.arxiv_client.results(search):
            paper_data = {
                "title": paper.title,
                "authors": ", ".join([author.name for author in paper.authors]),
                "abstract": str(paper.summary).replace('\n', ' '),
                "published": str(paper.published),
                "url": paper.entry_id
            }
            results.append(paper_data)

        print(f"[ACTION LAYER] Successfully retrieved {len(results)} papers.")
        return results

    @retry_with_backoff(max_retries=3, initial_delay=5.0, backoff_factor=2.0)
    def digest_papers(self, papers: List[Dict[str, str]]) -> str:
        """
        Phase 3: Digest. V2.0 Engine.
        Evaluates up to 20 papers, selects Top 3, provides deep tech-dive and URLs.
        """
        print("[COGNITIVE LAYER] Initializing V2.0 semantic analysis (Top 3 Selection)...")

        if not papers:
            return "> [!error] No papers found in the telemetry payload."

        # 1. Context Assembly (Now includes URLs)
        payload = ""
        for i, p in enumerate(papers, 1):
            payload += f"\n--- Paper {i} ---\nTitle: {p['title']}\nAuthors: {p['authors']}\nURL: {p['url']}\nAbstract: {p['abstract']}\n"

        # 2. V3.1.2 Prompt Engineering: Persona + Anti-Laziness & Strict Depth Constraints
        system_prompt = """
        Persona & Tone: You are a world-class Professor of high-end technology, such as Embodied AI, Robotics, and LLMs. However, you do not speak like a dusty, arrogant academic. You communicate like a brilliant, friendly 20-something peer. You possess deep, top-tier academic expertise, but you explain complex concepts using highly accessible, engaging, and easy-to-understand language. You are genuinely excited to share knowledge with your "bro/peer" (the user).

        Task & Constraints:
        - Analyze the ENTIRE provided context payload of recent papers.
        - EXACTLY 3 PAPERS: You MUST select EXACTLY the TOP 3 most valuable papers based on structural novelty and industry potential. Do not output just 1 or 2; I need exactly 3.
        - NO TRUNCATION: You must maintain the exact same extreme technical depth, length, and quality for Top 2 and Top 3 as you do for Top 1. Do not get lazy.
        - Output strictly in Obsidian-flavored Markdown.
        - DYNAMIC TAGGING: Generate 2-3 specific hashtags based on the paper's actual content. Keep #ArxivHunter as a permanent tag.
        - URL REQUIREMENT: You MUST include the exact URL provided in the payload for each selected paper.

        Required Output Structure (STRICTLY REPEAT THIS ENTIRE BLOCK 3 TIMES, for Top 1, Top 2, and Top 3):

        # 🥇 Top [1/2/3]: [Paper Title]
        [Dynamic Tag 1] [Dynamic Tag 2] #ArxivHunter

        > [!info] 🎯 Target Locked
        > **Authors:** [Authors]
        > **Link:** [Insert URL here - Crucial for Zotero!]
        > **Why this one, bro?:** [1-2 sentence, enthusiastic justification for why you picked this specific paper today.]

        > [!summary] 💡 Core Innovation
        > [CRITICAL LENGTH: Write 2-3 substantial paragraphs here. Strip away the academic jargon. Explain the underlying mechanics, the math/logic, and what specific problem it solves in plain, friendly language (as if explaining it over a cup of coffee), while maintaining extreme technical depth.]

        > [!example] 📈 Value Assessment & Future Prospects
        > [CRITICAL LENGTH: Write a highly detailed paragraph. What is the future impact of this technology? How can this be applied in real-world robotics or AI industry scenarios?]

        > [!quote] 🧠 Professor's Deep Dive
        > [CRITICAL LENGTH: Write a highly detailed paragraph. Provide your critical, independent thought on this paper. Is there a hidden flaw? Is it a game-changer or just an incremental update? Keep the tone sharp but peer-to-peer.]

        ---
        """

        try:
            response = self.llm_client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Context Payload:\n{payload}"}
                ],
                temperature=1.0,
                extra_body={"thinking": {"type": "enabled"}}
            )

            synthesis = response.choices[0].message.content
            print("[COGNITIVE LAYER] V2.0 Deep analysis complete.")
            return synthesis
        except Exception as e:
            print(f"[ERROR] Cognitive Layer misfire: {e}")
            raise

    def save_report(self, content: str, vault_path: str = None) -> None:
        """
        Phase 4: Report. Writes the synthesized AI response to the local file system.
        Delegates to ObsidianFileStorage.
        """
        print(f"\n[ORCHESTRATOR] Initiating Phase 4: Writing telemetry to local vault...")
        storage = ObsidianFileStorage(vault_path=vault_path, subfolder="Arxiv_Papers")
        storage.save(content, prefix="Arxiv_Hunter")

    def send_email(self, content: str) -> None:
        """
        Phase 4 (Action B): Deterministic SMTP client.
        Delegates to EmailDispatcher.
        """
        print(f"\n[ORCHESTRATOR] Initiating Phase 4 (Action B): Slicing text for email dispatch...")
        today_str = datetime.date.today().strftime("%Y-%m-%d")
        first_tag_match = None
        try:
            import re
            first_tag_match = re.search(r'#(\w+)', content)
        except:
            pass
        first_tag = first_tag_match.group(1) if first_tag_match else "Latest Research"
        subject = f"🤖 Arxiv Hunter [{first_tag}]: {today_str}"
        dispatcher = EmailDispatcher()
        dispatcher.send(content, subject)


if __name__ == "__main__":
    # --- 1. SYSTEM CONFIGURATION ---
    load_dotenv()
    api_key = os.getenv("GLM_API_KEY")
    obsidian_path = os.getenv("OBSIDIAN_PATH")

    # Ignite the Orchestrator
    hunter = ArxivHunter(glm_api_key=api_key)

    target_topic = os.getenv("TARGET_TOPIC")
    if not target_topic:
        target_topic = "Embodied AI"

    print(f"\n--- INITIATING HUNT SEQUENCE FOR: {target_topic} ---")

    # --- 2. THE ATOMIC APN LOOP ---
    try:
        # Phase 1 & 2: Generate
        retrieved_papers = hunter.hunt_papers(query=target_topic, max_results=15)
        print("\n--- INITIATING COGNITIVE DIGEST ---")
        final_report = hunter.digest_papers(papers=retrieved_papers)

        if final_report.startswith("> [!error]"):
            raise Exception("Cognitive Layer returned an error block.")

        # Phase 3: Vault Persistence
        try:
            hunter.save_report(content=final_report, vault_path=obsidian_path)
        except Exception as e:
            print(f"[HELIX_WARNING] Local Persistence Failed: {e}")

        # Phase 4: Network Dispatch
        try:
            hunter.send_email(content=final_report)
        except Exception as e:
            print(f"[HELIX_WARNING] Network Dispatch Failed: {e}")

        print("\n[SYSTEM] Arxiv Hunter APN routine complete. Mission Accomplished. Entering standby.")

    except Exception as fatal_error:
        import sys
        print(f"\n[CRITICAL FAILURE] Hunt sequence aborted: {fatal_error}")
        sys.exit(1)
