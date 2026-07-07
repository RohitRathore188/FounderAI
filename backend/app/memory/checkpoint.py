from langgraph.checkpoint.memory import MemorySaver

class GraphMemorySaver:
    """
    Wrapper for LangGraph checkpointer.
    Provides in-memory checkpointer by default, ready for custom SQLite / Postgres checkpointers.
    """
    def __init__(self):
        self.memory = MemorySaver()

    def get_checkpointer(self) -> MemorySaver:
        return self.memory

graph_memory = GraphMemorySaver()
