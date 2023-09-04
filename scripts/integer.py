import outlines.models as models
import outlines.text.generate as generate
import torch

model_name = "nomic-ai/gpt4all-j"
revision = "v1.2-jazzy"
# mps_device = torch.device("mps")
model = models.transformers(model_name,  revision=revision)

prompt = "2+2="
answer = generate.integer(model)(prompt)
print(1)