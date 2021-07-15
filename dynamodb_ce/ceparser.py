__all__ = ["CeParser"]

from copy import deepcopy
from decimal import Decimal
from typing import Callable, Dict, Set, Union

import simplejson as json
from boto3.dynamodb.types import (
    BINARY,
    BINARY_SET,
    BOOLEAN,
    LIST,
    MAP,
    NULL,
    NUMBER,
    NUMBER_SET,
    STRING,
    STRING_SET,
    Binary,
    TypeDeserializer,
    TypeSerializer,
)
from sly.yacc import Parser

from .celexer import CeLexer


class CeTypeDeserializer(TypeDeserializer):
    def deserialize(self, value):
        if value and isinstance(value, dict):
            if list(value)[0] in (
                BINARY,
                BINARY_SET,
                BOOLEAN,
                LIST,
                MAP,
                NULL,
                NUMBER,
                NUMBER_SET,
                STRING,
                STRING_SET,
            ):
                value = super().deserialize(value)
            else:
                value = {k: self.deserialize(v) for k, v in value.items()}
        return value.value if isinstance(value, Binary) else value


_TYPE_DESERIALIZER = CeTypeDeserializer()
_TYPE_SERIALIZER = TypeSerializer()

Dynamo = Union[
    Binary, bool, Decimal, dict, list, None, str, Set[Binary], Set[Decimal], Set[str]
]
ExpressionAttributeNames = Dict[str, str]
ExpressionAttributeValues = DynamoItem = Dict[str, Union[Dynamo, Dict[str, Dynamo]]]


class CeParser(Parser):

    _expression_cache: Dict[int, Callable[[DynamoItem], bool]] = dict()

    def __init__(
        self,
        *,
        expression_attribute_names: ExpressionAttributeNames = None,
        expression_attribute_values: ExpressionAttributeValues = None,
    ):
        self._expression_attribute_names: ExpressionAttributeNames = dict()
        self._expression_attribute_values: ExpressionAttributeValues = dict()
        self.expression_attribute_names = expression_attribute_names or dict()
        self.expression_attribute_values = expression_attribute_values or dict()
        self._set_expression_attribute_json()
        super().__init__()

    def _set_expression_attribute_json(self) -> None:
        self._expression_attribute_json = json.dumps(
            self._expression_attribute_names, separators=(",", ":"), use_decimal=True
        ) + json.dumps(
            self._expression_attribute_values, separators=(",", ":"), use_decimal=True
        )

    @property
    def expression_attribute_names(self) -> ExpressionAttributeNames:
        return deepcopy(self._expression_attribute_names)

    @expression_attribute_names.setter
    def expression_attribute_names(
        self, expression_attribute_names: ExpressionAttributeNames
    ) -> None:
        self._expression_attribute_names = (
            deepcopy(expression_attribute_names) or dict()
        )
        self._set_expression_attribute_json()

    @expression_attribute_names.deleter
    def expression_attribute_names(self) -> None:
        self._expression_attribute_names: ExpressionAttributeNames = dict()
        self._set_expression_attribute_json()

    @property
    def expression_attribute_values(self) -> ExpressionAttributeValues:
        return deepcopy(self._expression_attribute_values)

    @expression_attribute_values.setter
    def expression_attribute_values(
        self, expression_attribute_values: ExpressionAttributeValues
    ) -> None:
        self._expression_attribute_values: ExpressionAttributeValues = (
            _TYPE_DESERIALIZER.deserialize(expression_attribute_values) or dict()
        )
        self._set_expression_attribute_json()

    @expression_attribute_values.deleter
    def expression_attribute_values(self) -> None:
        self._expression_attribute_values: ExpressionAttributeValues = dict()
        self._set_expression_attribute_json()

    def evaluate(self, /, expression: str, item: DynamoItem) -> bool:
        return self.parse(expression)(item)

    @classmethod
    def flush_cache(cls) -> None:
        cls._expression_cache: Dict[int, Callable[[DynamoItem], bool]] = dict()

    def parse(self, expression: str) -> Callable[[DynamoItem], bool]:
        expression_hash = hash(expression + self._expression_attribute_json)
        if expression_hash not in self._expression_cache:
            compiled_expression: Callable[[DynamoItem], bool] = super().parse(
                CeLexer().tokenize(expression)
            )

            def truthy(item: DynamoItem) -> bool:
                item = _TYPE_DESERIALIZER.deserialize(item)
                return compiled_expression(item)

            self._expression_cache[expression_hash] = lambda m: truthy(m)
        return self._expression_cache[expression_hash]

    # Get the token list from the lexer (required)
    tokens = CeLexer.tokens

    precedence = (
        ("left", OR),
        ("left", AND),
        ("right", NOT),
        ("right", PARENS),
        ("left", ATTRIBUTE_EXISTS, ATTRIBUTE_NOT_EXISTS, BEGINS_WITH, CONTAINS),
        ("left", BETWEEN),
        ("left", IN),
        ("left", EQ, NE, LT, LTE, GT, GTE),
    )

    # Grammar rules and actions
    @_("operand EQ operand")
    def condition(self, p):
        operand0 = p.operand0
        operand1 = p.operand1
        return lambda m: operand0(m) == operand1(m)

    @_("operand NE operand")
    def condition(self, p):
        operand0 = p.operand0
        operand1 = p.operand1
        return lambda m: operand0(m) != operand1(m)

    @_("operand GT operand")
    def condition(self, p):
        operand0 = p.operand0
        operand1 = p.operand1
        return lambda m: operand0(m) > operand1(m)

    @_("operand GTE operand")
    def condition(self, p):
        operand0 = p.operand0
        operand1 = p.operand1
        return lambda m: operand0(m) >= operand1(m)

    @_("operand LT operand")
    def condition(self, p):
        operand0 = p.operand0
        operand1 = p.operand1
        return lambda m: operand0(m) < operand1(m)

    @_("operand LTE operand")
    def condition(self, p):
        operand0 = p.operand0
        operand1 = p.operand1
        return lambda m: operand0(m) <= operand1(m)

    @_("operand BETWEEN operand AND operand")
    def condition(self, p):
        operand0 = p.operand0
        operand1 = p.operand1
        operand2 = p.operand2
        return lambda m: operand1(m) <= operand0(m) <= operand2(m)

    @_('operand IN "(" in_list ")"')
    def condition(self, p):
        operand = p.operand
        in_list = p.in_list
        return lambda m: operand(m) in in_list(m)

    @_("function")
    def condition(self, p):
        function = p.function
        return lambda m: function(m)

    @_("condition AND condition")
    def condition(self, p):
        condition0 = p.condition0
        condition1 = p.condition1
        return lambda m: condition0(m) and condition1(m)

    @_("condition OR condition")
    def condition(self, p):
        condition0 = p.condition0
        condition1 = p.condition1
        return lambda m: condition0(m) or condition1(m)

    @_("NOT condition")
    def condition(self, p):
        condition = p.condition
        return lambda m: not condition(m)

    @_('"(" condition ")" %prec PARENS')
    def condition(self, p):
        condition = p.condition
        return lambda m: condition(m)

    @_('ATTRIBUTE_EXISTS "(" path ")"')
    def function(self, p):
        path = p.path
        return lambda m: path(m) is not None

    @_('ATTRIBUTE_NOT_EXISTS "(" path ")"')
    def function(self, p):
        path = p.path
        return lambda m: path(m) is None

    @_('ATTRIBUTE_TYPE "(" path "," operand ")"')
    def function(self, p):
        path = p.path
        operand = p.operand
        return lambda m: list(_TYPE_SERIALIZER.serialize(path(m)))[0] == operand(m)

    @_('BEGINS_WITH "(" path "," operand ")"')
    def function(self, p):
        path = p.path
        operand = p.operand
        return (
            lambda m: path(m).startswith(operand(m))
            if isinstance(path(m), str)
            else False
        )

    @_('CONTAINS "(" path "," operand ")"')
    def function(self, p):
        path = p.path
        operand = p.operand
        return (
            lambda m: operand(m) in path(m)
            if isinstance(path(m), (str, set))
            else False
        )

    @_('SIZE "(" path ")"')
    def operand(self, p):
        path = p.path
        return (
            lambda m: len(path(m))
            if isinstance(path(m), (str, set, dict, bytearray, bytes, list))
            else -1
        )

    @_('in_list "," operand')
    def in_list(self, p):
        in_list = p.in_list
        operand = p.operand
        return lambda m: [*in_list(m), operand(m)]

    @_('operand "," operand')
    def in_list(self, p):
        operand0 = p.operand0
        operand1 = p.operand1
        return lambda m: [operand0(m), operand1(m)]

    @_("path")
    def operand(self, p):
        return p.path

    @_("VALUE")
    def operand(self, p):
        VALUE = p.VALUE
        expression_attribute_values = self._expression_attribute_values
        return lambda m: expression_attribute_values.get(VALUE)

    @_('path "." NAME')
    def path(self, p):
        path = p.path
        NAME = p.NAME
        return lambda m: path(m).get(NAME) if path(m) else None

    @_('path "." NAME_REF')
    def path(self, p):
        path = p.path
        NAME_REF = p.NAME_REF
        expression_attribute_names = self._expression_attribute_names
        return (
            lambda m: path(m).get(expression_attribute_names.get(NAME_REF))
            if path(m)
            else None
        )

    @_('path "[" INDEX "]"')
    def path(self, p):
        path = p.path
        INDEX = p.INDEX
        return (
            lambda m: path(m)[INDEX]
            if isinstance(path(m), list) and len(path(m)) > INDEX
            else None
        )

    @_("NAME")
    def path(self, p):
        NAME = p.NAME
        return lambda m: m.get(NAME)

    @_("NAME_REF")
    def path(self, p):
        NAME_REF = p.NAME_REF
        expression_attribute_names = self._expression_attribute_names
        return lambda m: m.get(expression_attribute_names.get(NAME_REF))
