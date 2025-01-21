from agentosint.modules.ai_llama_module import LlamaModule

class ModuleRegistry:
    def __init__(self):
        self.modules = {
            "ai_llama": LlamaModule,
            # Add other modules as needed
        }

    def get_module(self, module_name):
        return self.modules.get(module_name)()
