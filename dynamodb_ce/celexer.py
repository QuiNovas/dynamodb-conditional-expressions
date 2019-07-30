from sly import Lexer

class CeLexer(Lexer):
  # Set of token names.
  tokens = {
    NAME,
    NAME_REF,
    VALUE,
    INDEX,
    BETWEEN,
    AND,
    OR,
    NOT,
    IN,
    EQ,
    NE,
    GT,
    GTE,
    LT,
    LTE,
    ATTRIBUTE_EXISTS,
    ATRIBUTE_NOT_EXISTS,
    ATTRIBUTE_TYPE,
    BEGINS_WITH,
    CONTAINS,
    SIZE
  }

  # Set of literal characters
  literals = {
    '(',
    ')',
    '[',
    ']',
    ',',
    '.'
  }

  # String containing ignored characters
  ignore = ' \t'

  # Regular expression rules for tokens
  NAME_REF            = r'\#[a-zA-Z0-9]+'
  VALUE               = r'\:[a-zA-Z0-9]+'
  BETWEEN             = r'BETWEEN'
  AND                 = r'AND'
  OR                  = r'OR'
  NOT                 = r'NOT'
  IN                  = r'IN'
  ATTRIBUTE_EXISTS    = r'attribute_exists'
  ATRIBUTE_NOT_EXISTS = r'attribute_not_exists'
  ATTRIBUTE_TYPE      = r'attribute_type'
  BEGINS_WITH         = r'begins_with'
  CONTAINS            = r'contains'
  SIZE                = r'size'
  NAME                = r'[a-zA-Z][a-zA-Z0-9]+'
  NE                  = r'<>'
  GTE                 = r'>='
  LTE                 = r'<='
  EQ                  = r'='
  GT                  = r'>'
  LT                  = r'<'

  @_(r'\d+')
  def INDEX(self, t):
    t.value = int(t.value)
    return t

  # Line number tracking
  @_(r'\n+')
  def ignore_newline(self, t):
      self.lineno += t.value.count('\n')

  def error(self, t):
      print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
      self.index += 1
