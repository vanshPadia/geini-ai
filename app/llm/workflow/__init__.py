from langgraph.graph import StateGraph, END
from app.llm.schemas.chat_schema import GraphState
from app.configs import log
from app.llm.workflow.pre_search_node import PreSearchNode
from app.llm.workflow.refine_search_node import RefineSearchNode
from app.llm.workflow.search_node import SearchNode
from app.llm.workflow.manager_node import ManagerNode
from app.llm.workflow.pre_search_refinement.pre_search_refinement_node import PreSearchRefinementNode
from app.llm.schemas.enums import GenieNodes


def init_workflow() -> StateGraph:
    graph = StateGraph(GraphState)

    graph.add_node(GenieNodes.MANAGER_NODE.value, lambda state: ManagerNode().apply(state, GenieNodes.MANAGER_NODE.value))
    graph.add_node(GenieNodes.PRE_SEARCH_NODE.value, lambda state: PreSearchNode().apply(state, GenieNodes.PRE_SEARCH_NODE.value))
    graph.add_node(GenieNodes.PRE_SEARCH_REFINEMENT_NODE.value, lambda state: PreSearchRefinementNode().apply(state, GenieNodes.PRE_SEARCH_REFINEMENT_NODE.value))
    graph.add_node(GenieNodes.SEARCH_NODE.value, lambda state: SearchNode().apply(state, GenieNodes.SEARCH_NODE.value))
    graph.add_node(GenieNodes.REFINE_SEARCH_NODE.value, lambda state: RefineSearchNode().apply(state, GenieNodes.REFINE_SEARCH_NODE.value))

    graph.set_entry_point(GenieNodes.MANAGER_NODE.value)

    graph.add_conditional_edges(
        GenieNodes.MANAGER_NODE.value,
        lambda state: GenieNodes.PRE_SEARCH_NODE.value if state.should_continue else END
    )

    graph.add_conditional_edges(
        GenieNodes.PRE_SEARCH_NODE.value,
        lambda state: GenieNodes.PRE_SEARCH_REFINEMENT_NODE.value if state.should_continue else END
    )

    graph.add_edge(
        GenieNodes.PRE_SEARCH_REFINEMENT_NODE.value,
        GenieNodes.SEARCH_NODE.value
    )

    graph.add_conditional_edges(
        GenieNodes.SEARCH_NODE.value,
        lambda state: GenieNodes.REFINE_SEARCH_NODE.value if state.should_continue else END
    )

    graph.add_edge(GenieNodes.REFINE_SEARCH_NODE.value, END)

    log.info("Workflow is initialized")
    return graph.compile()
