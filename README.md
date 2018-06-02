[![Build Status](https://travis-ci.org/weirdname404/test-generator-api.svg?branch=master)](https://travis-ci.org/weirdname404/test-generator-api)
[![BCH compliance](https://bettercodehub.com/edge/badge/weirdname404/test-generator-api?branch=master)](https://bettercodehub.com/)
# test-generator-api
It is a backend web service for unique test item generation, which was built with the help of [Flask](http://flask.pocoo.org/) and [SQLAlchemy](https://www.sqlalchemy.org/).
Microservice follows REST API architecture, however it supports only __GET__ and __POST__ methods, which was actually enough to fulfill the requirements.

Generator is deployed on [Heroku](https://www.heroku.com/) and it can be checked [here](https://test-generator-api.herokuapp.com/)
Keep in mind that I use free Heroku plan, which means that Heroku [dyno](https://www.heroku.com/dynos) will sleep after 30min with no activity. If a sleeping web dyno receives web traffic, it will become active again after a **short delay**, so be patient.


## Setup DB
Service uses Postgres DB.
 - Deployed service uses Heroku Postgres DB, you can read about it [here](https://www.heroku.com/postgres)
 - Locally, I used PostgreSQL instance inside a Docker container.

If you are willing to test the generator locally, it is necessary to install [Docker](https://www.docker.com/what-docker), here is the [guide](https://docs.docker.com/install/) how to do it.

After the installation, follow command creates a PostgreSQL instance.

```
docker run --name ontology-orm-psql \
    -e POSTGRES_PASSWORD=ONTOLOGY-DB \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_DB=ontology-db \
    -p 5432:5432 \
    -d postgres
```

**IF case**
If you got something like `Got permission denied while trying to connect to the Docker daemon`, just add `sudo` before any Docker command or follow these [steps](https://docs.docker.com/install/linux/linux-postinstall/)


**REMINDER**
 - to stop the instance `docker stop ontology-orm-psql`
 - to remove the instance `docker rm ontology-orm-psql`


## Setup and run
After we have successfully created PostgreSQL instance, we can install all the dependencies and run the app.

0) `pip install pipenv` [Pipenv](https://github.com/pypa/pipenv)
1) make a directory where you would like to clone the repository and go there
2) `git clone https://www.github.com/weirdname404/test-generator-api`
3) `cd test-generator-api`
4) `pipenv install` _it installs all dependencies_
5) `pipenv run ./run.sh` **runs the app**


## Behind the scenes
Test item generation works on the basis of the domain ontology. (Currently, ontology is only in the __Excel__ format)

**What happens after** `run.sh`?

1) The ontology of the domain is parsed and data about the entities **(objects, attributes, classes)** is moved to DB
2) Flask starts the app locally and then just listens to the requests. http://0.0.0.0:5000/
3) After receiving the request to generate a test item, a special `Config` is created on the basis of JSON request requirements. **Config class** can be found [here](https://github.com/weirdname404/test-generator-api/blob/master/api/api_modules/generator_modules/generation_config.py)
4) Certain sets of objects and attributes are fetched from the DB. _Required objects and attributes are mentioned in the_ `Config`
5) According to the `qustion_form` and `answer_form`, which are mentioned in the `Config` as well, certain entities that can be either distractors or right answers are randomly chosen. **Distractor** - _special false answer option that look very similar to the right answer_
6) The correct stem is chosen on the basis of `qustion_form` and `answer_form`
7) Response JSON with generated items is returned


### Request example
We requested 3 test items with the request JSON shown below:
```
{
	"author": "Author",
	"creation_date": "01.01.1970",
	"version": "1.00",
	"guid": "2E7E22F4-5B51-4948-B120-AB21F08317DB",
	"test_requirements": {
		"count": 3,
		"question_type": ["O>A>O", "O>A", "A>O"],
		"answer_form": ["binary", "choice", "options"],
		"entities1": ["Ст4сп", "05кп", "50", "20", "60"],
		"entities2": ["Содержание легирующих элементов", "Способ раскисления", "Характеристика качества", "ГОСТ сплава", "Максимальная доля углерода в процентах", "Минимальная доля марганца в процентах"]
	}
}
```
**REMINDER**
`question_type` can be any from `["O>A", "A>O", "O>A>O]` which corresponds to:
 - Object -> Attribute
 - Attribute -> Object
 - Object -> Attribute -> Object

`answer_form` can be any from `["binary", "choice", "options"]` which corresponds to:
 - **binary** - Yes/No answer
 - **choice** - single choice answer
 - **options** - multiple choice answer

**In my example I chose all possible question and answer forms.**

`objects` and `attributes` can be any from http://0.0.0.0:5000/entities _(if the app works locally)_ or from https://test-generator-api.herokuapp.com/entities

### Response
The generator responded with the following JSON:
```
{
	"questions": [{
		"answer_form": "binary",
		"distractors": ["Да", "Нет"],
		"entity1": "481EE934-C8E4-4F52-B822-87F7A1BF20DC",
		"entity2": "CC87318D-0877-4595-BE74-BF67C515778C",
		"guid": "F00EA984-A227-4962-BEE3-8D7442A6AEC5",
		"key": ["Да"],
		"question_type": "A>O",
		"stem": "Согласны ли Вы с тем, что верным примером стали, которую можно охарактеризовать как сталь обыкновенного качества, является сталь марки Ст4сп?"
	}, {
		"answer_form": "choice",
		"distractors": ["08пс", "Ст4сп", "Ст4кп", "Ст2пс", "Ст0"],
		"entity1": "3E005E99-F8C7-42EC-AEB7-D97D4774560D",
		"entity2": "776A475C-F816-41AC-99C5-3481DEA05439",
		"guid": "C487C646-3948-4481-854B-6EC5CCBAB873",
		"key": ["08пс"],
		"question_type": "O>A>O",
		"stem": "Назовите марки стали, входят в тот же ГОСТ, что и сталь 05кп:"
	}, {
		"answer_form": "options",
		"distractors": ["20", "45", "60", "20пс", "Ст5пс"],
		"entity1": "3E005E99-F8C7-42EC-AEB7-D97D4774560D",
		"entity2": "481EE934-C8E4-4F52-B822-87F7A1BF20DC",
		"guid": "5C3494B5-100B-43D6-B429-D513B94249AA",
		"key": ["20", "45", "60", "20пс"],
		"question_type": "O>A>O",
		"stem": "Назовите марки стали, которые по характеристике качества одинаковы со сталью 05кп:"
	}],
	"request_info": {
		"author": "Author",
		"creation_date": "01.01.1970",
		"guid": "2E7E22F4-5B51-4948-B120-AB21F08317DB",
		"test_requirements": {
			"answer_form": ["binary", "choice", "options"],
			"count": 3,
			"entities1": ["Ст4сп", "05кп", "50", "20", "60"],
			"entities2": ["Содержание легирующих элементов", "Способ раскисления", "Характеристика качества", "ГОСТ сплава", "Максимальная доля углерода в процентах", "Минимальная доля марганца в процентах"],
			"question_type": ["O>A>O", "O>A", "A>O"]
		},
		"version": "1.00"
	}
}
```


## How to test the generator?

I tested it with [curl](https://en.wikipedia.org/wiki/CURL)

1) Send the request via curl to local server
```
curl -XPOST -H "Content-type: application/json" -d '{"author": "Author","creation_date": "01.01.1970","version": "1.00","guid": "2E7E22F4-5B51-4948-B120-AB21F08317DB","test_requirements": {"count": 3,"question_type": ["O>A>O", "O>A", "A>O"],"answer_form": ["binary", "choice", "options"],"entities1": ["Ст4сп", "05кп", "50", "20", "60"],"entities2": ["Содержание легирующих элементов", "Способ раскисления", "Характеристика качества", "ГОСТ сплава", "Максимальная доля углерода в процентах", "Минимальная доля марганца в процентах"]}}' '0.0.0.0:5000/generate-test'

```

2) Send the request via curl to the deployed server
```
curl -XPOST -H "Content-type: application/json" -d '{"author": "Author","creation_date": "01.01.1970","version": "1.00","guid": "2E7E22F4-5B51-4948-B120-AB21F08317DB","test_requirements": {"count": 3,"question_type": ["O>A>O", "O>A", "A>O"],"answer_form": ["binary", "choice", "options"],"entities1": ["Ст4сп", "05кп", "50", "20", "60"],"entities2": ["Содержание легирующих элементов", "Способ раскисления", "Характеристика качества", "ГОСТ сплава", "Максимальная доля углерода в процентах", "Минимальная доля марганца в процентах"]}}' 'test-generator-api.herokuapp.com/generate-test'
```

