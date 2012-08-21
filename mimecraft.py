#!/usr/bin/python

import os
import sys
import argparse
import email.message
import email.mime.nonmultipart
import email.mime.multipart
import base64

class MIMEAction (argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not namespace.parts:
            namespace.parts = [
                    { 'type': namespace.type, 'parts': []}
                    ]

            setattr(namespace, 'acc', [namespace.parts[0]])

class BeginAction (MIMEAction):
    def __call__(self, parser, namespace, values, option_string=None):
        super(BeginAction, self).__call__(parser, namespace, values, option_string)

        if '/' in values:
            contenttype = values
        else:
            contenttype = 'multipart/%s' % values

        namespace.acc.append({'type': contenttype, 'parts': []})

class EndAction (MIMEAction):
    def __call__(self, parser, namespace, values, option_string=None):
        super(EndAction, self).__call__(parser, namespace, values, option_string)

        try:
            current = namespace.acc.pop()
        except (AttributeError, IndexError):
            raise argparse.ArgumentError(self, '--end without --begin')

        if namespace.acc:
            namespace.acc[-1]['parts'].append(current)
        else:
            namespace.parts.append(current)

class AttachAction (MIMEAction):
    def __call__(self, parser, namespace, values, option_string=None):
        super(AttachAction, self).__call__(parser, namespace, values, option_string)

        try:
            current = namespace.acc[-1]
        except (AttributeError, IndexError):
            raise argparse.ArgumentError(self, '--attach without --begin')

        current['parts'].append({
            'type': values[0], 'source': values[1],
            })

class AttachLiteralAction (MIMEAction):
    def __call__(self, parser, namespace, values, option_string=None):
        super(AttachLiteralAction, self).__call__(parser, namespace, values, option_string)

        try:
            current = namespace.acc[-1]
        except (AttributeError, IndexError):
            raise argparse.ArgumentError(self, '--attach without --begin')

        current['parts'].append({
            'type': values[0],
            'content': values[1],
            })

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

    g = p.add_argument_group('attachment options')
    g.add_argument('--begin', '-b', action=BeginAction,
            dest='parts',
            metavar='CONTENT-TYPE')
    g.add_argument('--attach', '-a', action=AttachAction,
            nargs=2,
            dest='parts',
            metavar=('TYPE', 'FILE'))
    g.add_argument('--attach-literal', '-l',
            action=AttachLiteralAction, nargs=2,
            dest='parts')
    g.add_argument('--end', '-e', action=EndAction, 
            dest='parts',
            nargs=0)

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
            name = os.path.basename(p['source'])

            payload = email.mime.nonmultipart.MIMENonMultipart(
                    p_type,
                    p_subtype,
                    name=name)

            if msg['content-type'] == 'multipart/related':
                payload['Content-ID'] = '<%s>' % name
                payload['Content-Disposition'] = 'inline; filename="%s"' % name

            data = open(p['source']).read()

            if not p_type == 'text':
                data = base64.encodestring(data)
                payload['Content-Transfer-Encoding'] = 'base64'

            payload.set_payload(data)
        elif 'parts' in p and p_type == 'multipart':
            payload = email.mime.multipart.MIMEMultipart(
                    p_subtype)
            attach_parts(payload, p['parts'])

        msg.attach(payload)

def build_multipart (opts):
    msg = email.message.Message()
    msg.set_type(opts.type)

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

    msg = build_multipart(opts)
    print msg
    
if __name__ == '__main__':
    main()

