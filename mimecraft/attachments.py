#!/usr/bin/python

import email.message
import email.mime.nonmultipart
import email.mime.multipart

def attach_parts(parent, parts):
    for p in parts:
        p_type, p_subtype = p['type'].split('/', 1)

        if 'content' in p:
            payload = email.mime.nonmultipart.MIMENonMultipart(
                    p_type,
                    p_subtype)
            payload.set_payload(p['content'])
        elif 'source' in p:
            name = p.get('name', os.path.basename(p['source']))
            id = p.get('id', name)

            payload = email.mime.nonmultipart.MIMENonMultipart(
                    p_type,
                    p_subtype,
                    name=name)

            # If we are building a multipart/related part,
            # assign parts a content-id (for use with the `cid:` url
            # scheme) and `inline` content-disposition.
            if parent['content-type'] == 'multipart/related':
                payload['Content-ID'] = '<%s>' % id
                payload['Content-Disposition'] = 'inline; filename="%s"' % name

            data = open(p['source']).read()

            # Base64 encode non-text attachments.
            if not p_type == 'text':
                data = base64.encodestring(data)
                payload['encoding'] = 'base64'
                payload['Content-Transfer-Encoding'] = 'base64'
            elif p.get('encoding') == 'quoted-printable':
                data = quopri.encodestring(data)
                payload['Content-Transfer-Encoding'] = 'quoted-printable'

            payload.set_payload(data)
        elif 'parts' in p and p_type == 'multipart':
            payload = email.mime.multipart.MIMEMultipart(
                    p_subtype)
            attach_parts(payload, p['parts'])

        parent.attach(payload)

def build_multipart (opts):
    msg = email.message.Message()
    msg.set_type(opts.type)

    for hdr_name, hdr_val in opts.header:
        msg[hdr_name] = hdr_val

    if opts.to_addr:
        msg['To'] = opts.to_addr

    if opts.from_addr:
        msg['From'] = opts.from_addr

    if opts.subject:
        msg['Subject'] = opts.subject

    if opts.cc:
        msg['Cc'] = opts.cc
    
    if opts.parts:
        attach_parts(msg, opts.parts[0]['parts'])

    return msg
