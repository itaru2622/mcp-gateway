#!/usr/bin/env python3

# cf. https://github.com/jlowin/fastmcp/blob/main/docs/integrations/openapi.mdx
# cf. https://qiita.com/__Kat__/items/8e0144c19aa3079f1b6b

#
#  trying to gateway from existing REST server for User/AI/LLM with:
#   - load openAPI spec file,
#   - generate MCP server for AI/LLM for the above spec.
#   - message forwarding among User/AI/LLM <=> MCP <=> existing REST server.
#

from fastmcp import FastMCP
from fastmcp.server.openapi import ( FastMCPOpenAPI, RouteMap, MCPType,)
from typing import Any
import httpx
import yaml
import json
import argparse
import sys


def load(path:str='/dev/stdin') -> Any:
    """load json/yaml from file"""

    with open(path, "r", encoding='utf-8') as fp:
        c = fp.read()
        try: # try json first
            d = json.loads(c)
        except: # if failed, try yaml
            d = yaml.safe_load(c)
        return d


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--spec',      help='OpenAPI spec file for gateway (json/yaml)', default='/dev/stdin')
    parser.add_argument('-b', '--baseURL',   help='baseURL to REST Server',                    default='')
    parser.add_argument('-a', '--token',     help='bearer token to REST server',               default=None)
    parser.add_argument('-t', '--transport', help='MCP server transport',                      default='stdio')
    parser.add_argument('-p', '--port',      help='MCP server port',                           default=8888)
    parser.add_argument('-H', '--host',      help='MCP server host to listen',                 default='0.0.0.0')
    opts = parser.parse_args()

    opts.headers = {}

    if opts.token not in [None, '']:
         opts.headers.update(Authorization=f'Bearer {opts.token}')
    print(f"opts: ########### {opts}", file=sys.stderr)
#   exit(0)
    
    route_maps=[RouteMap(mcp_type=MCPType.TOOL)] # all routes as tool
    spec = load(opts.spec)

    # cli to access REST Server.
    cli = httpx.AsyncClient()
    #cli = httpx.AsyncClient(base_url=opts.baseURL, headers=opts.headers ) # cli to REST Server.

    mcp = FastMCP.from_openapi(spec, client=cli, route_maps=route_maps)

    kwargs = dict(transport=opts.transport)
    if opts.transport not in ['stdio']:
      kwargs = { k : opts['k']   for k in ['host', 'port', 'transport' ] }

    print(f"{kwargs=}", file=sys.stderr)
    #mcp.run(**kwargs) # not yet...
    exit(0)
