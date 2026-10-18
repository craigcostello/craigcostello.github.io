"""Shared cards for homepage highlights and searchable archives."""

def render_card(item, kind, *, a, e, img, target, branding, archive=False):
    attrs = ' id="' + e(item['id']) + '"' if archive else ''
    entry = ' entry' if archive else ''
    url = item.get('canonical_url') or target(item['links'][0])

    def image(path, alt='', cls=''):
        return '<img src="' + img(path) + '" alt="' + e(alt) + '" class="' + cls + '" loading="lazy">'

    if kind == 'print':
        logo = branding.get(item.get('logo_key'), {})
        if logo.get('available'):
            visual = image(logo['local_url'], '', 'publisher-' + item['logo_key'])
        else:
            visual = image(item['local_image'])
        meta = item['outlet'] + (' · ' + str(item['year']) if item.get('year') else '')
        return ('<article class="press-item' + entry + '"' + attrs + '><a class="press-logo" href="' + e(url)
                + '" aria-label="' + e(item['outlet'] + ': ' + item['title']) + '">' + visual
                + '</a><div><h3>' + a(url, item['title']) + '</h3><p>' + e(meta) + '</p></div></article>')

    if kind == 'talks':
        visual = image(item['preview_image'], 'Opening slide: ' + item['title'], 'document-slide')
        label, meta = 'Slides · PDF', item['detail']
    else:
        visual = image(item['local_image'], '', 'podcast-art' if item.get('image_fit') == 'contain' else '')
        label = 'Watch on TED' if item.get('canonical_url', '').startswith('https://www.ted.com/') else {'podcast': 'Watch / listen', 'radio': 'Listen', 'video': 'Watch'}[item['format']]
        meta = item['outlet'] + (' · ' + str(item['year']) if item.get('year') else '')
    out = ('<article class="tile' + entry + '"' + attrs + '><a class="tile-visual" href="' + e(url)
           + '" aria-label="' + e(label + ': ' + item['title']) + '">' + visual + '<span class="tile-label">'
           + label + '</span></a><p class="tile-meta">' + e(meta) + '</p><h3>' + a(url, item['title']) + '</h3>')
    if item.get('display_stat'):
        out += '<div class="tile-stat" title="Checked ' + e(item['stat_checked']) + '">' + e(item['display_stat']) + '</div>'
    extras = item['links'][1:] if kind == 'talks' else [l for l in item['links'] if l['text'] in ['Apple', 'Spotify', 'Audible', 'Amazon']]
    if extras:
        out += '<div class="tile-links">' + ''.join(a(target(l), l['text']) for l in extras) + '</div>'
    return out + '</article>'
