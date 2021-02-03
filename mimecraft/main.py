import os
import sys
import argparse
import email.generator

from mimecraft import actions
from mimecraft import attachments


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
    g.add_argument('--begin', '-b', action=actions.BeginAction,
                   dest=None,
                   metavar='CONTENT-TYPE',
                   help='Begin a multipart sub-part')
    g.add_argument('--attach', '-a', action=actions.AttachAction,
                   nargs=2,
                   dest=None,
                   metavar=('CONTENT-TYPE', 'FILE'),
                   help='Attach a file')
    g.add_argument('--attach-literal', '-l',
                   action=actions.AttachLiteralAction, nargs=2,
                   dest=None,
                   metavar=('CONTENT-TYPE', 'CONTENTS'),
                   help='Create an attachment with literal content')
    g.add_argument('--quoted-printable', '--qp',
                   nargs=0,
                   action=actions.QuotedPrintableAction,
                   dest=None,
                   help='Use quoted-printable encoding on the preceding attachment')
    g.add_argument('--name', action=actions.NameAction, dest=None,
                   help='Set the filename of the preceding attachment')
    g.add_argument('--id', action=actions.IdAction, dest=None,
                   help='Set the content-id of the preceding attachment')
    g.add_argument('--end', '-e', action=actions.EndAction,
                   dest=None,
                   nargs=0,
                   help='Close a multipart sub-part')

    p.add_argument('--debug', '-D', action='store_true')

    p.set_defaults(parts=None)

    return p.parse_args()


def main():
    import pprint
    opts = parse_args()

    if '/' not in opts.type:
        opts.type = 'multipart/%s' % opts.type

    if opts.debug:
        pprint.pprint(opts.parts)
        sys.exit()

    msg = attachments.build_multipart(opts)
    g = email.generator.Generator(sys.stdout, mangle_from_=False)
    g.flatten(msg)


if __name__ == '__main__':
    main()
