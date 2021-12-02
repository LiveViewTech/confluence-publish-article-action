from typing import Dict, List
from os import listdir, environ
from os.path import join

import requests
from markdown import markdown
from mdx_gfm import GithubFlavoredMarkdownExtension


workspace = environ.get('GITHUB_WORKSPACE')
if not workspace:
    raise Exception('No workspace is set')

envs: Dict[str, str] = {}
for key in ['src', 'pageId', 'cloudId', 'user', 'token']:
    value = environ.get(f'INPUT_{key.upper()}')
    if not value:
        raise Exception(f'Missing value for {key}')
    envs[key] = value
src, pageId, cloudId, user, token = envs

with open(join(workspace, src)) as f:
    md = f.read()

url = f"https://{cloudId}.atlassian.net/wiki/rest/api/content/{pageId}"
current = requests.get(url, auth=(user, token)).json()
html = markdown(md, extensions=[GithubFlavoredMarkdownExtension()])
content = {
    'id': current['id'],
    'type': current['type'],
    'title': current['title'],
    'version': {'number': current['version']['number'] + 1},
    'body': {
        'editor': {
            'value': html,
            'representation': 'editor'
        }
    }
}

updated = requests.put(url, json=content, auth=(user, token)).json()
link = updated['_links']['base'] + updated['_links']['webui']
print(f'Uploaded content successfully to page {link}')
