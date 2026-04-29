# agents_core/crew_runner.py

from crewai import Crew, Process
from agents_core.insurance_agents import build_researcher, build_writer
from agents_core.insurance_tasks import (
    build_research_task,
    build_writing_task,
    insurance_web_search,
)


# ── Output Capture ────────────────────────────────────────────────────────────

class AgentLogger:
    """
    Collects step-by-step agent logs during crew execution.
    Streamlit will read from this to show live progress.
    """

    def __init__(self):
        self.logs: list[dict] = []

    def log(self, agent: str, event: str, detail: str = ""):
        self.logs.append({
            "agent": agent,
            "event": event,
            "detail": detail.strip(),
        })

    def clear(self):
        self.logs = []


# Singleton logger — import this in Streamlit page to read logs
agent_logger = AgentLogger()


# ── Step Callback ─────────────────────────────────────────────────────────────

def _make_step_callback():
    """
    Returns a callback function compatible with crewai 1.x.
    Called after each agent step — logs to agent_logger.
    """
    def step_callback(agent_output):
        try:
            # agent_output varies by crewai version — handle both formats
            if hasattr(agent_output, "agent") and hasattr(agent_output, "output"):
                agent_name = str(agent_output.agent)
                output_text = str(agent_output.output)
            elif isinstance(agent_output, tuple) and len(agent_output) == 2:
                agent_name, output_text = str(agent_output[0]), str(agent_output[1])
            else:
                agent_name = "Agent"
                output_text = str(agent_output)

            # Detect tool use vs final answer
            if "insurance_web_search" in output_text.lower():
                event = "🔍 Using Search Tool"
            elif "final answer" in output_text.lower():
                event = "✅ Final Answer Ready"
            elif "thought" in output_text.lower():
                event = "💭 Thinking"
            else:
                event = "⚙️ Processing"

            agent_logger.log(
                agent=agent_name,
                event=event,
                detail=output_text[:300],  # cap detail to avoid huge logs
            )

        except Exception:
            pass  # Never let logging crash the crew

    return step_callback


# ── Main Runner Function ──────────────────────────────────────────────────────

def run_insurance_crew(user_query: str) -> dict:
    """
    Runs the full Researcher → Writer crew pipeline.

    Args:
        user_query: The insurance topic from the user.

    Returns:
        dict with keys:
            - "success": bool
            - "final_report": str  (Writer's markdown output)
            - "research_notes": str (Researcher's raw output)
            - "logs": list[dict]   (step-by-step agent logs)
            - "error": str         (only if success=False)
    """

    agent_logger.clear()

    try:
        # ── 1. Build agents ───────────────────────────────────────────────────
        agent_logger.log("System", "🚀 Starting", "Initializing agents...")

        tools = [insurance_web_search]
        researcher = build_researcher(tools=tools)
        writer = build_writer()

        agent_logger.log("System", "✅ Agents Ready", "Researcher + Writer initialized")

        # ── 2. Build tasks ────────────────────────────────────────────────────
        research_task = build_research_task(
            researcher=researcher,
            user_query=user_query,
        )
        writing_task = build_writing_task(
            writer=writer,
            research_task=research_task,
        )

        agent_logger.log(
            "System",
            "📋 Tasks Created",
            f"Query: {user_query[:100]}"
        )

        # ── 3. Assemble crew ──────────────────────────────────────────────────
        crew = Crew(
            agents=[researcher, writer],
            tasks=[research_task, writing_task],
            process=Process.sequential,   # Researcher MUST finish before Writer starts
            verbose=True,
            step_callback=_make_step_callback(),
        )

        agent_logger.log(
            "Crew",
            "⚡ Crew Assembled",
            "Sequential process: Researcher → Writer"
        )

        # ── 4. Kickoff ────────────────────────────────────────────────────────
        agent_logger.log("Researcher", "🔍 Research Starting", f"Searching: {user_query}")

        result = crew.kickoff()

        # ── 5. Extract outputs ────────────────────────────────────────────────
        # In crewai 1.x, result is a CrewOutput object
        final_report = ""
        research_notes = ""

        if hasattr(result, "raw"):
            final_report = str(result.raw)
        elif hasattr(result, "output"):
            final_report = str(result.output)
        else:
            final_report = str(result)

        # Try to get individual task outputs
        if hasattr(result, "tasks_output") and result.tasks_output:
            tasks_out = result.tasks_output
            if len(tasks_out) >= 1:
                research_notes = str(tasks_out[0].raw if hasattr(tasks_out[0], "raw") else tasks_out[0])
            if len(tasks_out) >= 2:
                final_report = str(tasks_out[1].raw if hasattr(tasks_out[1], "raw") else tasks_out[1])

        agent_logger.log("Writer", "✅ Report Complete", "Final report generated")

        return {
            "success": True,
            "final_report": final_report,
            "research_notes": research_notes,
            "logs": agent_logger.logs.copy(),
            "error": "",
        }

    except Exception as e:
        agent_logger.log("System", "❌ Error", str(e))
        return {
            "success": False,
            "final_report": "",
            "research_notes": "",
            "logs": agent_logger.logs.copy(),
            "error": str(e),
        }