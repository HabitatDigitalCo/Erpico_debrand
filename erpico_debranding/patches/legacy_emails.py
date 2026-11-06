# © 2026 Habitat Digital
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

import re

from lxml import etree

from odoo import tools

_POWERED_RE = re.compile(r'Powered by <a[^>]*>Odoo</a>')
_TOUR_RE = re.compile(r'<a[^>]*>Odoo Tour</a>')
_MARKETING_RE = re.compile(
    r'Never heard of Odoo\?.*?increase your productivity\.\s*',
    flags=re.S,
)

_REPLACEMENTS = (
    ('invites you to connect to Odoo', 'invites you to connect to ERPICO'),
    ('Welcome to Odoo', 'Welcome to ERPICO'),
    ('>OdooBot</t>', '>Your administrator</t>'),
    ('to connect on Odoo.', 'to connect on ERPICO.'),
    ('Your Odoo domain is:', 'Your domain is:'),
    ('>http://yourcompany.odoo.com</a>', '>http://yourcompany.example.com</a>'),
    ('Enjoy Odoo!', 'Enjoy ERPICO!'),
)

LEGACY_EMAIL_XMLIDS = (
    'auth_signup.set_password_email',
    'auth_signup.portal_set_password_email',
    'auth_signup.mail_template_data_unregistered_users',
    'auth_signup.mail_template_user_signup_account_created',
)


def _clean(html):
    html = str(html)  # bypass markupsafe.Markup.replace quirk
    for old, new in _REPLACEMENTS:
        html = html.replace(old, new)
    html = _MARKETING_RE.sub('', html)
    html = _TOUR_RE.sub('ERPICO guide', html)
    return _POWERED_RE.sub('Powered by <b>ERPICO</b>', html)


def patch_legacy_emails(env):
    """Update only stock English templates; leave custom templates untouched."""
    patched = []
    with tools.file_open('auth_signup/data/mail_template_data.xml', 'rb') as source:
        templates = etree.parse(source)
    for xmlid in LEGACY_EMAIL_XMLIDS:
        rec = env.ref(xmlid, raise_if_not_found=False)
        if not rec:
            continue
        rec = rec.with_context(lang='en_US')
        record_nodes = templates.xpath('//record[@id=$name]', name=xmlid.split('.')[1])
        if not record_nodes:
            continue
        record = record_nodes[0]
        values = {}
        body_nodes = record.xpath('./field[@name="body_html"]')
        if body_nodes and rec.body_html:
            raw = ''.join(
                etree.tostring(node, method='html', encoding='unicode')
                for node in body_nodes[0]
            )
            stock_body = str(rec._fields['body_html'].convert_to_cache(raw, rec))
            current_body = str(rec.body_html)
            if current_body == stock_body:
                cleaned = _clean(stock_body)
                if cleaned != current_body:
                    values['body_html'] = cleaned
        subject_nodes = record.xpath('./field[@name="subject"]')
        if subject_nodes and rec.subject == (subject_nodes[0].text or ''):
            subject = rec.subject.replace('invites you to connect to Odoo',
                                          'invites you to connect to ERPICO')
            if subject != rec.subject:
                values['subject'] = subject
        if values:
            rec.write(values)
            patched.append(xmlid)
    return patched
