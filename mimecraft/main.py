#!/usr/bin/python

import os
import sys
import argparse
import email.message
import email.mime.nonmultipart
import email.mime.multipart
import email.generator
import base64
import quopri

from actions import *

def parse_args():
    p = argparse.ArgumentParser()

    p.add_argument('--type', '-c',
            default='multipart/mixed')
    p.add_argument('--to', '-t', dest='to_addr',
            default=os.environ['LOGNAME'])
    p.add_argument('--from', '-f', dest='from_addr',
            default=os.environ['LOGNAME'])
    p.add_argument('--subject', '-s')
    p.add_argument('--cc')
    p.add_argument('--header', '-H',
            action='append',
            default=[],
            nargs=2,
            metavar=('HEADER_NAME', 'HEADER_VALUE'),
            help='Set an arbitrary message header')

    g = p.add_argument_group('attachment options')
    g.add_argument('--begin', '-b', action=BeginAction,
            dest=None,
            metavar='CONTENT-TYPE',
            help='Begin a multipart sub-part')
    g.add_argument('--attach', '-a', action=AttachAction,
            nargs=2,
            dest=None,
            metavar=('CONTENT-TYPE', 'FILE'),
            help='Attach a file')
    g.add_argument('--attach-literal', '-l',
            action=AttachLiteralAction, nargs=2,
            dest=None,
            metavar=('CONTENT-TYPE', 'CONTENTS'),
            help='Create an attachment with literal content')
    g.add_argument('--quoted-printable', '--qp',
            nargs=0,
            action=QuotedPrintableAction,
            dest=None,
            help='Use quoted-printable encoding on the preceding attachment')
    g.add_argument('--name', action=NameAction, dest=None,
            help='Set the filename of the preceding attachment')
    g.add_argument('--id', action=IdAction, dest=None,
            help='Set the content-id of the preceding attachment')
    g.add_argument('--end', '-e', action=EndAction, 
            dest=None,
            nargs=0,
            help='Close a multipart sub-part')

    p.add_argument('--debug', '-D', action='store_true')

    p.set_defaults(parts=None)

    return p.parse_args()

def attach_parts(msg, parts):
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
            if msg['content-type'] == 'multipart/related':
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

        msg.attach(payload)

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

def main():
    import pprint
    opts = parse_args()

    if not '/' in opts.type:
        opts.type = 'multipart/%s' % opts.type

    if opts.debug:
        pprint.pprint(opts.parts)
        sys.exit()

    msg = build_multipart(opts)
    g = email.generator.Generator(sys.stdout, mangle_from_=False)
    g.flatten(msg)
    
if __name__ == '__main__':
    main()

