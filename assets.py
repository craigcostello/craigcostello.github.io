"""Prepare local slide previews and maintain the public asset manifest."""
import concurrent.futures
import hashlib
import json
import mimetypes
import pathlib
import shutil
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent

def read(name):
    return json.loads((ROOT / 'content' / f'{name}.json').read_text())

def write(name, value):
    (ROOT / 'content' / f'{name}.json').write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def refresh_manifest():
    previous = {item['local_url']: item for item in read('assets')}
    provenance = {}
    for item in read('media'):
        if item.get('local_image') and item.get('image_url'):
            provenance[item['local_image']] = {'original_url': item['image_url'], 'referring_page': item.get('image_source_page') or item['links'][0]['original_url']}
    for item in read('branding').values():
        if item.get('local_url') and item.get('source_url'):
            provenance[item['local_url']] = {'original_url': item['source_url']}
    for item in read('talks'):
        if item.get('preview_image') and item.get('preview_source'):
            provenance[item['preview_image']] = {'generated_from': item['preview_source']}
    assets = []
    for path in sorted((ROOT / 'public').rglob('*')):
        if not path.is_file() or any(part.startswith('.') for part in path.relative_to(ROOT / 'public').parts):
            continue
        url = '/' + path.relative_to(ROOT / 'public').as_posix()
        entry = dict(previous.get(url, {}))
        entry.update(provenance.get(url, {}))
        entry.update(local_url=url, size_bytes=path.stat().st_size, sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        entry['file_type'] = path.suffix.lstrip('.').upper()
        entry['content_type'] = mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
        assets.append(entry)
    write('assets', assets)
    return len(assets)

def prepare_thumbnails():
    talks = read('talks')
    jobs = {}
    for item in talks:
        pdf = next((link['local_url'] for link in item['links'] if link.get('asset_type') == 'PDF' and link.get('local_url')), None)
        if not pdf:
            raise ValueError(f"{item['id']}: add a local slide PDF before preparing its thumbnail")
        path = ROOT / 'public' / pdf.lstrip('/')
        digest = hashlib.sha256(path.read_bytes()).hexdigest()[:16]
        url = '/images/talks/' + digest + '.jpg'
        jobs[url] = path
        item['preview_image'] = url
        item['preview_source'] = {'local_url': pdf, 'page': 1}

    missing = [(url, path) for url, path in jobs.items() if not (ROOT / 'public' / url.lstrip('/')).exists()]
    if missing and not shutil.which('pdftoppm'):
        raise ValueError('Install Poppler (pdftoppm) to generate new slide thumbnails. Existing thumbnails build without it.')

    def render(job):
        url, pdf = job
        out = ROOT / 'public' / url.lstrip('/')
        out.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(['pdftoppm', '-f', '1', '-singlefile', '-scale-to', '800', '-jpeg', '-jpegopt', 'quality=82', str(pdf), str(out.with_suffix(''))], check=True, capture_output=True)
        if not out.read_bytes().startswith(b'\xff\xd8'):
            raise ValueError('Invalid thumbnail: ' + str(out))

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(render, missing))
    write('talks', talks)
    return len(missing), len(jobs)
