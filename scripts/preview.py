#!/usr/bin/env python3
"""Render using GitHub's Markdown API; optionally serve a local-only preview.

Requires an authenticated gh CLI. Nothing is committed or published.
"""
import argparse
import html
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def render():
    git_dir = Path(subprocess.check_output(['git', 'rev-parse', '--absolute-git-dir'], cwd=ROOT, text=True).strip())
    output = git_dir / 'profile-preview'
    output.mkdir(exist_ok=True)
    payload = dict(text=(ROOT/'README.md').read_text(), mode='gfm', context='tejask-dev/tejask-dev')
    rendered = subprocess.run(['gh', 'api', '--method', 'POST', 'markdown', '--input', '-'], input=json.dumps(payload), text=True, capture_output=True, check=True).stdout
    (output/'github-render.html').write_text(rendered)
    # GitHub's page layer supplies heading anchors after Markdown rendering.
    def heading(match):
        level, attrs, content = match.groups()
        plain = html.unescape(re.sub('<[^>]*>', '', content)).lower()
        slug = re.sub(r'[^\w\- ]', '', plain).replace(' ', '-')
        return f'<h{level} id="{slug}"{attrs}>{content}</h{level}>'
    rendered = re.sub(r'<h([1-6])([^>]*)>(.*?)</h\1>', heading, rendered)
    rendered = rendered.replace('assets/profile/', '/assets/profile/')
    req = Request('https://github.com/tejask-dev', headers={'User-Agent': 'profile-readme-preview'})
    with urlopen(req, timeout=30) as response:
        github = response.read().decode()
    css = re.findall(r'<link[^>]*rel="stylesheet"[^>]*href="(https://github.githubassets.com/[^\"]+)"', github)
    if not css:
        raise RuntimeError('Could not discover GitHub stylesheets; refusing an unstyled preview.')
    links = ''.join(f'<link rel="stylesheet" href="{html.escape(url)}">' for url in css)
    for theme in ('light','dark'):
        doc = f'''<!doctype html><html lang="en" data-color-mode="{theme}" data-light-theme="light" data-dark-theme="dark">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tejas Kaushik · profile preview · {theme}</title>{links}
<style>html{{color-scheme:{theme}}}body{{margin:0;background:var(--bgColor-default);color:var(--fgColor-default)}}main{{box-sizing:border-box;max-width:928px;margin:24px auto;padding:32px;border:1px solid var(--borderColor-default);border-radius:6px}}@media(max-width:600px){{main{{margin:0;padding:20px 16px;border:0}}}}</style></head>
<body><main class="markdown-body">{rendered}</main></body></html>'''
        # Match GitHub's selected theme even if the local OS uses another one.
        doc = doc.replace('(prefers-color-scheme: dark)', '(min-width: 0px)' if theme == 'dark' else '(max-width: 0px)')
        (output/f'{theme}.html').write_text(doc)
    return output


def serve(output, port):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            route = urlparse(self.path).path
            if route in ('/', '/light.html', '/dark.html'):
                path = output/('dark.html' if route == '/' else route[1:])
                mime = 'text/html; charset=utf-8'
            elif re.fullmatch(r'/assets/profile/[a-z0-9-]+\.svg', route):
                path, mime = ROOT/route[1:], 'image/svg+xml'
            elif route in ('/data/activity.json','/docs/PROFILE-DESIGN.md','/.github/workflows/profile-activity.yml'):
                path, mime = ROOT/route[1:], 'text/plain; charset=utf-8'
            else:
                self.send_error(404)
                return
            if not path.is_file():
                self.send_error(404)
                return
            data = path.read_bytes()
            self.send_response(200)
            self.send_header('Content-Type', mime)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(data)
    print(f'Local preview: http://127.0.0.1:{port}/dark.html (or /light.html)', flush=True)
    HTTPServer(('127.0.0.1', port), Handler).serve_forever()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--serve', action='store_true')
    parser.add_argument('--port', type=int, default=8766)
    args = parser.parse_args()
    directory = render()
    print(f'Rendered through GitHub Markdown API: {directory}', flush=True)
    if args.serve:
        serve(directory, args.port)
