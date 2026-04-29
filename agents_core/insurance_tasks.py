# agents_core/insurance_tasks.py
from crewai import Task
from crewai.tools import tool
from duckduckgo_search import DDGS

# ── Custom Search Tool ────────────────────────────────────────────────────────
# We build a lightweight @tool instead of using LangChain's wrapper
# because crewai 1.x prefers its own @tool decorator

@tool("insurance_web_search")
def insurance_web_search(query: str) -> str:
    """
    Searches the web for insurance policy information.
    """
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(
                f"insurance policy {query}",
                max_results=5,
            ):
                results.append(
                    f"Title: {r['title']}\n"
                    f"URL: {r['href']}\n"
                    f"Summary: {r['body']}\n"
                )
        if not results:
            return "No results found. Try rephrasing the query."
        return "\n---\n".join(results)

    except Exception as e:
        return f"Search failed: {str(e)}. Proceeding with internal knowledge."
# ── Task 1: Research Task ─────────────────────────────────────────────────────

def build_research_task(researcher, user_query: str) -> Task:
    """
    Assigns the Researcher Agent to find policy information
    for the given user query. Output becomes context for Writer.
    """
    return Task(
        description=(
            f"Research the following insurance topic thoroughly:\n\n"
            f"QUERY: {user_query}\n\n"
            f"Your job:\n"
            f"1. Use the insurance_web_search tool to find relevant policy info\n"
            f"2. Identify: coverage type, what is covered, what is excluded\n"
            f"3. Note any premium ranges or eligibility criteria if found\n"
            f"4. Compile all findings into structured research notes\n"
            f"5. If web search fails, use your expert knowledge\n\n"
            f"Output format (strictly follow this):\n"
            f"INSURANCE TYPE: ...\n"
            f"KEY COVERAGES: bullet list\n"
            f"EXCLUSIONS: bullet list\n"
            f"ELIGIBILITY/PREMIUMS: ...\n"
            f"SOURCES: list URLs if found\n"
        ),
        expected_output=(
            "Structured research notes with insurance type, "
            "key coverages, exclusions, eligibility, and sources."
        ),
        agent=researcher,
    )


# ── Task 2: Writing Task ──────────────────────────────────────────────────────

def build_writing_task(writer, research_task: Task) -> Task:
    """
    Assigns the Writer Agent to synthesize the Researcher's
    output into a clean, customer-friendly report.
    context=[research_task] is the handoff mechanism.
    """
    return Task(
        description=(
            "Using ONLY the research notes provided to you as context, "
            "write a clear, friendly insurance report for a customer.\n\n"
            "Your report MUST follow this exact structure:\n\n"
            "## 📋 Insurance Summary\n"
            "A 2-3 sentence plain-English overview.\n\n"
            "## ✅ What's Covered\n"
            "Bullet points of key coverages.\n\n"
            "## ❌ What's Not Covered (Exclusions)\n"
            "Bullet points of exclusions.\n\n"
            "## 💰 Cost & Eligibility\n"
            "Premium ranges and who qualifies.\n\n"
            "## 💡 Key Takeaways\n"
            "3-4 bullet points a customer should remember.\n\n"
            "Rules:\n"
            "- Use simple, jargon-free language\n"
            "- Never add information not in the research notes\n"
            "- Keep each section concise but complete\n"
        ),
        expected_output=(
            "A well-structured, customer-friendly insurance report "
            "following the exact markdown format specified."
        ),
        agent=writer,
        context=[research_task],   # ← THIS is the handoff from Researcher → Writer
    )