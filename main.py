import sys
from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.verifier import VerifierAgent
from dotenv import load_dotenv

load_dotenv()

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py \"Your operation task here\"")
        return

    user_query = sys.argv[1]
    print(f"\n--- Starting AssistOps: AI Operations Assistant ---")
    print(f"Task: {user_query}\n")

    # 1. Planning Phase
    print("[Agent] Planner is designing a logical flow...")
    planner = PlannerAgent()
    plan = planner.create_plan(user_query)
    
    if not plan:
        print("Planner could not generate a plan for this request.")
        return

    # 2. Execution Phase
    print(f"[Agent] Executor is fetching verified data (Steps: {len(plan)})...")
    executor = ExecutorAgent()
    results = executor.execute(plan)

    # 3. Verification Phase
    print("[Agent] Verifier (The Integrity Guardian) is validating results...")
    verifier = VerifierAgent()
    final_output = verifier.verify_and_finalize(user_query, results)

    print("\n--- FINAL VERIFIED OUTPUT ---")
    print(final_output)
    print("------------------------------\n")

if __name__ == "__main__":
    main()
