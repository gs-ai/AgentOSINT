import json
from typing import List, Dict, Any, Optional, Callable
from agentosint.core.module_registry import MODULE_MAP
from agentosint.modules.ai_llama_module import LlamaModule


class PipelineStep:
    """
    Represents a single step in the pipeline with a module name, target, and optional result key.
    """
    def __init__(self, module_name: str, target: str, result_key: Optional[str] = None):
        self.module_name = module_name
        self.target = target
        self.result_key = result_key

    def __repr__(self) -> str:
        return f"<PipelineStep(module_name={self.module_name}, target={self.target}, result_key={self.result_key})>"


class Pipeline:
    """
    Manages and executes a sequence of PipelineSteps, with optional AI processing integration.
    """
    def __init__(self, steps: List[PipelineStep], logger: Optional[Callable[[str], None]] = None):
        self.steps = steps
        self.results: List[Dict[str, Any]] = []
        self.logger = logger or print  # Default to print if no logger provided
        self.ai_module = LlamaModule()  # AI module initialization

    def log(self, message: str):
        """
        Logs a message using the provided logger.
        """
        if self.logger:
            self.logger(message)

    def process_with_ai(self, prompt: str) -> str:
        """
        Process a task using the AI module.
        """
        self.log(f"Processing with AI for prompt: {prompt}")
        try:
            response = self.ai_module.generate_text(prompt, max_length=200, temperature=0.7)
            self.log(f"AI Response: {response}")
            return response
        except Exception as e:
            error_message = f"Error during AI processing: {str(e)}"
            self.log(error_message)
            return error_message

    def run_step(self, step: PipelineStep) -> Dict[str, Any]:
        """
        Runs an individual pipeline step.
        """
        self.log(f"Running step: {step}")
        if step.module_name not in MODULE_MAP:
            error_message = f"Module '{step.module_name}' not found in registry."
            self.log(error_message)
            return {"module": step.module_name, "error": error_message}

        try:
            runner = MODULE_MAP[step.module_name]
            result = runner(step.target)
            if step.result_key:
                return {step.result_key: result}
            return {"module": step.module_name, "result": result}
        except Exception as e:
            error_message = f"Error in module '{step.module_name}': {str(e)}"
            self.log(error_message)
            return {"module": step.module_name, "error": error_message}

    def run(self, data: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Executes all pipeline steps in sequence, with optional AI processing at the start.
        """
        self.log("\n[Pipeline] Starting execution...")
        
        if data and "prompt" in data:
            ai_results = self.process_with_ai(data["prompt"])
            self.results.append({"ai_results": ai_results})

        for index, step in enumerate(self.steps, start=1):
            self.log(f"\n[Pipeline] Step {index}/{len(self.steps)}")
            result = self.run_step(step)
            self.results.append(result)

        self.log("\n[Pipeline] Execution completed.")
        return self.results

    def to_json(self) -> str:
        """
        Serializes the pipeline results to a JSON string.
        """
        return json.dumps(self.results, indent=2)
