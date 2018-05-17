[![Build Status](https://travis-ci.org/weirdname404/test-generator-api.svg?branch=master)](https://travis-ci.org/weirdname404/test-generator-api)
[![BCH compliance](https://bettercodehub.com/edge/badge/weirdname404/test-generator-api?branch=master)](https://bettercodehub.com/)
# test-generator-api
Web service for unique test generation based on ontology of the domain

### Request example
```
{
	"author": "Author",
	"creation_date": "01.01.1970",
	"version": "1.00",
	"guid": "2E7E22F4-5B51-4948-B120-AB21F08317DB",
	"test_requirements": {
		"count": 3,
		"question_type": ["O>A"],
		"answer_form": ["choice", "options"],
		"objects": [
			"Ст4сп",
			"05кп",
			"20пс"
		],

		"attributes": [
			"Массовая доля углерода",
			"Способ раскисления",
			"Содержание легирующих элементов"
		]
	}
}
```

### Response example
```
{
	"request_info": {
	"author": "Author",
	"creation_date": "01.01.1970",
	"version": "1.00",
	"guid": "2E7E22F4-5B51-4948-B120-AB21F08317DB",
	"test_requirements": {
		"count": 3,
		"question_type": ["O>A"],
		"answer_form": ["choice", "options"],
		"objects": [
			"Ст4сп",
			"05кп",
			"20пс"
		],

		"attributes": [
			"Массовая доля углерода",
			"Способ раскисления",
			"Содержание легирующих элементов"
		]
	}
},

	"questions": [{
			"guid": "Q1_GUID",
			"question_type": "O>A",
			"answer_form": "choice",
			"entity1": "E1_GUID",
			"entity2": "E2_GUID",
			"stem": "Определите верный способ раскисления у марки стали 05кп:",
			"distractors": [
				"Полуспокойная",
				"Кипящая",
				"Спокойная"
			],
			
			"key": [1]
		},
		{
			"guid": "Q2_GUID",
			"question_type": "O>A",
			"answer_form": "choice",
			"entity1": "E1_GUID",
			"entity2": "E2_GUID",
			"stem": "Определите верную массовую долю углерода у марки стали 05кп:",
			"distractors": [
				"0,05-0,12",
				"<=0,06",
				"0,57-0,65",
				"0,07-0,14",
				"0,27-0,35"
			],
			"key": [1]
		},
		{
			"guid": "Q3_GUID",
			"question_type": "O>A",
			"answer_form": "options",
			"entity1": "E1_GUID",
			"entity2": "E2_GUID",
			"stem": "Определите какие легирующие элементы содержатся в составе марки стали 05кп:",
			"distractors": [
				"Кремний",
				"Никель",
				"Марганец",
				"Хром",
				"Молибден"
			],
			"key": [0, 2, 3]

		}
	]
}
```
