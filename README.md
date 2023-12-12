# llmine
LLM-based agent for Minecraft

Planner:
- [x] knowledge base files stored
- [x] meta data extracted
- [x] indices built
- [x] rag implemented
- [ ] prompt defined
- [ ] retrieval chain for subgoal extraction works
- [ ] knwledge graph extraction

Pipeline:
- Plan
    - RAG for subgoal extraction
    - Input: goals
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