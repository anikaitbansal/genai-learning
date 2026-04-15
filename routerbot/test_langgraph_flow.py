from memory_manager import MemoryManager
from retriever import FAISSRetriever
from langgraph_flow import build_langgraph_flow


def main():
    session_id = "test-session"

    memory = MemoryManager("chat_history.json")
    retriever = FAISSRetriever()
    graph = build_langgraph_flow()

    initial_state = {
            "original_message": "who is anikait bansal and where does he live?",
            "chat_history": memory.load(),
            "use_rag": True,
            "retriever": retriever,
            "intent": "",
            "retrieved_chunks": [],
            "rag_used": False,
            "bot_reply": "",
            "evaluation": {},
            "evaluation_reason": "",
            "retry_count": 0
        }

    final_state = graph.invoke(initial_state)

    print("\nRETRY DEBUG\n")
    print("final_retry_count:", final_state["retry_count"])
    print("retry_happened:", final_state["retry_count"] > 0)
    print("final_evaluation:", final_state["evaluation"])

    result = {
        "user_message": initial_state["original_message"],
        "bot_reply": final_state["bot_reply"],
        "intent": final_state["intent"],
        "session_id": session_id,
        "rag_used": final_state["rag_used"],
        "retrieved_chunks": final_state["retrieved_chunks"],
        "evaluation": final_state["evaluation"]
    }

    print("\nFINAL GRAPH RESULT\n")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()