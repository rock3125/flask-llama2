import torch
from transformers import pipeline

# small sample on how to run llama-3b

generate_text = pipeline(
    model="h2oai/h2ogpt-gm-oasst1-en-2048-open-llama-3b",
    torch_dtype="auto",
    trust_remote_code=True,
    use_fast=False,
    device_map={"": "cuda:0"},
)

res = generate_text(
    "Why is drinking water so healthy?",
    min_new_tokens=2,
    max_new_tokens=1024,
    do_sample=False,
    num_beams=1,
    temperature=float(0.3),
    repetition_penalty=float(1.2),
    renormalize_logits=True
)
print(res[0]["generated_text"])

