#!/usr/bin/env python3
"""Guided content additions. No Python packages or network required."""
import argparse
import hashlib
import pathlib
import re
import shutil
import subprocess
import sys
from assets import ROOT, read, write, refresh_manifest, prepare_thumbnails

KINDS = {'paper': 'papers', 'talk': 'talks', 'media': 'media'}

def import_asset(source, folder, suffixes):
    path = pathlib.Path(source).expanduser().resolve()
    if not path.is_file() or path.suffix.lower() not in suffixes:
        raise ValueError('Expected an existing ' + ', '.join(suffixes) + ' file: ' + str(path))
    data = path.read_bytes()
    if suffixes == {'.pdf'} and not data.startswith(b'%PDF-'):
        raise ValueError('The slides file is not a PDF')
    name = re.sub(r'[^A-Za-z0-9._-]', '-', path.stem).strip('.-') or 'asset'
    url = '/' + folder + '/' + name + '-' + hashlib.sha256(data).hexdigest()[:8] + path.suffix.lower()
    dest = ROOT / 'public' / url.lstrip('/')
    dest.parent.mkdir(parents=True, exist_ok=True)
    if path != dest:
        shutil.copyfile(path, dest)
    return url

def add(args):
    collection = KINDS[args.kind]
    items = read(collection)
    if args.from_json:
        import json
        item = json.loads(pathlib.Path(args.from_json).read_text())
        if not isinstance(item, dict):
            raise ValueError('Entry JSON must be one object')
    else:
        item = {'title': input('Title: ').strip()}
        item['detail'] = input('Authors and venue (paper), event and date (talk), or outlet (media): ').strip()
        item['year'] = input('Year (blank if unknown): ').strip() or None
        url = input('Original URL (blank for a new local slide deck): ').strip()
        item['links'] = [{'text': item['title'], 'original_url': url}] if url else []
        if args.kind == 'media':
            item['format'] = input('Format [article / podcast / radio / video]: ').strip()
            item['outlet'] = item['detail']
    if not item.get('title') or not item.get('detail'):
        raise ValueError('Title and detail are required')
    if args.kind == 'media':
        if item.get('format') not in ['article', 'podcast', 'radio', 'video']:
            raise ValueError('Media format must be article, podcast, radio or video')
        item['category'] = 'print' if item['format'] == 'article' else 'watch'
        item.setdefault('outlet', item['detail'])
        if args.image:
            item['local_image'] = import_asset(args.image, 'images/media', {'.jpg', '.jpeg', '.png', '.webp', '.svg'})
        if not item.get('local_image') and not item.get('logo_key'):
            raise ValueError('Supply --image FILE or a local_image / logo_key in the entry JSON')
    if args.kind == 'talk' and args.slides:
        local = import_asset(args.slides, 'slides', {'.pdf'})
        links = item.setdefault('links', [])
        if links:
            links[0].update(local_url=local, asset_type='PDF')
        else:
            links.append({'text': 'Slides', 'original_url': local, 'local_url': local, 'asset_type': 'PDF'})
    links = item.get('links', [])
    if not links or any(not l.get('text') or not l.get('original_url', '').startswith(('https://', 'http://', '/')) for l in links):
        raise ValueError('Provide links with text and an http(s) original_url (or a local slide deck)')
    if args.kind == 'talk' and not any(l.get('local_url') and l.get('asset_type') == 'PDF' for l in links):
        raise ValueError('Supply --slides FILE or a local PDF link in the entry JSON')
    next_number = max([int(x['id'].split('-')[-1]) for x in items if re.fullmatch(collection + r'-\d+', x['id'])] or [0]) + 1
    item.setdefault('id', f'{collection}-{next_number:03d}')
    if any(x['id'] == item['id'] for x in items):
        raise ValueError('Duplicate ID: ' + item['id'])
    items.insert(0, item)  # Editorial order; no sorting by inferred dates.
    original_content = (ROOT / 'content' / (collection + '.json')).read_bytes()
    write(collection, items)
    try:
        if args.kind == 'talk':
            prepare_thumbnails()
    except (ValueError, OSError, subprocess.CalledProcessError):
        # An unreadable PDF must not leave a half-added catalogue entry.
        (ROOT / 'content' / (collection + '.json')).write_bytes(original_content)
        raise
    if args.feature:
        if args.kind != 'media':
            print('Papers and talks feature the first items automatically.')
        else:
            config = read('site')
            key = 'featured_' + item['category']
            config[key] = [item['id']] + config[key]
            write('site', config)
    refresh_manifest()
    print('Added ' + item['id'] + '. Run python3 build.py && python3 check.py, then review and commit.')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    create = commands.add_parser('add', help='Add a paper, talk or media item at the top of its archive')
    create.add_argument('kind', choices=KINDS)
    create.add_argument('--from-json', help='Use an entry object instead of the guided questions')
    create.add_argument('--slides', help='Copy a talk PDF and generate its opening-slide thumbnail')
    create.add_argument('--image', help='Copy a media thumbnail image')
    create.add_argument('--feature', action='store_true', help='Also add media to homepage highlights')
    commands.add_parser('thumbnails', help='Generate missing opening-slide thumbnails from local PDFs')
    commands.add_parser('assets', help='Refresh size and SHA-256 records after changing local assets')
    args = parser.parse_args()
    try:
        if args.command == 'add':
            before = {path: path.read_bytes() for path in (ROOT / 'content').glob('*.json')}
            assets_before = {path for path in (ROOT / 'public').rglob('*') if path.is_file()}
            try:
                add(args)
            except (ValueError, OSError, subprocess.CalledProcessError):
                for path, data in before.items():
                    path.write_bytes(data)
                for path in (ROOT / 'public').rglob('*'):
                    if path.is_file() and path not in assets_before:
                        path.unlink()
                raise
        elif args.command == 'thumbnails':
            created, total = prepare_thumbnails()
            print(f'Created {created} thumbnails; {total} distinct slide decks covered.')
            refresh_manifest()
        else:
            print(f'Updated {refresh_manifest()} public asset records.')
    except subprocess.CalledProcessError as error:
        detail = error.stderr.decode(errors='replace') if isinstance(error.stderr, bytes) else str(error.stderr or '')
        sys.exit('Slide preview could not be generated; entry was not added. ' + detail[-500:])
    except (ValueError, OSError) as error:
        sys.exit(str(error))

if __name__ == '__main__':
    main()
