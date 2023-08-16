# flask-llama2

## installing

```
pip install -r requirements.txt
```

## running using gunircorn

```
gunicorn --bind 0.0.0.0:9000 --timeout 120 --threads 1 server:app
```

## testing using curl

* summarizer
```
curl -H "Content-Type: plain/text" -X POST --data "As is often the case with SpaceX's Starship program, it's difficult to predict when the company might make another attempt to launch a fully integrated Starship rocket stack, which towers some 400 feet (120 meters) tall, larger than NASA's Saturn V rocket from more than 50 years ago.  Elon Musk, SpaceX's founder and CEO, said in mid-June that the company could be ready for another Starship test flight in six to eight weeks. Taken most generously, that timetable has now expired." http://localhost:9000/summarize
```

* Question answering
```
curl -H "Content-Type: plain/text" -X POST --data "As is often the case with SpaceX's Starship program, it's difficult to predict when the company might make another attempt to launch a fully integrated Starship rocket stack, which towers some 400 feet (120 meters) tall, larger than NASA's Saturn V rocket from more than 50 years ago.  Elon Musk, SpaceX's founder and CEO, said in mid-June that the company could be ready for another Starship test flight in six to eight weeks. Taken most generously, that timetable has now expired.|who is the founder?" http://localhost:9000/qna
```

NB. uses the '|' symbol at the end to separate the question from the data supplied.

response: (processing_time in milliseconds, from a 12GB RTX 2080)
```json
{"processing_time":289,"response":"The founder of SpaceX is Elon Reeve Musk."}
```

## docker build
```
docker build -t llama2-server .
```

## arch / ubuntu gpu support for docker
```
yay -S libnvidia-container libnvidia-container-tools nvidia-container-runtime
```
or
```
sudo apt install -y nvidia-container-tools
```
test `docker run -it --rm --gpus all --runtime nvidia nvidia/cuda:12.2.0-base-ubuntu20.04 nvidia-smi`


## docker run
```
docker run -it --rm --gpus all --runtime nvidia -p 9000:9000 llama2-server:latest
```

## location of the model inside the container
```
/root/.cache/huggingface/hub/models--h2oai--h2ogpt-gm-oasst1-en-2048-open-llama-3b/snapshots/2c118b28c58a39e41bbc07c48594a4900ba3f083/pytorch_model.bin
```

