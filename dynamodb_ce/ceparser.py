__all__ = ['CeParser']
from boto3.dynamodb.types import TypeSerializer, TypeDeserializer
from celexer import CeLexer
from sly import Parser
from decimal import *
_TYPE_DESERIALIZER = TypeDeserializer()
_TYPE_SERIALIZER = TypeSerializer()

class CeParser(Parser):

  _expression_cache = {}

  def __init__(self):
    self._expression_attribute_names = {}
    self._expression_attribute_values = {}
    super().__init__()

  @property
  def expression_attribute_names(self):
    return self._expression_attribute_names

  @expression_attribute_names.setter
  def expression_attribute_names(self, expression_attribute_names={}):
    assert expression_attribute_names, 'expression_attribute_names is None'
    self._expression_attribute_names = expression_attribute_names

  @expression_attribute_names.deleter
  def expression_attribute_names(self):
    self._expression_attribute_names = {}

  @property
  def expression_attribute_values(self):
    return self._expression_attribute_values

  @expression_attribute_values.setter
  def expression_attribute_values(self, expression_attribute_values={}):
    assert expression_attribute_values, 'expression_attribute_values is None'
    self._expression_attribute_values = expression_attribute_values

  @expression_attribute_values.deleter
  def expression_attribute_values(self):
    self._expression_attribute_values = {}

  def evaluate(self, expression, item):
    return self.parse(expression)(item)

  def flush_cache(self):
    _expression_cache = {}

  def parse(self, expression):
    if expression not in self._expression_cache:
      self._expression_cache[expression] = super().parse(CeLexer().tokenize(expression))
    return self._expression_cache[expression]

  # Get the token list from the lexer (required)
  tokens = CeLexer.tokens

  # Define precendence
  precendence = (
    ('left', OR),
    ('left', AND),
    ('right', NOT),
 )

  # Internal helper to deference attribute values
  def _get_expression_attribute_value(self, value_name):
    value = self._expression_attribute_values.get(value_name)
    return _TYPE_DESERIALIZER.deserialize(value) if value else None

  # Grammar rules and actions
  @_('operand EQ operand')
  def condition(self, p):
    operand0 = p.operand0
    operand1 = p.operand1
    return lambda m: operand0(m) == operand1(m)

  @_('operand NE operand')
  def condition(self, p):
    operand0 = p.operand0
    operand1 = p.operand1
    return lambda m: operand0(m) != operand1(m)

  @_('operand GT operand')
  def condition(self, p):
    operand0 = p.operand0
    operand1 = p.operand1
    return lambda m: operand0(m) > operand1(m)

  @_('operand GTE operand')
  def condition(self, p):
    operand0 = p.operand0
    operand1 = p.operand1
    return lambda m: operand0(m) >= operand1(m)

  @_('operand LT operand')
  def condition(self, p):
    operand0 = p.operand0
    operand1 = p.operand1
    return lambda m: operand0(m) < operand1(m)

  @_('operand LTE operand')
  def condition(self, p):
    operand0 = p.operand0
    operand1 = p.operand1
    return lambda m: operand0(m) <= operand1(m)

  @_('operand BETWEEN operand AND operand')
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

  @_('function')
  def condition(self, p):
    function = p.function
    return lambda m: function(m)

  @_('condition AND condition')
  def condition(self, p):
    condition0 = p.condition0
    condition1 = p.condition1
    return lambda m: condition0(m) and condition1(m)

  @_('condition OR condition')
  def condition(self, p):
    condition0 = p.condition0
    condition1 = p.condition1
    return lambda m: condition0(m) or condition1(m)

  @_('NOT condition')
  def condition(self, p):
    condition = p.condition
    return lambda m: not condition(m)

  @_('"(" condition ")"')
  def condition(self, p):
    condition = p.condition
    return lambda m: condition(m)

  @_('ATTRIBUTE_EXISTS "(" path ")"')
  def function(self, p):
    path = p.path
    return lambda m: path(m) is not None

  @_('ATRIBUTE_NOT_EXISTS "(" path ")"')
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
    return lambda m: path(m).startswith(operand(m)) if isinstance(path(m), str) else False

  @_('CONTAINS "(" path "," operand ")"')
  def function(self, p):
    path = p.path
    operand = p.operand
    return lambda m: operand(m) in path(m) if isinstance(path(m), (str, set)) else False

  @_('SIZE "(" path ")"')
  def operand(self, p):
    path = p.path
    return lambda m: len(path(m)) if isinstance(path(m), (str, set, dict, bytearray, bytes, list)) else -1

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

  @_('path')
  def operand(self, p):
    return p.path

  @_('VALUE')
  def operand(self, p):
    VALUE = p.VALUE
    return lambda m: self._get_expression_attribute_value(VALUE)

  @_('path "." NAME')
  def path(self, p):
    path = p.path
    NAME = p.NAME
    return lambda m: path(m).get(NAME) if path(m) else None

  @_('path "." NAME_REF')
  def path(self, p):
    path = p.path
    NAME_REF = p.NAME_REF
    return lambda m: path(m).get(self._expression_attribute_names.get(NAME_REF)) if path(m) else None

  @_('path "[" INDEX "]"')
  def path(self, p):
    path = p.path
    INDEX = p.INDEX
    return lambda m: path(m)[INDEX] if isinstance(path(m), list) and len(path(m)) > INDEX else None

  @_('NAME')
  def path(self, p):
    NAME = p.NAME
    return lambda m: m.get(NAME)

  @_('NAME_REF')
  def path(self, p):
    NAME_REF = p.NAME_REF
    return lambda m: m.get(self._expression_attribute_names.get(NAME_REF))
