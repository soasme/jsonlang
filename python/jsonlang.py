# -*- coding: utf-8 -*-

import json

def help():
    print "type exit to quit program. enter valid json content please."

def eval_jsonlang():
    env = {}
    construct_env(env)
    help()
    while True:
        try:
            code = raw_input('>> ')
            if code == 'exit':
                exit(0)
            elif code == 'help':
                help()
                continue
            elif code == 'env':
                print env
                continue
            loaded = json.loads(code)
            print exec_jsonlang_code(loaded, env)
        except Exception as exc:
            print 'Error: ', exc


class Undefined(object):

    def __nonzero__(self):
        return False

    def __str__(self):
        return 'undefined'

undefined = Undefined()

def exec_jsonlang(codes, env=None):
    env = env or {}
    for code in codes:
        exec_jsonlang_code(code, env)
    destruct_env(env)
    return env

def exec_jsonlang_code(code, env):
    if isinstance(code, bool):
        return code
    elif isinstance(code, str):
        return code
    elif isinstance(code, int):
        return code
    elif '$ref' in code:
        return exec_ref_code(code, env)
    elif '$deref' in code:
        return exec_deref_code(code, env)
    elif '$assign' in code:
        return exec_assign_code(code, env)
    elif '$if' in  code:
        return exec_if_code(code, env)
    elif '$empty' in code:
        return exec_empty_code(code, env)
    elif '$eq' in code:
        return exec_eq_code(code, env)
    elif '$not' in code:
        return exec_not_code(code, env)
    elif '$local' in code:
        return exec_local_code(code, env)
    else:
        return code

def exec_ref_code(code, env):
    ref = str(exec_jsonlang_code(code['$ref'], env))
    if ref.startswith('$$'):
        return env.get('___local___', {}).get(ref, undefined)
    elif ref in env:
        return env[ref]
    return undefined

def exec_deref_code(code, env):
    ref = str(exec_jsonlang_code(code['$deref'], env))
    if ref.startswith('$$'):
        if '___local___' in env and ref in env['___local___']:
            del env['___local___'][ref]
    if ref in env:
        del env[ref]

def set_assignment_to_env(env, key, value):
    env[key] = value

def exec_assign_code(code, env):
    key = code['$assign']
    newvalue = code['$to']
    set_assignment_to_env(env, key, newvalue)
    return newvalue

def exec_if_code(code, env):
    dollar_if = code['$if']
    dollar_then = code['$then']
    dollar_else = code.get('$else')
    if exec_if_condition_code(dollar_if, env):
        if isinstance(dollar_then, list):
            return exec_jsonlang(dollar_then, env)
        elif isinstance(dollar_then, dict):
            return exec_jsonlang_code(dollar_then, env)
        else:
            return dollar_then
    else:
        if isinstance(dollar_else, list):
            return exec_jsonlang(dollar_else, env)
        elif isinstance(dollar_else, dict):
            return exec_jsonlang_code(dollar_else, env)
        else:
            return dollar_else

def exec_if_condition_code(code, env):
    if isinstance(code, bool):
        return code
    return bool(exec_jsonlang_code(code, env))

def exec_empty_code(code, env):
    return bool(not exec_jsonlang_code(code['$empty'], env))

def exec_eq_code(code, env):
    if "$to" in code:
        return env.get(code.get('$eq')) == code.get('$to')
    elif '$toref' in code:
        return env.get(code.get('$eq')) == env.get(code.get('$toref'))
    return False

def exec_local_code(code, env):
    env.setdefault('___local___', {})
    assert code['$local'].startswith('$$'), 'Local value must start with $$.'
    if '$to' in code:
        env['___local___'][code['$local']] = exec_jsonlang_code(code['$to'], env)
    else:
        env['___local___'][code['$local']] = undefined
    return env['___local___'][code['$local']]

def exec_not_code(code, env):
    return not exec_jsonlang_code(code.get('$not'), env)

def destruct_env(env):
    if '___local___' in env:
        del env['___local___']

def construct_env(env=None):
    return dict(env or {})

if __name__ == '__main__':
    import sys

    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            exec_jsonlang(json.loads(f.read()))
    else:
        eval_jsonlang()
