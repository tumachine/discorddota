#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Response template, this is used so we can pass the response as an object"""

import json
from .exceptions import *


class Dota2Dict(dict):
    pass


def build(req, url=None):
    if isinstance(req, bytes):
        req_resp = json.loads(req.decode('utf8'))
    else:
        req_resp = req.json()
    if 'result' in req_resp:
        if 'error' in req_resp['result']:
            raise APIError(req_resp['result']['error'])
        if 'status' in req_resp['result']:
            if not (1 == req_resp['result']['status'] == 200):
                try:
                    raise APIError(req_resp['result']['statusDetail'])
                except KeyError:
                    pass
        resp = Dota2Dict(req_resp['result'])
    elif 'response' in req_resp:
        resp = Dota2Dict(req_resp['response'])
    elif isinstance(req_resp, list):
        resp = Dota2Dict({"results": req_resp})
    else:
        resp = Dota2Dict(req_resp)

    resp.url = url
    resp.json = json.dumps(resp, ensure_ascii=False)

    return resp
