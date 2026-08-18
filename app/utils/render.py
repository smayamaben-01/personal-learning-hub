import markdown
import bleach

ALLOWED_TAGS = ['p', 'em', 'strong', 'ul', 'ol', 'li', 'pre', 'code', 'h1', 'h2', 'h3', 'a']

def render_note_content(raw_content):
    html = markdown.markdown(raw_content, extensions=['fenced_code'])
    safe_html = bleach.clean(html, tags=ALLOWED_TAGS, strip=True)
    return safe_html