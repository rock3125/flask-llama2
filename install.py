import torch
from transformers import pipeline

pipeline(
    model="h2oai/h2ogpt-gm-oasst1-en-2048-open-llama-3b",
    torch_dtype="auto",
    trust_remote_code=True,
    use_fast=False,
)
