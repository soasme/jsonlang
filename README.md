# jsonlang

JSONLang is a programming language written in JSON format.

## Quick Start

Using Python Implement:

    $ cd python
    $ python jsonlang.py
    >> exit

Type `exit` to quit.

## Examples

### $if

    >> {"$if": true, "$then": 1, "$else": 2 }
    1

### $empty

    >> {"$empty": "A" }
    True

### $assign

    >> {"$assign": "A", "$to", 1}
    1

    >> {"$empty": "A"}
    False

### $eq

    >> {"$eq": "A", "$to": 1}
    True
    >> {"$if": {"$eq": "A", "$to": 1}, "$then": {"$assign": "A", "$to": 2}}
    2
    >> {"$eq": "A", "$to": 2}
    True

### $not

    >> {"$not": {"$empty": "A"}}
    True
