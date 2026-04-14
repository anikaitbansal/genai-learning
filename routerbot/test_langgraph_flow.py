from memory_manager import MemoryManager
from retriever import FAISSRetriever
from langgraph_flow import build_langgraph_flow


def main():
    session_id = "test-session"

    memory = MemoryManager("chat_history.json")
    retriever = FAISSRetriever()
    graph = build_langgraph_flow()

    initial_state = {
        "message": "Explain RAG in simple words",
        "chat_history": memory.load(),
        "use_rag": True,
        "retriever": retriever,
        "intent": "",
        "retrieved_chunks": [],
        "rag_used": False,
        "bot_reply": "",
        "evaluation": {}
    }

    final_state = graph.invoke(initial_state)

    result = {
        "user_message": initial_state["message"],
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