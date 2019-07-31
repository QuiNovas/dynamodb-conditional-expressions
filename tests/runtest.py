#!/usr/bin/env python3.7
import sys
from os.path import dirname, join, abspath
from CeTests import *

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

test = inList()
test.run()

test = attribute_exists()
test.run()

test = attribute_not_exists()
test.run()

test = attribute_type()
test.run()

test = begins_with()
test.run()

test = size()
test.run()

test = Not()
test.run()

test = And()
test.run()

test = Or()
test.run()

test = precedence()
test.run()
