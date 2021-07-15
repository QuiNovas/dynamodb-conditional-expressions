import inspect
import sys
from decimal import *
from pprint import pprint

from boto3.dynamodb.types import TypeSerializer
from dynamodb_ce import CeParser


class TestUnit(object):
    parser = CeParser()

    def getResult(self, expr, result):
        stack = inspect.stack()[2][4][0]
        testUnit = stack.split('.')[0]
        if result:
            result = "PASSED: "
            return "\033[1;32;40m " + testUnit + " " + result + "at case -> " + expr + " \033[01;37;40m"
        else:
            result = "FAILED: "
            if "--exit-on-error" in sys.argv:
                print("\033[1;31;40m " + testUnit + " " + result + "at case -> " + expr + " \033[01;37;40m")
                sys.exit(1)
            return "\033[1;31;40m " + testUnit + " " + result + "at case -> " + expr + " \033[01;37;40m"

    def run(self):
        serializer = TypeSerializer()
        for expr in self.expressions:
            try:
                result = self.getResult(expr, self.parser.evaluate(expr, self.message))
                print(f"dict: {result}")
                result = self.getResult(expr, self.parser.evaluate(expr, serializer.serialize(self.message)["M"]))
                print(f"ddb-dict: {result}")
            except Exception as e:
                result = self.getResult(expr, False)
                print(result)
                print("Caught exception on previous CASE: \033[1;31;40m ")
                pprint(e)
                print("\033[01;37;40m")

class greaterThan(TestUnit):
    def __init__(self):
        print(" \033[01;37;40m \n Starting test for " + inspect.stack()[1][4][0].split('.')[0].split('=')[-1])
        super(TestUnit, self).__init__()
        self.message = {"body": {"number1": 1, "number2": 2, "string1": "a", "string2": "b"}}
        self.expressions = [
                    "#path.string2 > #path.string1", # CASE: path > path
                    ":number2 > :number1", # CASE: int(value) > int(value)
                    ":string2 > :string1", # CASE: str(value) > str(value)
                    "#path.number2 > :number1", # CASE: path > int(value)
                    "#path.string2 > :string1", # CASE: path > str(value)
                    ":number2 > #path.number1",  # CASE: int(value) > path
                    ":string2 > #path.string1"
                ]
        self.parser._expression_attribute_names = {"#path": "body"}
        self.parser._expression_attribute_values = {':string1': {'S': "a"}, ':string2': {'S': "b"}, ':number1': {'N': 1}, ':number2': {'N': 2}}

class greaterThanOrEqual(TestUnit):
    def __init__(self):
        print(" \033[01;37;40m \n Starting test for " + inspect.stack()[1][4][0].split('.')[0].split('=')[-1])
        super(TestUnit, self).__init__()
        self.parser._expression_attribute_names = {"#path": "body"}
        self.parser._expression_attribute_values = {':string1': {'S': "a"}, ':string2': {'S': "b"}, ':number1': {'N': 1}, ':number2': {'N': 2}}
        self.message = {"body": {"number1": 1, "number2": 2, "string1": "a", "string2": "b"}}
        self.expressions = [
            "#path.string2 >= #path.string1", # CASE: path >= path (greater)
            "#path.string2 >= #path.string2", # CASE: path >= path (equal)
            ":number2 >= :number1", # CASE: int(value) >= int(value) (greater)
            ":number2 >= :number2", # CASE: int(value) >= int(value) (equal)
            ":string2 >= :string1", # CASE: str(value) >= str(value) (greater)
            ":string2 >= :string2", # CASE: str(value) >= str(value) (equal)
            "#path.number2 >= :number1", # CASE: path >= int(value) (greater)
            "#path.number2 >= :number2", # CASE: path >= int(value) (equal)
            "#path.string2 >= :string1", # CASE: path >= str(value) (greater)
            "#path.string2 >= :string2", # CASE: path >= str(value) (equal)
            ":number2 >= #path.number1", # CASE: int(value) > path (greater)
            ":number2 >= #path.number2", # CASE: int(value) > path (equal)
            ":string2 >= #path.string1", # Case: str(value) >= path (greater)
            ":string2 >= #path.string2"  # Case: str(value) >= path (equal)
        ]

class lessThanOrEqual(TestUnit):
    def __init__(self):
        print(" \033[01;37;40m \n Starting test for " + inspect.stack()[1][4][0].split('.')[0].split('=')[-1])
        super(TestUnit, self).__init__()
        self.message = {"body": {"number1": 1, "number2": 2, "string1": "a", "string2": "b"}}
        self.parser._expression_attribute_names = {"#path": "body"}
        self.parser._expression_attribute_values = {':string1': {'S': "a"}, ':string2': {'S': "b"}, ':number1': {'N': 1}, ':number2': {'N': 2}}
        self.expressions = [
            "#path.string1 <= #path.string2", # CASE: path <= path (greater)
            "#path.string1 <= #path.string1", # CASE: path <= path (equal)
            ":number1 <= :number2", # CASE: int(value) <= int(value) (greater)
            ":number1 <= :number1", # CASE: int(value) <= int(value) (equal)
            ":string1 <= :string2", # CASE: str(value) <= str(value) (greater)
            ":string1 <= :string1", # CASE: str(value) <= str(value) (equal)
            "#path.number1 <= :number2", # CASE: path <= int(value) (greater)
            "#path.number1 <= :number1", # CASE: path <= int(value) (equal)
            "#path.string1 <= :string2", # CASE: path <= str(value) (greater)
            "#path.string1 <= :string1", # CASE: path <= str(value) (equal)
            ":number1 <= #path.number2", # CASE: int(value) <= path (greater)
            ":number1 <= #path.number1", # CASE: int(value) <= path (equal)
            ":string1 <= #path.string2", # Case: str(value) <= path (greater)
            ":string1 <= #path.string1"  # Case: str(value) <= path (equal)
        ]

class lessThan(TestUnit):
    def __init__(self):
        print(" \033[01;37;40m \n Starting test for " + inspect.stack()[1][4][0].split('.')[0].split('=')[-1])
        super(TestUnit, self).__init__()
        self.message = {"body": {"number1": 1, "number2": 2, "string1": "a", "string2": "b"}}
        self.parser._expression_attribute_names = {"#path": "body"}
        self.parser._expression_attribute_values = {':string1': {'S': "a"}, ':string2': {'S': "b"}, ':number1': {'N': 1}, ':number2': {'N': 2}}
        self.expressions = [
            "#path.string1 < #path.string2", # CASE: path < path
            ":number1 < :number2", # CASE: int(value) < int(value)
            ":string1 < :string2", # CASE: str(value) < str(value)
            "#path.number1 < :number2", # CASE: path < int(value)
            "#path.string1 < :string2", # CASE: path < str(value)
            ":number1 < #path.number2",  # CASE: int(value) < path
            ":string1 < #path.string2"
        ]

class equal(TestUnit):
    def __init__(self):
        print(" \033[01;37;40m \n Starting test for " + inspect.stack()[1][4][0].split('.')[0].split('=')[-1])
        super(TestUnit, self).__init__()
        self.message = {"body": {"number1": 1, "number2": 2, "string1": "a", "string2": "b"}}
        self.parser._expression_attribute_names = {"#path": "body"}
        self.parser._expression_attribute_values = {':string1': {'S': "a"}, ':string2': {'S': "b"}, ':number1': {'N': 1}, ':number2': {'N': 2}}
        self.expressions = [
            "#path.string1 = #path.string1", # CASE: path < path
            ":number1 = :number1", # CASE: int(value) < int(value)
            ":string1 = :string1", # CASE: str(value) < str(value)
            "#path.number1 = :number1", # CASE: path < int(value)
            "#path.string1 = :string1", # CASE: path < str(value)
            ":number1 = #path.number1",  # CASE: int(value) < path
            ":string1 = #path.string1"
        ]

class notEqual(TestUnit):
    def __init__(self):
        print(" \033[01;37;40m \n Starting test for " + inspect.stack()[1][4][0].split('.')[0].split('=')[-1])
        super(TestUnit, self).__init__()
        self.message = {"body": {"number1": 1, "number2": 2, "string1": "a", "string2": "b"}}
        self.parser._expression_attribute_names = {"#path": "body"}
        self.parser._expression_attribute_values = {':string1': {'S': "a"}, ':string2': {'S': "b"}, ':number1': {'N': 1}, ':number2': {'N': 2}}
        self.expressions = [
            "#path.string1 <> #path.string2", # CASE: path <> path
            ":number1 <> :number2", # CASE: int(value) <> int(value)
            ":string1 <> :string2", # CASE: str(value) <> str(value)
            "#path.number1 <> :number2", # CASE: path <> int(value)
            "#path.string1 <> :string2", # CASE: path <> str(value)
            ":number1 <> #path.number2",  # CASE: int(value) <> path
            ":string1 <> #path.string2"
        ]

class between(TestUnit):
    def __init__(self):
        print(" \033[01;37;40m \n Starting test for " + inspect.stack()[1][4][0].split('.')[0].split('=')[-1])
        self.parser._expression_attribute_names = {"#path": "body"}
        self.parser._expression_attribute_values = {':string1': {'S': "a"}, ':string2': {'S': "b"}, ':string3': {'S': "c"}, ':number1': {'N': 1}, ':number2': {'N': 2}, ':number3': {'N': 3}}
        self.message = {"body": {"number1": 1, "number2": 2, "number3": 3, "string1": "a", "string2": "b", "string3": "c", "string2char": "aa", "string3char": "aaa", "numberList": [1,2,3]}}
        self.expressions = [
            "#path.numberList[1] BETWEEN #path.numberList[0] AND #path.numberList[2]", # CASE: int(path) BETWEEN int(path) AND int(path)
            "#path.numberList[1] BETWEEN #path.numberList[0] AND :number3", # CASE: int(path) BETWEEN int(path) AND int(value)
            "#path.numberList[1] BETWEEN :number1 AND #path.numberList[2]", # CASE: int(path) BETWEEN int(value) AND int(path)
            "#path.numberList[1] BETWEEN :number1 AND :number3", # CASE: int(path) BETWEEN int(value) AND int(value)
            "#path.string2 BETWEEN #path.string1 AND #path.string3", # CASE: str(path) BETWEEN str(path) AND str(path)
            "#path.string2 BETWEEN #path.string1 AND :string3", # CASE: str(path) BETWEEN str(path) AND str(value)
            "#path.string2 BETWEEN :string1 AND :string3", # CASE: str(path) BETWEEN str(value) AND str(value)
            "#path.string2 BETWEEN :string1 AND #path.string3", # CASE: str(path) BETWEEN str(value) AND str(path)
            ":string2 BETWEEN #path.string1 AND #path.string3", # CASE: str(value) BETWEEN str(path) AND str(path)
            ":string2 BETWEEN #path.string1 AND :string3", # CASE: str(value) BETWEEN str(path) AND str(value)
            ":string2 BETWEEN :string1 AND :string3", # CASE: str(value) BETWEEN str(value) AND str(value)
            ":string2 BETWEEN :string1 AND #path.string3", # CASE: str(value) BETWEEN str(value) AND str(path)
            ":number2 BETWEEN :number1 AND :number3", # CASE: int(value) BETWEEN int(value) AND int(value)
            ":number2 BETWEEN #path.numberList[0] AND #path.numberList[2]", # CASE: int(value) BETWEEN int(path) AND int(path)
            ":number2 BETWEEN #path.numberList[0] AND :number3", # CASE: int(value) BETWEEN int(path) AND int(value)
            ":number2 BETWEEN :number1 AND #path.numberList[2]", # CASE: int(value) BETWEEN int(value) AND int(path)
            "size(#path.string2char) BETWEEN size(#path.string1) AND size(#path.string3char)",
            "size(#path.string2char) BETWEEN size(#path.string1) AND :number3",
            "size(#path.string2char) BETWEEN #path.number1 AND #path.number3",
            "size(#path.string2char) BETWEEN :number1 AND :number3"
        ]

class inList(TestUnit):
    def __init__(self):
        print(" \033[01;37;40m \n Starting test for " + inspect.stack()[1][4][0].split('.')[0].split('=')[-1])
        self.parser._expression_attribute_names = {"#path": "body"}
        self.parser._expression_attribute_values = {':string1': {'S': "a"}, ':string2': {'S': "b"}, ':string3': {'S': "c"}, ':number1': {'N': 1}, ':number2': {'N': 2}, ':number3': {'N': 3}}
        self.message = {"body": {"number1": 1, "number2": 2, "number3": 3, "string1": "a", "string2": "b", "string3": "c", "numberList": [1,2,3]}}
        self.expressions = [
            "#path.string1 IN (:string2, :string1, :string3)"
        ]

class attribute_exists(TestUnit):
    def __init__(self):
        print(" \033[01;37;40m \n Starting test for " + inspect.stack()[1][4][0].split('.')[0].split('=')[-1])
        self.parser._expression_attribute_names = {"#path": "body", "#string": "string1"}
        self.parser._expression_attribute_values = {':string1': {'S': "a"}, ':string2': {'S': "b"}, ':string3': {'S': "c"}, ':number1': {'N': 1}, ':number2': {'N': 2}, ':number3': {'N': 3}, "map": {"M": {"mapkey": "mapval"}}}
        self.message = {"body": {"number1": 1, "number2": 2, "number3": 3, "string1": "a", "string2": "b", "string3": "c", "numberList": [1,2,3], "map": {"mapkey": "mapvalue"}}}
        self.expressions = [
            "attribute_exists(#path.string1)",
            "attribute_exists(#path.number1)",
            "attribute_exists(#path.numberList[0])",
            "attribute_exists(#path.map.mapkey)",
            "attribute_exists(#path.#string)"
        ]

class attribute_not_exists(TestUnit):
    def __init__(self):
        print(" \033[01;37;40m \n Starting test for " + inspect.stack()[1][4][0].split('.')[0].split('=')[-1])
        self.parser._expression_attribute_names = {"#path": "body", "#notThere": "not_there"}
        self.parser._expression_attribute_values = {':string1': {'S': "a"}, ':string2': {'S': "b"}, ':string3': {'S': "c"}, ':number1': {'N': 1}, ':number2': {'N': 2}, ':number3': {'N': 3}, "map": {"M": {"mapkey": "mapval"}}}
        self.message = {"body": {"number1": 1, "number2": 2, "number3": 3, "string1": "a", "string2": "b", "string3": "c", "numberList": [1, 2, 3], "map": {"mapkey": "mapvalue"}}}
        self.expressions = [
            "attribute_not_exists(#path.#notThere)"
        ]

class attribute_type(TestUnit):
    def __init__(self):
        print(" \033[01;37;40m \n Starting test for " + inspect.stack()[1][4][0].split('.')[0].split('=')[-1])
        self.parser._expression_attribute_names = {"#path": "body"}
        self.parser._expression_attribute_values = {
                                                    	':string1': {
                                                    		'S': "a"
                                                    	},
                                                    	':number1': {
                                                    		'N': 1
                                                    	},
                                                        ':stringType': {
                                                            'S': 'S'
                                                        },
                                                        ':numberType': {
                                                            'S': 'N'
                                                        },
                                                        ':binaryType':{
                                                            'S': 'B'
                                                        },
                                                        ':boolType':{
                                                            'S': 'BOOL'
                                                        },
                                                        ':nullType':{
                                                            'S': 'NULL'
                                                        },
                                                        ':mapType': {
                                                            'S': 'M'
                                                        },
                                                        ":listType": {
                                                            'S': 'L'
                                                        },
                                                        ":numberSetType": {
                                                            'S': 'NS'
                                                        },
                                                        ":stringSetType": {
                                                            'S': 'SS'
                                                        },
                                                        ':binarySetType':{
                                                            'S': 'BS'
                                                        },
                                                    	"map": {
                                                    		"M": {
                                                    			"mapkey": "mapval"
                                                    		}
                                                    	}
                                                    }
        self.message = {
                        	"body": {
                        		"number": 1,
                        		"string": "a",
                                "binary": bytes("dGhpcyB0ZXh0IGlzIGJhc2U2NC1lbmNvZGVk", "utf-8"),
                                "bool": False,
                                "null": None,
                                "binarySet": {bytes("Zm9v", "utf-8"), bytes("YmFy", "utf-8"), bytes("YmF6", "utf-8")},
                        		"numberSet": {Decimal("1.1"), Decimal("2.2"), Decimal("3.3")},
                        		"stringSet": {"foo", "bar", "baz"},
                                "list": ["foo", "bar", "baz"],
                        		"map": {
                        			"mapkey": "mapvalue"
                        		}
                        	}
                        }
        self.expressions = [
            "attribute_type( #path.string, :stringType )",
            "attribute_type( #path.number, :numberType )",
            "attribute_type( #path.map, :mapType )",
            "attribute_type( #path.numberSet, :numberSetType )",
            "attribute_type( #path.stringSet, :stringSetType )",
            "attribute_type( #path.binarySet, :binarySetType )",
            "attribute_type( #path.list, :listType )",
            "attribute_type( #path.bool, :boolType )",
            "attribute_type( #path.null, :nullType )",
        ]

class begins_with(TestUnit):
    def __init__(self):
        print(" \033[01;37;40m \n Starting test for " + inspect.stack()[1][4][0].split('.')[0].split('=')[-1])
        self.parser._expression_attribute_names = {"#path": "body", "#notThere": "not_there"}
        self.parser._expression_attribute_values = {':word1': {'S': "alpha"}, ':string1': {'S': "a"}, ':string2': {'S': "b"}, ':string3': {'S': "c"}, ':number1': {'N': 1}, ':number2': {'N': 2}, ':number3': {'N': 3}, ":mapval": {"S": "mapval"}}
        self.message = {"body": {"word1": "alpha", "number1": 1, "number2": 2, "number3": 3, "string1": "a", "string2": "b", "string3": "c", "numberList": [1,2,3], "map": {"mapkey": "mapvalue"}}}
        self.expressions = [
            "begins_with(#path.word1, :string1)",
            "begins_with(#path.word1, :word1)",
            "begins_with(#path.map.mapkey, :mapval)"
        ]

class size(TestUnit):
    def __init__(self):
        print(" \033[01;37;40m \n Starting test for " + inspect.stack()[1][4][0].split('.')[0].split('=')[-1])
        self.parser._expression_attribute_names = {"#path": "body"}
        self.parser._expression_attribute_values = {':wordlen': {'N': 3}, ':binarylen': {'N': 36}, ':string1': {'S': "a"}, ':string2': {'S': "b"}, ':string3': {'S': "c"}, ':number1': {'N': 1}, ':number2': {'N': 2}, ':number3': {'N': 3}, ":mapval": {"S": "mapval"}}
        self.message = {
                        	"body": {
                        		"number": 1,
                        		"word": "foo",
                                "binary": bytes("dGhpcyB0ZXh0IGlzIGJhc2U2NC1lbmNvZGVk", "utf-8"),
                                "bool": False,
                                "null": None,
                                "binarySet": {bytes("Zm9v", "utf-8"), bytes("YmFy", "utf-8"), bytes("YmF6", "utf-8")},
                        		"numberSet": {Decimal("1.1"), Decimal("2.2"), Decimal("3.3")},
                        		"stringSet": {"foo", "bar", "baz"},
                                "list": ["foo", "bar", "baz"],
                        		"map": {
                        			"mapkey": "map",
                                    "secondKey": "secondValue",
                                    "thirdKey": {"key1": "val2", "key2": "val2"}
                        		}
                        	}
                        }

        self.expressions = [
            "size(#path.word) = :wordlen",
            "size(#path.binary) = :binarylen",
            "size(#path.binarySet) = :number3",
            "size(#path.numberSet) = :number3",
            "size(#path.stringSet) = :number3",
            "size(#path.list) = :number3",
            "size(#path.map) = :number3",
            "size(#path.map.thirdKey) = :number2",
            "size(#path.map.mapkey) = :number3"
        ]

class Not(TestUnit):
    def __init__(self):
        print(" \033[01;37;40m \n Starting test for " + inspect.stack()[1][4][0].split('.')[0].split('=')[-1])
        self.message = {"body": {"number1": 1, "number2": 2, "string1": "a", "string2": "b"}}
        self.parser._expression_attribute_names = {"#path": "body"}
        self.parser._expression_attribute_values = {':string1': {'S': "a"}, ':string2': {'S': "b"}, ':number1': {'N': 1}, ':number2': {'N': 2}}
        self.expressions = [
                    "NOT #path.string2 < #path.string1", # CASE: path > path
                    "NOT :number2 < :number1", # CASE: int(value) > int(value)
                    "NOT :string2 < :string1", # CASE: str(value) > str(value)
                    "NOT #path.number2 < :number1", # CASE: path > int(value)
                    "NOT #path.string2 < :string1", # CASE: path > str(value)
                    "NOT :number2 < #path.number1",  # CASE: int(value) > path
                    "NOT :string2 < #path.string1",
                    "NOT size(#path.string1) > size(#path.string2)",
                    "NOT size(#path.string1) > :number2",
                    "NOT NOT :number2 > size(#path.string1)", # Double NOT
                    "NOT NOT NOT size(#path.string1) > :number2", # Triple NOT
                ]


class And(TestUnit):
    def __init__(self):
        print(" \033[01;37;40m \n Starting test for " + inspect.stack()[1][4][0].split('.')[0].split('=')[-1])
        self.message = {"body": {"number1": 1, "number2": 2, "number3": 3, "string1": "a", "string2": "b", "string1char": "a", "string2char": "aa"}}
        self.parser._expression_attribute_names = {"#path": "body"}
        self.parser._expression_attribute_values = {':string1': {'S': "a"}, ':string2': {'S': "b"}, ':number1': {'N': 1}, ':number2': {'N': 2}, ':number3': {'N': 3}, ":stringtype": {'S': 'S'}}
        self.expressions = [
                    "#path.string2 > #path.string1 AND :string1 < :string2",
                    ":number2 > :number1 AND :number1 < #path.number2",
                    ":string2 > :string1 AND size(#path.string1char) < :number2",
                    "#path.number2 > :number1 AND :number1 < size(#path.string2char)",
                    "#path.number2 BETWEEN :number1 AND :number3 AND :number1 < :number2",
                    "attribute_type(#path.string1, :stringtype) AND :number1 < :number2",
                    "attribute_exists(#path) AND :number2 > #path.number1",
                    "attribute_exists(#path) AND attribute_not_exists(#path.foo)",
                ]

class Or(TestUnit):
    def __init__(self):
        print(" \033[01;37;40m \n Starting test for " + inspect.stack()[1][4][0].split('.')[0].split('=')[-1])
        self.message = {"body": {"number1": 1, "number2": 2, "number3": 3, "string1": "a", "string2": "b", "string1char": "a", "string2char": "aa"}}
        self.parser._expression_attribute_names = {"#path": "body"}
        self.parser._expression_attribute_values = {':string1': {'S': "a"}, ':string2': {'S': "b"}, ':number1': {'N': 1}, ':number2': {'N': 2}, ':number3': {'N': 3}, ":stringtype": {'S': 'S'}}
        self.expressions = [
                    "#path.string2 > #path.string1 OR :string1 > :string2",
                    ":number2 > :number1 OR :number1 > #path.number2",
                    ":string2 > :string1 OR size(#path.string1char) > :number2",
                    "#path.number2 > :number1 OR :number1 > size(#path.string2char)",
                    "#path.number2 BETWEEN :number1 AND :number3 OR :number1 > :number2",
                    "attribute_type(#path.string1, :stringtype) OR :number1 > :number2",
                    "attribute_exists(#path) OR :number2 < #path.number1",
                    "attribute_not_exists(#path) OR attribute_not_exists(#path.foo)",
                ]

class precedence(TestUnit):
    def __init__(self):
        print(" \033[01;37;40m \n Starting test for " + inspect.stack()[1][4][0].split('.')[0].split('=')[-1])
        self.message = {"body": {"number1": 1, "number2": 2, "number3": 3, "string1": "a", "string2": "b", "string1char": "a", "string2char": "aa"}}
        self.parser._expression_attribute_names = {"#path": "body"}
        self.parser._expression_attribute_values = {':string1': {'S': "a"}, ':string2': {'S': "b"}, ':number1': {'N': 1}, ':number2': {'N': 2}, ':number3': {'N': 3}, ":stringtype": {'S': 'S'}}
        self.expressions = [
                    ":number2 > :number1 OR :number1 < :number2 AND :number1 > :number2",
                    ":number2 > :number1 OR :number1 < :number2 AND :number1 > :number2 AND :number3 < :number2",
                    ":number1 > :number2 OR :number2 < :number3 AND size(#path.string1) = :number1",
                    "(:number1 > :number2 OR :number2 < :number3 AND size(#path.string1) = :number1) OR (:number2 > :number1 OR :number1 < :number2 AND :number1 > :number2) AND (:number1 > :number2)",
                    "NOT (:number1 > :number2 OR :number2 < :number3 AND size(#path.string1) = :number2) OR (:number2 > :number1 OR  :number3 > :number2 AND :number1 > :number2) AND :number1 > :number1",
                    "((:number1 > :number2 OR :number2 < :number3 AND size(#path.string1) = :number2) OR (:number2 > :number1 OR  :number3 > :number2 AND :number1 > :number2)) AND (:number1 = :number1 AND :number2 > :number1)",
                    "NOT (:number2 < :number1 OR :number3 < :number2) AND :number2 > :number1"
                ]
