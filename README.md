# llmine
LLM-based agent for Minecraft

Pipeline:
- Plan
    - Build multimodal knowledge base
    - RAG for subgoal extraction
    - Input: goal
    - Output: list of atomic subgoals
- Decompose
    - multimodal decomposer 
    - layer 1:
        - Input: frame and subgoal list
        - Output: select which subgoal to execute
    - layer 2:
        - Input: frame and subgoal:
        - Execution: select with kb sequence of action
        - output: sequence of action
- act
    - execute action sequence & get a result 
- optimize