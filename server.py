#!/usr/bin/env python

import uuid
import os
import logging

from datetime import datetime

from flask import Flask
from flask import request
from flask_cors import CORS
import json

import torch
from transformers import pipeline

# setup logging to file
logger = logging.getLogger("llama-2-server")
handler = logging.FileHandler('log/llama2-server.log')
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(handler)

# gunicorn --bind 0.0.0.0:9000 --timeout 120 --threads 1 server:app

# summarizer:   curl -H "Content-Type: plain/text" -X POST --data "As is often the case with SpaceX's Starship program, it's difficult to predict when the company might make another attempt to launch a fully integrated Starship rocket stack, which towers some 400 feet (120 meters) tall, larger than NASA's Saturn V rocket from more than 50 years ago.  Elon Musk, SpaceX's founder and CEO, said in mid-June that the company could be ready for another Starship test flight in six to eight weeks. Taken most generously, that timetable has now expired." http://localhost:9000/summarize
# qna       :   curl -H "Content-Type: plain/text" -X POST --data "As is often the case with SpaceX's Starship program, it's difficult to predict when the company might make another attempt to launch a fully integrated Starship rocket stack, which towers some 400 feet (120 meters) tall, larger than NASA's Saturn V rocket from more than 50 years ago.  Elon Musk, SpaceX's founder and CEO, said in mid-June that the company could be ready for another Starship test flight in six to eight weeks. Taken most generously, that timetable has now expired.|who is the founder?" http://localhost:9000/qna


generate_text = pipeline(
    model="h2oai/h2ogpt-gm-oasst1-en-2048-open-llama-3b",
    torch_dtype="auto",
    trust_remote_code=True,
    use_fast=False,
    device_map={"": "cuda:0"},
)


# temp directory for the system
temp_dir = "/tmp"

app = Flask(__name__)
CORS(app, resources={r"/summarize/*": {"origins": "*"}})


@app.route('/')
def index():
    return "llama2-server"


@app.route('/summarize', methods=['POST'])
def summarize():
    t1 = datetime.now()
    instruction = "Create a short summary of the following text: \"{}.\"".format(request.data.decode('utf8'))
    res = generate_text(
        instruction,
        min_new_tokens=2,
        max_new_tokens=128,
        do_sample=False,
        num_beams=1,
        temperature=float(0.01),
        repetition_penalty=float(1.2),
        renormalize_logits=True
    )
    print(res[0]["generated_text"])

    delta = datetime.now() - t1
    return {"processing_time": int(delta.total_seconds() * 1000), "response": res[0]["generated_text"]}


@app.route('/qna', methods=['POST'])
def qna():
    complete_text = request.data.decode('utf8').split("|")
    t1 = datetime.now()
    instruction = "Given the following text: \"{}.\", answer this question: \"{}\"".format(complete_text[0], complete_text[1])
    res = generate_text(
        instruction,
        min_new_tokens=2,
        max_new_tokens=128,
        do_sample=False,
        num_beams=1,
        temperature=float(0.01),
        repetition_penalty=float(1.2),
        renormalize_logits=True
    )
    print(res[0]["generated_text"])

    delta = datetime.now() - t1
    return {"processing_time": int(delta.total_seconds() * 1000), "response": res[0]["generated_text"]}


# non gunicorn use - debug
if __name__ == "__main__":
    logger.info("running in dev test mode (not containered)")
    app.run(host="0.0.0.0",
            port=9000,
            debug=True,
            use_reloader=False)

