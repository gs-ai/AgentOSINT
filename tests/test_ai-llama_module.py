import unittest
from agentosint.modules.ai_llama_module import LlamaModule

class TestLlamaModule(unittest.TestCase):
    def setUp(self):
        self.llama = LlamaModule(server_url="http://localhost:5000")

    def test_generate_text(self):
        result = self.llama.generate_text("What is OSINT?", max_length=50)
        self.assertIsInstance(result, str)

    def test_set_model(self):
        response = self.llama.set_model("./models/sample_model")
        self.assertIn("message", response)

if __name__ == "__main__":
    unittest.main()
