#!/usr/bin/env python

from dynamodb_ce import CeParser
import sys
import argparse
import os.path
import json
try:
    from prompt_toolkit import prompt
    from prompt_toolkit.history import FileHistory
    from prompt_toolkit.completion import WordCompleter
    import click
except:
    print("Modules prompt-toolkit and click required")
    sys.exit(1)

def getNames():
    global p
    filepath = os.environ['HOME'] + '/.dynamodb-term.names.txt'
    if os.path.isfile(filepath) and os.stat(filepath).st_size != 0:
        with open(filepath) as f:
            return json.load(f)
    else:
        return ""

def setNames(names):
    global p
    filepath = os.environ['HOME'] + '/.dynamodb-term.names.txt'
    try:
        with open(filepath, 'w') as f:
                json.dump(names, f)
    except:
        print("Invalid attribute_names or attribute_names format")

def getValues():
    global p
    filepath = os.environ['HOME'] + '/.dynamodb-term.values.txt'
    if os.path.isfile(filepath) and os.stat(filepath).st_size != 0:
        with open(filepath) as f:
            return json.load(f)
    else:
        return ""

def setValues(values):
    global p
    filepath = os.environ['HOME'] + '/.dynamodb-term.values.txt'
    try:
        with open(filepath, 'w') as f:
            json.dump(values, f)
    except:
        print("Invalid attribute_values or attribute_values format")

def getMessage():
    filepath = os.environ['HOME'] + '/.dynamodb-term.message.txt'
    try:
        with open(filepath) as f:
            return json.load(f)
    except:
        return ""

def setMessage(msg):
    filepath = os.environ['HOME'] + '/.dynamodb-term.message.txt'
    try:
        with open(filepath) as f:
            json.dump(msg, f)
    except:
        print("Invalid message or message format")

def helpMsg():
    print("""
        -------------------------------------------------
                dynamodb-ce command line CeParser
        -------------------------------------------------
            commands:
                \pn     Print attribute_names
                \pv     Print attribute_values
                \pm     Print message
                \sn     Set attribute_names in editor
                \sv     Set attribute_values in editor
                \sm     Set message in editor
                \e      Exit the commandline
                \h      Print this help message
        -------------------------------------------------
        """
    )

def parseCmd(cmd):
    global p
    global message
    try:
        if cmd == r'\pn': # print names
            print(getNames())

        elif cmd == r'\pv': # print values
            print(getValues())

        elif cmd == r'\pm': # print message
            print(getMessage())

        elif cmd == r'\sm':
            m = click.edit(getMessage())
            if m == getMessage() or m == None:
                print("No changes made")
            else:
                setMessage(m)
                print("Message updated")

        elif cmd == r'\sn':
            m = click.edit(getNames())
            if m == getNames() or m == None:
                print("No changes made")
            else:
                setNames(m)
                print("Attribute names updated")

        elif cmd == r'\sv':
            m = click.edit(getValues())
            if m == getValues() or m == None:
                print("No changes made")
            else:
                setValues(m)
                print("Attribute values updated")

        elif cmd == r'\e':
            print("Exiting")
            sys.exit(0)

        elif cmd == r'\\':
            print("Unknown command or syntax error")
            helpMsg()

        else:
            print("Unknown command or syntax error")
            helpMsg()
    except Exception as e:
        print(e)
        print("Invalid input")
        helpMsg()


def runParser():
    helpMsg()

    p = CeParser()
    completer = WordCompleter(["\\sn", "\\sm", "\\sv", "\\pm", "\\pn", "\\pv", "\\e"])

    if not getMessage():
        print("No message defined. Set one with \\sm")
    if not getValues():
        print("No attribute_values defined. Set with \\sv")
    if not getNames():
        print("No names defined. Set with \\sn")

    while True:
            try:
                expr = prompt('EVALUATE >', history=FileHistory(os.environ['HOME'] + '/.dynamodb-term.history.txt'), completer=completer,complete_while_typing=True)
                if expr[0] == '\\':
                    parseCmd(expr)
                else:
                    p._expression_attribute_names = getNames()
                    p._expression_attribute_values = getValues()
                    message = getMessage()
                    result = p.evaluate(expr, message)
                    print(result)
            except KeyboardInterrupt:
                print('Canceled')
            except EOFError:
                pass
            except TypeError:
                print("Unknown type or type error. You may want to check your JSON")
            except Exception as e:
                print(e)

runParser()
