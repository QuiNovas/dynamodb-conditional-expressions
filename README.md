# dynamodb-ce

### 

## Installation
```
pip install dynamodb-ce
```


## Overview
`dynamodb-ce` is a compiler that can compile [DynamoDB Conditional Expressions](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ConditionExpressions.html) into executable Python truthy functions that evaluate either a Python `dict` or a DynamoDB item (with DynamoDB typing).

Setting up the parser requires setting expression attribute names and values, just as they would be set
when calling DynamoDB. Expression attribute values can be represented either using Python types or DynamoDB
types.

Compilation is done once per (expression, attribute names, attribute values) tuple and cached. The truthy function that is the result of the compilation is designed to be _extremely_ fast. 

Lexing and parsing courtesy of [SLY](https://sly.readthedocs.io/en/latest/index.html).

### Usage

#### Using DynamoDB types:
```python
from dynamodb_ce import CeParser

parser = CeParser(
    expression_attribute_names={"#path": "body"},
    expression_attribute_values={':string1': {'S': "a"}, ':string2': {'S': "b"}, ':number1': {'N': 1}, ':number2': {'N': 2}}
)
item = {"body": {"M": {"number1": {"N": 1}, "number2": {"N": 2}, "string1": {"S": "a"}, "string2": {"S": "b"}}}}
parser.evaluate("#path.string2 > #path.string1", item)
```

#### Using Python types
```python
from dynamodb_ce import CeParser

parser = CeParser(
    expression_attribute_names={"#path": "body"},
    expression_attribute_values={':string1': "a", ':string2': "b", ':number1': 1, ':number2': 2}
)
item = {"body": {"number1": 1, "number2": 2, "string1": "a", "string2": "b"}}
parser.evaluate("#path.string2 > #path.string1", item)
```

#### Using the parsed (compiled) result directly
```python
from dynamodb_ce import CeParser

parser = CeParser(
    expression_attribute_names={"#path": "body"},
    expression_attribute_values={':string1': "a", ':string2': "b", ':number1': 1, ':number2': 2}
)
item = {"body": {"number1": 1, "number2": 2, "string1": "a", "string2": "b"}}
truthy = parser.parse("#path.string2 > #path.string1")
truthy(item)
```
