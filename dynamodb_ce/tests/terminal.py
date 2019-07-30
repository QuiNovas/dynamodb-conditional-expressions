#!/usr/bin/env python

from dynamodb_ce import CeParser

message = {"body": {"number1": 1, "number2": 2, "string1": "a", "string2": "b"}}
p = CeParser()
p._expression_attribute_names = {"#path": "body"}
p._expression_attribute_values = {':string1': {'S': "a"}, ':string2': {'S': "b"}, ':number1': {'N': 1}, ':number2': {'N': 2}}

while True:
        try:
            expr = input('QUERY > ')
            result = p.evaluate(expr, message)
            print(result)
        except EOFError:
            pass
        except TypeError:
            print("Unknown type or type error")
        except Exception as e:
            print(e)
