#!/usr/bin/env python3

# cf. https://github.com/jlowin/fastmcp/blob/main/docs/clients/client.mdx

#
#  MCP client to send request server in pure MCP
#   - get mcp server info to connect.
#   - send request to MCP server.
#

from fastmcp import FastMCP, Client
from typing import Any
import httpx
import yaml
import json
import argparse
import sys
import asyncio
import logging
from fastmcp.utilities.logging import get_logger
from collections import defaultdict

for comp in [ "fastmcp.experimental.utilities.openapi.director",
              "fastmcp.experimental.server.openapi.components",
              "fastmcp.experimental.server.openapi.server" ]:
    get_logger(comp).setLevel(logging.DEBUG)

#logging.basicConfig(level=logging.DEBUG) # Configure root logger


def load(path:str='/dev/stdin') -> Any:
    """load json|yaml|text(url) from file"""

    with open(path, "r", encoding='utf-8') as fp:
        c = fp.read() # read as text

        for loader in [ json.loads, yaml.safe_load ]:
        # for each supporting format
            try:
                d = loader(c)
                return d
            except Exception as e:
                continue
        return c



async def test(cli) -> Any:

    rtn = defaultdict(list[Any])

    cmds = [
             ( 'tools', cli.list_tools )
            ,( 'resources', cli.list_resources )
            ,( 'resource_templates', cli.list_resource_templates )
            ,( 'prompts', cli.list_prompts )
           ]

    async with cli:
      for k, op in cmds:
        tmp = await op()
        print(f'{k} {tmp=}', file=sys.stderr)
        rtn[k] = tmp

    print(f'{rtn}', file=sys.stderr)


if __name__ == '__main__':


    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--spec',      help='mcpServeers config to connect (json/yaml/text[url])', default='/dev/stdin')
    parser.add_argument('-d', '--log_level', help='MCP log level',                      default='DEBUG')
    opts = parser.parse_args()

    opts.headers = {}

    spec = load(opts.spec)
    client = Client(spec)
    #exit(0)

    asyncio.run( test(client) )
