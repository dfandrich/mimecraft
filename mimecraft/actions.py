#!/usr/bin/python

import os
import argparse

class MIMEAction (argparse.Action):
    '''This is the base class for other argparse actions.  It ensures that
    the namespace has been initialized.'''
    def __call__(self, parser, namespace, values, option_string=None):
        if not namespace.parts:
            namespace.parts = [
                    { 'type': namespace.type, 'parts': []}
                    ]

            setattr(namespace, 'acc', [namespace.parts[0]])

class BeginAction (MIMEAction):
    '''Implements the --begin option.  Starts a new multipart attachment by
    appending a dictionary to namespace.acc.'''
    def __call__(self, parser, namespace, values, option_string=None):
        super(BeginAction, self).__call__(parser, namespace, values, option_string)

        if '/' in values:
            contenttype = values
        else:
            contenttype = 'multipart/%s' % values

        namespace.acc.append({'type': contenttype, 'parts': []})

class EndAction (MIMEAction):
    '''Implements the --end option.  Pops the current attachment from
    namespace.acc and appends it to namespace.parts.'''
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

class QuotedPrintableAction (MIMEAction):
    def __call__(self, parser, namespace, values, option_string=None):
        super(QuotedPrintableAction, self).__call__(parser, namespace, values, option_string)

        try:
            current = namespace.acc[-1]
            current['parts'][-1]['encoding'] = 'quoted-printable'
        except (AttributeError, IndexError):
            raise argparse.ArgumentError(self, 'no attachment for %s' % option_string)

class NameAction (MIMEAction):
    def __call__(self, parser, namespace, values, option_string=None):
        super(NameAction, self).__call__(parser, namespace, values, option_string)

        try:
            current = namespace.acc[-1]
            current['parts'][-1]['name'] = values
        except (AttributeError, IndexError):
            raise argparse.ArgumentError(self, 'no attachment for %s' % option_string)

class IdAction (MIMEAction):
    def __call__(self, parser, namespace, values, option_string=None):
        super(IdAction, self).__call__(parser, namespace, values, option_string)

        try:
            current = namespace.acc[-1]
            current['parts'][-1]['id'] = values
        except (AttributeError, IndexError):
            raise argparse.ArgumentError(self, 'no attachment for %s' % option_string)

