from app.services.backend_agent import BackendAgent
from app.services.llm_backend_agent import LLMBackendAgent
from app.services.frontend_agent import FrontendAgent
from app.services.db_agent import DatabaseAgent
from app.services.test_agent import TestAgent
from app.services.task_decomposer import decompose_story
from app.services.task_parser import detect_patterns

class Coordinator:
    def __init__(self, logger):
        self.backend = BackendAgent()
        self.llm_backend = LLMBackendAgent()
        self.frontend = FrontendAgent()
        self.db = DatabaseAgent()
        self.test = TestAgent()
        self.logger = logger

    def run(self, work_item: dict, project_name: str):
        self.logger("Coordinator: Parsing story")

        patterns = detect_patterns(
            work_item["title"] + " " + work_item.get("description", "")
        )

        tasks = decompose_story(work_item)

        if "BACKEND" in tasks:
            if len(patterns) > 0:
                self.logger("Coordinator: Using rule-based backend agent")
                self.logger(self.backend.generate_api(work_item, project_name))
            else:
                self.logger("Coordinator: Fallback to LLM backend agent")
                self.logger(self.llm_backend.generate_api(work_item, project_name))

        if "FRONTEND" in tasks:
            self.logger(self.frontend.generate_ui(work_item, project_name))

        if "DATABASE" in tasks:
            self.logger(self.db.generate_schema(project_name))

        if "TESTING" in tasks:
            self.logger(self.test.generate_tests(project_name))

        self.logger("Coordinator: Done")
