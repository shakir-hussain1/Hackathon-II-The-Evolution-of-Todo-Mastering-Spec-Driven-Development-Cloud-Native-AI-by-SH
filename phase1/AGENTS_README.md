# Agent System Architecture - Phase 1 Todo Application

## Overview

The Agent System is a reusable intelligence framework built on the **Claude Agent SDK** principles. It enables modular, composable, and extensible task management through specialized agents and skills.

### Key Features

✅ **Modular Architecture** - Agents and skills are independent, self-contained units
✅ **Composable Skills** - Skills can be shared across multiple agents
✅ **Intelligent Routing** - Automatic intent detection and command routing
✅ **Analytics & Metrics** - Built-in task analytics and reporting
✅ **Execution Tracking** - Complete history of all agent/skill executions
✅ **Async-Ready** - Fully asynchronous execution for scalability
✅ **100% Testable** - Every component has unit tests

---

## Architecture Overview

### 4-Layer System

```
┌─────────────────────────────────────────────────┐
│        User Interface (CLI / Interactive)       │
├─────────────────────────────────────────────────┤
│        AgentOrchestrator (Central Hub)          │
│  ┌──────────────────────────────────────────┐  │
│  │        AgentRegistry (Lookup)             │  │
│  ├──────────────────────────────────────────┤  │
│  │  ┌─────────────────┐  ┌──────────────┐  │  │
│  │  │ TaskMgmtAgent   │  │AnalyticsAgent│  │  │
│  │  ├─────────────────┤  ├──────────────┤  │  │
│  │  │ Skills:         │  │ Skills:      │  │  │
│  │  │ • CreateTask    │  │ • Metrics    │  │  │
│  │  │ • ListTasks     │  │              │  │  │
│  │  │ • DeleteTask    │  │              │  │  │
│  │  │ • UpdateTask    │  │              │  │  │
│  │  │ • ToggleStatus  │  │              │  │  │
│  │  └─────────────────┘  └──────────────┘  │  │
│  └──────────────────────────────────────────┘  │
├─────────────────────────────────────────────────┤
│      TaskManager (Business Logic)              │
├─────────────────────────────────────────────────┤
│      Database / Storage Layer                   │
└─────────────────────────────────────────────────┘
```

---

## Core Components

### 1. **BaseAgent** (`src/agents/base_agent.py`)
Abstract base class for all agents.

**Key Methods:**
- `register_skill()` - Register a skill with the agent
- `execute()` - Execute agent logic (abstract)
- `get_skill()` - Retrieve a skill by name
- `list_skills()` - Get all registered skills

**Key Attributes:**
- `name` - Agent identifier
- `description` - Agent purpose
- `skills` - List of registered skills

```python
from src.agents.base_agent import BaseAgent, AgentContext

class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="MyAgent", description="My custom agent")

    async def execute(self, context: AgentContext) -> dict:
        # Implement agent logic
        return {"success": True, "message": "OK", "data": None}
```

### 2. **BaseSkill** (`src/skills/base_skill.py`)
Abstract base class for all skills.

**Key Methods:**
- `execute()` - Execute skill logic (abstract)
- `validate()` - Validate context before execution (abstract)
- `get_metadata()` - Get skill metadata

**Key Attributes:**
- `name` - Skill identifier
- `description` - Skill purpose
- `version` - Skill version
- `tags` - Skill tags for categorization
- `execution_count` - How many times executed

```python
from src.skills.base_skill import Skill, SkillConfig

class MySkill(Skill):
    def __init__(self):
        config = SkillConfig(
            name="my_skill",
            description="My custom skill",
            tags=["custom", "example"]
        )
        super().__init__(config)

    def validate(self, context: AgentContext) -> bool:
        return hasattr(context, "task_manager")

    async def execute(self, context: AgentContext) -> dict:
        # Implement skill logic
        return {"success": True, "message": "Skill executed", "data": None}
```

### 3. **AgentRegistry** (`src/agents/agent_registry.py`)
Central registry for managing agents and skills.

**Key Methods:**
- `register_agent()` - Register an agent
- `register_skill_for_agent()` - Attach skill to agent
- `get_agent()` - Retrieve agent by name
- `get_skill()` - Retrieve skill by name
- `list_all_agents()` - Get all registered agents
- `list_all_skills()` - Get all registered skills
- `get_registry_summary()` - Get complete registry state

```python
from src.agents.agent_registry import AgentRegistry
from src.agents.task_management_agent import TaskManagementAgent
from src.skills.task_skills import CreateTaskSkill

registry = AgentRegistry()
agent = TaskManagementAgent()
registry.register_agent(agent)
registry.register_skill_for_agent("TaskManagementAgent", CreateTaskSkill())

# Lookup
my_agent = registry.get_agent("TaskManagementAgent")
my_skill = registry.get_skill("create_task")
```

### 4. **AgentOrchestrator** (`src/agents/agent_orchestrator.py`)
Coordinates execution of agents and skills.

**Key Methods:**
- `execute_agent()` - Execute a specific agent
- `execute_skill()` - Execute a specific skill directly
- `get_execution_history()` - Retrieve execution log
- `get_registry_info()` - Get registry summary
- `clear_history()` - Clear execution history

```python
from src.agents.agent_orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator(registry, task_manager)

# Execute agent
result = await orchestrator.execute_agent(
    agent_name="TaskManagementAgent",
    user_input="add Buy groceries | Fresh vegetables"
)

# Execute skill directly
result = await orchestrator.execute_skill(
    skill_name="toggle_task_status",
    user_input="1"
)

# View history
history = orchestrator.get_execution_history()
```

### 5. **AgentFactory** (`src/agents/agent_factory.py`)
Factory for building the complete agent system.

**Key Methods:**
- `create_agent_system()` - Initialize all agents and skills

```python
from src.agents.agent_factory import AgentFactory

registry = AgentFactory.create_agent_system()
# Returns fully initialized AgentRegistry with all agents and skills
```

---

## Implemented Agents

### **TaskManagementAgent**
Handles all task lifecycle operations.

**Skills:**
- `create_task` - Create new tasks
- `list_tasks` - Retrieve all tasks
- `update_task` - Update task details
- `delete_task` - Delete tasks
- `toggle_task_status` - Mark complete/incomplete

**Intent Recognition:**
- "add", "create", "new" → `create` intent
- "get", "show", "list" → `retrieve` intent
- "delete", "remove" → `delete` intent
- "update", "edit", "change" → `update` intent
- "complete", "toggle", "mark" → `toggle` intent

**Example:**
```python
# Add task
result = await orchestrator.execute_agent(
    agent_name="TaskManagementAgent",
    user_input="add Buy milk | For breakfast"
)

# List tasks
result = await orchestrator.execute_agent(
    agent_name="TaskManagementAgent",
    user_input="list all tasks"
)
```

### **AnalyticsAgent**
Provides task insights and metrics.

**Skills:**
- `compute_metrics` - Calculate task statistics

**Metrics Provided:**
- `total_tasks` - Count of all tasks
- `completed_tasks` - Count of completed tasks
- `incomplete_tasks` - Count of incomplete tasks
- `completion_rate` - Percentage of completed tasks

**Example:**
```python
result = await orchestrator.execute_agent(
    agent_name="AnalyticsAgent",
    user_input="compute metrics"
)

metrics = result["data"]
print(f"Completion Rate: {metrics['completion_rate']}%")
```

---

## Implemented Skills

### **Task Skills** (`src/skills/task_skills.py`)

#### CreateTaskSkill
Creates new tasks from user input.

Input format: `title | description`

```python
result = await orchestrator.execute_skill(
    skill_name="create_task",
    user_input="Buy groceries | Fresh vegetables"
)
```

#### ListTasksSkill
Lists all tasks with optional filtering.

```python
result = await orchestrator.execute_skill(
    skill_name="list_tasks",
    user_input="list",
    metadata={"status_filter": "incomplete"}
)
```

#### UpdateTaskSkill
Updates task title and/or description.

Input format: `task_id | title | description`

```python
result = await orchestrator.execute_skill(
    skill_name="update_task",
    user_input="1 | New title | New description"
)
```

#### DeleteTaskSkill
Deletes tasks by ID.

```python
result = await orchestrator.execute_skill(
    skill_name="delete_task",
    user_input="1"
)
```

#### ToggleTaskStatusSkill
Toggles task between complete/incomplete.

```python
result = await orchestrator.execute_skill(
    skill_name="toggle_task_status",
    user_input="1"
)
```

### **Analytics Skills** (`src/skills/analytics_skills.py`)

#### ComputeMetricsSkill
Calculates task completion metrics.

```python
result = await orchestrator.execute_skill(
    skill_name="compute_metrics",
    user_input="metrics"
)
```

---

## Using the Agent System

### Installation

Ensure dependencies are installed:
```bash
cd phase1
uv sync
```

### Example 1: Direct Agent Execution

```python
import asyncio
from src.services.task_manager import TaskManager
from src.agents.agent_factory import AgentFactory
from src.agents.agent_orchestrator import AgentOrchestrator

async def main():
    task_manager = TaskManager()
    registry = AgentFactory.create_agent_system()
    orchestrator = AgentOrchestrator(registry, task_manager)

    # Create task
    result = await orchestrator.execute_agent(
        agent_name="TaskManagementAgent",
        user_input="add My task | Description here"
    )

    print(f"Success: {result['success']}")
    print(f"Message: {result['message']}")

asyncio.run(main())
```

### Example 2: Run with Agent-Enhanced Interactive CLI

```bash
# Run interactive CLI with agent system
python src/interactive_agent_enhanced.py
```

**Available Commands:**
```
add <title> | <description>      - Add task with agent
list                             - List all tasks
complete <id>                    - Mark complete
incomplete <id>                  - Mark incomplete
update <id> | <title> | <desc>   - Update task
delete <id>                      - Delete task
analytics                        - Show metrics
registry                         - Show agent registry
history                          - Show execution history
clear-history                    - Clear history
help                             - Show all commands
exit                             - Quit
```

### Example 3: Run Agent System Demo

```bash
# Run comprehensive demo
python src/main_with_agents.py
```

---

## Creating Custom Agents and Skills

### Step 1: Create Custom Agent

```python
# src/agents/my_custom_agent.py
from src.agents.base_agent import BaseAgent, AgentContext

class MyCustomAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="MyCustomAgent",
            description="My custom agent for specific tasks"
        )

    async def execute(self, context: AgentContext) -> dict:
        try:
            intent = self._parse_intent(context.user_input)

            if intent == "my_operation":
                return await self._handle_my_operation(context)

            return {
                "success": False,
                "message": f"Unknown operation: {intent}",
                "data": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error: {str(e)}",
                "data": None
            }

    def _parse_intent(self, user_input: str) -> str:
        user_input_lower = user_input.lower()
        if "my_keyword" in user_input_lower:
            return "my_operation"
        return "unknown"

    async def _handle_my_operation(self, context: AgentContext) -> dict:
        skill = self.get_skill("my_skill")
        if not skill:
            return {
                "success": False,
                "message": "Skill not available",
                "data": None
            }
        return await skill.execute(context)
```

### Step 2: Create Custom Skill

```python
# src/skills/my_custom_skills.py
from src.skills.base_skill import Skill, SkillConfig
from src.agents.base_agent import AgentContext
from datetime import datetime

class MyCustomSkill(Skill):
    def __init__(self):
        config = SkillConfig(
            name="my_skill",
            description="My custom skill",
            tags=["custom"]
        )
        super().__init__(config)

    def validate(self, context: AgentContext) -> bool:
        return hasattr(context, "task_manager")

    async def execute(self, context: AgentContext) -> dict:
        try:
            # Your skill logic here
            self.execution_count += 1
            self.last_executed = datetime.now()

            return {
                "success": True,
                "message": "Operation successful",
                "data": {"result": "value"}
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error: {str(e)}",
                "data": None
            }
```

### Step 3: Register in Factory

```python
# Update src/agents/agent_factory.py
from src.agents.my_custom_agent import MyCustomAgent
from src.skills.my_custom_skills import MyCustomSkill

@staticmethod
def create_agent_system() -> AgentRegistry:
    registry = AgentRegistry()

    # ... existing agents ...

    # Add your custom agent
    custom_agent = MyCustomAgent()
    registry.register_agent(custom_agent)
    registry.register_skill_for_agent("MyCustomAgent", MyCustomSkill())

    return registry
```

---

## Testing

### Run All Tests

```bash
pytest tests/test_agents.py -v
```

### Test Specific Agent

```bash
pytest tests/test_agents.py::TestTaskManagementAgent -v
```

### Test Specific Skill

```bash
pytest tests/test_agents.py::TestCreateTaskSkill -v
```

### Example Test

```python
import pytest
import asyncio
from src.services.task_manager import TaskManager
from src.agents.task_management_agent import TaskManagementAgent
from src.agents.base_agent import AgentContext
from src.skills.task_skills import CreateTaskSkill

@pytest.mark.asyncio
async def test_create_task_agent():
    """Test creating task via agent."""
    agent = TaskManagementAgent()
    agent.register_skill(CreateTaskSkill())

    task_manager = TaskManager()
    context = AgentContext(
        task_manager=task_manager,
        user_input="add Buy milk | For breakfast"
    )

    result = await agent.execute(context)

    assert result["success"] is True
    assert "created" in result["message"]
```

---

## File Structure

```
phase1/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py          # Abstract agent base class
│   │   ├── task_management_agent.py  # Task operations agent
│   │   ├── analytics_agent.py      # Analytics agent
│   │   ├── agent_registry.py       # Agent/skill registry
│   │   ├── agent_orchestrator.py   # Execution orchestrator
│   │   └── agent_factory.py        # Agent system factory
│   ├── skills/
│   │   ├── __init__.py
│   │   ├── base_skill.py           # Abstract skill base class
│   │   ├── task_skills.py          # Task-related skills
│   │   └── analytics_skills.py     # Analytics skills
│   ├── main_with_agents.py         # Demo/example usage
│   └── interactive_agent_enhanced.py  # Agent-enhanced CLI
├── tests/
│   └── test_agents.py              # Agent/skill tests
└── AGENTS_README.md                # This file
```

---

## Execution Flow

### Typical Agent Execution Flow

```
User Input
    ↓
Interactive CLI
    ↓
AgentOrchestrator.execute_agent()
    ↓
AgentRegistry.get_agent()
    ↓
Agent.execute() - Intent Recognition
    ↓
Agent._parse_intent() → Determine operation
    ↓
Agent.get_skill() → Retrieve appropriate skill
    ↓
Skill.validate() → Check context
    ↓
Skill.execute() → Run skill logic
    ↓
Result → TaskManager updates
    ↓
Execution recorded in history
    ↓
Response to user
```

---

## Response Format

All agents and skills return a standardized response:

```python
{
    "success": bool,           # Operation success
    "message": str,            # Human-readable message
    "data": dict or None       # Operation results
}
```

**Success Example:**
```python
{
    "success": True,
    "message": "Task 1 created successfully",
    "data": {
        "task_id": 1,
        "title": "Buy groceries",
        "description": "Fresh vegetables",
        "status": "incomplete",
        "created_at": "2024-01-04T10:30:00"
    }
}
```

**Error Example:**
```python
{
    "success": False,
    "message": "Task 99 not found",
    "data": None
}
```

---

## Best Practices

### 1. **Single Responsibility Principle**
Each skill handles ONE specific operation. Complex workflows delegate to multiple skills.

### 2. **Intent Recognition**
Agents should intelligently parse user input to determine intent. Use keywords and patterns.

### 3. **Graceful Error Handling**
Never throw exceptions in main flow. Return error responses instead.

```python
# Good
return {"success": False, "message": "Error message", "data": None}

# Bad
raise ValueError("Error message")  # Exposes stack trace
```

### 4. **Metadata Tracking**
Every skill tracks execution count and timestamp for analytics.

### 5. **Dependency Injection**
Pass dependencies through AgentContext, not direct imports.

```python
# Good
context.task_manager.add_task(...)

# Bad
from src.services.task_manager import TaskManager
tm = TaskManager()  # Creates new instance, not shared
```

### 6. **Async-First Design**
All agent and skill execution is async-ready for future scalability.

```python
async def execute(self, context: AgentContext) -> dict:
    # Async operations
    result = await some_async_operation()
    return result
```

---

## Advanced Usage

### Direct Skill Execution

```python
# Skip agent, execute skill directly
result = await orchestrator.execute_skill(
    skill_name="create_task",
    user_input="Buy milk | For breakfast"
)
```

### Execution History

```python
# Get all executions
history = orchestrator.get_execution_history()

# Analyze patterns
for entry in history:
    print(f"Agent/Skill: {entry.get('agent') or entry.get('skill')}")
    print(f"Input: {entry['user_input']}")
    print(f"Success: {entry['result']['success']}")
```

### Registry Introspection

```python
# Discover system capabilities at runtime
info = orchestrator.get_registry_info()

print("Available Agents:", info["agents"])
print("Available Skills:", info["skills"])
print("Agent Capabilities:", info["agent_skill_map"])
```

### Custom Metadata

```python
# Pass metadata to agents
result = await orchestrator.execute_agent(
    agent_name="TaskManagementAgent",
    user_input="list tasks",
    metadata={
        "status_filter": "incomplete",
        "sort_by": "created_at",
        "user_id": "user123"
    }
)
```

---

## Performance Considerations

- **Async Execution**: All operations are non-blocking
- **Execution Tracking**: History stored in memory (consider persistence for production)
- **Registry Lookup**: O(1) for agent/skill retrieval via dictionary
- **Skill Reusability**: Avoid redundant agent wrappers

---

## Future Enhancements

- [ ] Persistence of execution history to database
- [ ] Agent composition for complex workflows
- [ ] Skill versioning and rollback
- [ ] Performance metrics and timing
- [ ] Agent authentication and authorization
- [ ] Distributed agent execution
- [ ] Machine learning for intent recognition
- [ ] Natural language intent parsing

---

## Troubleshooting

### "Agent not found"
```
✗ Agent 'UnknownAgent' not found

Solution: Use registry.list_all_agents() to see available agents
```

### "Skill not available"
```
✗ Create skill not available

Solution: Check AgentFactory to ensure skill is registered for agent
```

### "Validation failed"
```
✗ Skill 'create_task' validation failed

Solution: Ensure AgentContext has required attributes (task_manager, user_input, metadata)
```

### Skills return None
```
Solution: All skills must return dict with 'success', 'message', 'data' keys
```

---

## Support and Contribution

For issues, feature requests, or contributions:
1. Check existing issues
2. Create detailed bug reports with reproducible examples
3. Follow the existing code style and patterns
4. Add tests for new features
5. Update documentation

---

## License

This agent system is part of the Phase 1 Todo application.

---

**Last Updated**: January 4, 2026
**Agent System Version**: 1.0.0
**Status**: Production Ready
