import os
import requests

class LlamaModule:
    def __init__(self, server_url="http://localhost:5000"):
        self.server_url = server_url

    def set_model(self, model_path):
        """
        Switch the active model on the LM Studio server.
        """
        url = f"{self.server_url}/set_model"
        response = requests.post(url, json={"model_path": model_path})
        return response.json()

    def generate_text(self, prompt, max_length=100, temperature=0.7):
        """
        Generate text using the active model.
        """
        url = f"{self.server_url}/generate"
        payload = {"prompt": prompt, "max_length": max_length, "temperature": temperature}
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json().get("response")
        else:
            return f"Error: {response.json().get('error')}"

# Example usage
if __name__ == "__main__":
    llama = LlamaModule()
    print(llama.generate_text("Explain OSINT in simple terms.", max_length=150))
