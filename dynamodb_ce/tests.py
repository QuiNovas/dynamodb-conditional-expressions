#!python3.7

from ceparser import CeParser
from celexer import CeLexer
import inspect
from pprint import pprint

class TestUnit(object):
    lexer = CeLexer()
    parser = CeParser()

    def getResult(self, expr, result):
        stack = inspect.stack()[2][4][0]
        testUnit = stack.split('.')[0]
        if result:
            result = "PASSED: "
            return "\033[1;32;40m " + testUnit + " " + result + "at case -> " + expr + " \033[01;37;40m"
        else:
            result = "FAILED: "
            return "\033[1;31;40m " + testUnit + " " + result + "at case -> " + expr + " \033[01;37;40m"


    def run(self):
        for expr in self.expressions:
            try:
                result = self.getResult(expr, self.parser.evaluate(expr, self.message))
                print(result)
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
        self.message = {"body": {"number1": 1, "number2": 2, "string1": "a", "string2": "b"}}
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
        self.message = {"body": {"number1": 1, "number2": 2, "number3": 3, "string1": "a", "string2": "b", "string3": "c", "numberList": [1,2,3]}}
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
        self.parser._expression_attribute_names = {"#path": "body"}
        self.parser._expression_attribute_values = {':string1': {'S': "a"}, ':string2': {'S': "b"}, ':string3': {'S': "c"}, ':number1': {'N': 1}, ':number2': {'N': 2}, ':number3': {'N': 3}, "map": {"M": {"mapkey": "mapval"}}}
        self.message = {"body": {"number1": 1, "number2": 2, "number3": 3, "string1": "a", "string2": "b", "string3": "c", "numberList": [1,2,3], "map": {"mapkey": "mapvalue"}}}
        self.expressions = [
            "attribute_exists(#path.string1)",
            "attribute_exists(#path.number1)",
            "attribute_exists(#path.numberList[0])",
            "attribute_exists(#path.map.mapkey5)"
        ]

class attribute_not_exists(TestUnit):
    def __init__(self):
        print(" \033[01;37;40m \n Starting test for " + inspect.stack()[1][4][0].split('.')[0].split('=')[-1])
        self.parser._expression_attribute_names = {"#path": "body"}
        self.parser._expression_attribute_values = {':string1': {'S': "a"}, ':string2': {'S': "b"}, ':string3': {'S': "c"}, ':number1': {'N': 1}, ':number2': {'N': 2}, ':number3': {'N': 3}, "map": {"M": {"mapkey": "mapval"}}}
        self.message = {"body": {"number1": 1, "number2": 2, "number3": 3, "string1": "a", "string2": "b", "string3": "c", "numberList": [1,2,3], "map": {"mapkey": "mapvalue"}}}
        self.expressions = [
            "attribute_not_exists(#path.number1)",
        ]

class attribute_type(TestUnit):
    def __init__(self):
        print(" \033[01;37;40m \n Starting test for " + inspect.stack()[1][4][0].split('.')[0].split('=')[-1])
        self.parser._expression_attribute_names = {"#path": "body"}
        self.parser._expression_attribute_values = {
                                                    	':string1': {
                                                    		'S': "a"
                                                    	},
                                                    	':string2': {
                                                    		'S': "b"
                                                    	},
                                                    	':string3': {
                                                    		'S': "c"
                                                    	},
                                                    	':number1': {
                                                    		'N': 1
                                                    	},
                                                    	':number2': {
                                                    		'N': 2
                                                    	},
                                                    	':number3': {
                                                    		'N': 3
                                                    	},
                                                        ':stringType': {
                                                            'S': 'S'
                                                        },
                                                        ':numberType': {
                                                            'S': 'N'
                                                        },
                                                        ':mapType': {
                                                            'S': 'M'
                                                        },
                                                        ":listType": {
                                                            'S': 'L'
                                                        },
                                                    	"map": {
                                                    		"M": {
                                                    			"mapkey": "mapval"
                                                    		}
                                                    	}
                                                    }
        self.message = {
                        	"body": {
                        		"number1": 1,
                        		"number2": 2,
                        		"number3": 3,
                        		"string1": "a",
                        		"string2": "b",
                        		"string3": "c",
                        		"numberList": [1, 2, 3],
                        		"map": {
                        			"mapkey": "mapvalue"
                        		}
                        	}
                        }
        self.expressions = [
            "attribute_type( #path.string1, :stringType )",
            "attribute_type( #path.number1, :numberType )",
            "attribute_type( #path.map, :mapType )",
            "attribute_type( #path.numberList, :listType )",
        ]

"""
test = greaterThan()
test.run()

test = greaterThanOrEqual()
test.run()

test = lessThanOrEqual()
test.run()

test = lessThan()
test.run()

test = equal()
test.run()

test = notEqual()
test.run()

test = between()
test.run()
"""
test = inList()
test.run()
"""
test = attribute_exists()
test.run()

test = attribute_not_exists()
test.run()

"""
test = attribute_type()
test.run()
