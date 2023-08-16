# flask-llama2

## installing

```
pip install -r requirements.txt
```

## running using gunircorn

```
unicorn --bind 0.0.0.0:9000 --timeout 120 --threads 1 server:app
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
