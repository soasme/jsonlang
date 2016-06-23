# -*- coding: utf-8 -*-

from jsonlang import exec_jsonlang, exec_jsonlang_code, undefined

def test_assign():
    assert exec_jsonlang([
        {
            "$assign": "Field",
            "$to": "Data"
        }
    ], {
        'Field': "Value"
    }) == {
        'Field': 'Data'
    }


def test_if_then():
    assert exec_jsonlang([
        {
            "$if": {
                '$empty': {'$ref': 'Field'}
            },
            "$then": {
                "$assign": "Field",
                "$to": "Data"
            }
        }
    ]) == {'Field': 'Data'}

def test_if_expr():
    assert exec_jsonlang_code({
        '$if': False,
        "$then": 1,
        "$else": 2,
    }, {}) == 2
    assert exec_jsonlang_code({
        '$if': True,
        "$then": 1,
        "$else": 2,
    }, {}) == 1

def test_if_not_then():
    assert exec_jsonlang([
        {
            "$if": {
                '$not': {
                    '$empty': 'Field'
                }
            },
            "$then": {
                "$assign": "Field",
                "$to": "Modified"
            }
        }
    ], {
        'Field': 'Data'
    }) == {'Field': 'Modified'}


def test_if_then_else():
    assert exec_jsonlang([
        {
            "$if": {
                '$not': {
                    '$empty': {'$ref': 'Field'}
                }
            },
            "$then": {
                "$assign": "Field",
                "$to": "ModifiedThen"
            },
            '$else': {
                "$assign": "Field",
                "$to": "ModifiedElse"
            }
        }
    ]) == {
        'Field': 'ModifiedElse'
    }

def test_eq_to():
    assert not exec_jsonlang_code({'$eq': 'A', '$to': 1}, {'A': 2})
    assert exec_jsonlang_code({'$eq': 'A', '$to': 1}, {'A': 1})

def test_eq_toref():
    assert not exec_jsonlang_code({'$eq': 'A', '$toref': 'B'}, {'A': 1, 'B': 2})
    assert exec_jsonlang_code({'$eq': 'A', '$toref': 'B'}, {'A': 1, 'B': 1})


def test_resolve_ref():
    assert exec_jsonlang_code({'$ref': 'A'}, {'A': 1}) == 1
    assert exec_jsonlang_code({'$ref': 'A'}, {}) == undefined

def test_deref():
    assert not exec_jsonlang_code({'$deref': "A"}, {"A": 1})
