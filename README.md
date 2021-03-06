MIMECraft
=========

MIMECraft is a tool for crafting complex MIME messages from the command line.

Description
-----------

<img src="https://raw.github.com/larsks/mimecraft/master/mimecraft.png" width="200" style="float: left" />

There are many tools for extracting the contents of a MIME-encoded
message, but there are comparatively few command-line tools that exist
for *generating* such messages.  While tools like [smtp-cli][], for
example, are quite capable, they are still limited in the structure
they can produce.

MIMECraft makes it easy to produce a `multipart/alternative` message
with a `text/plain` part, a `text/rtf` part, and a `multipart/related`
sub-part containing a `text/html` document and one or more images.

[smtp-cli]: http://www.logix.cz/michal/devel/smtp-cli/

Synopsis
--------

    usage: mimecraft [-h] [--type TYPE] [--to TO_ADDR] [--from FROM_ADDR]
                     [--subject SUBJECT] [--cc CC]
                     [--header HEADER_NAME HEADER_VALUE] [--begin CONTENT-TYPE]
                     [--attach CONTENT-TYPE FILE]
                     [--attach-literal CONTENT-TYPE CONTENTS] [--quoted-printable]
                     [--name NAME] [--id ID] [--end] [--debug]

Options
-------

### Message options

- `--type` *content-type*, `-c` *content-type*
  
    Sets the subtype of the message.  This will typically be
    `alternative`, `mixed`, or `related`, but `chartreuse` is also
    acceptable.

- `--to` *address*, `-t` *address*

    Sets the `To:` header of the message.

- `--cc` *address*

    Sets the `Cc:` header of the message.

- `--from` *address*, `-f` *address*

    Sets the `From:` header of the message.

- `--subject` *subject*, `-s` *subject*

    Sets the `Subject:` of the message.

- `--header` *header_name* *header_value*, `-H` *header_name*
  *header_value*

    Sets an arbitrary header in the message.

### Attachment options

- `--attach` *content-type* *file*, `-a` *content-type* *file*

    Attach a file using the specified content-type.  Non-`text/*`
    attachments will be base64 encoded.

- `--attach-literal` *content-type* *string*, `-l` *content-type* *string*

    Attach a literal string of the specified content-type.  Non-`text/*`
    attachments will be base64 encoded.

- `--quoted-printable`, `--qp`

    The immeditely preceding attachment will be encoded using
    *quoted-printable* encoding.

- `--name` *string*

    Sets the attachment filename.  Defaults to the basename of the
    source file.

- `--id` *string*

    Sets the `Content-ID` for the attachment.  If unspecified this
    defaults to the filename.

- `--begin` *subtype*, `-b` *subtype*

    Begin a new `multipart/*` sub-part.

- `--end`, `-e`

    End a mutipart sub-part.

Example
-------

### A simple example

This command:

    $ mimecraft -c alternative \
      -l text/plain "This is a plain part" \
      -l text/x-markdown "*This* is a **Markdown** part" \
      -l text/html "<em>This</em> is a <strong>HTML</strong> part."

Would generate the following output:

    MIME-Version: 1.0
    Content-Type: multipart/alternative;
     boundary="===============5796968212609317359=="
    To: lars
    From: lars

    --===============5796968212609317359==
    Content-Type: text/plain
    MIME-Version: 1.0

    This is a plain part
    --===============5796968212609317359==
    Content-Type: text/x-markdown
    MIME-Version: 1.0

    *This* is a **Markdown** part
    --===============5796968212609317359==
    Content-Type: text/html
    MIME-Version: 1.0

    <em>This</em> is a <strong>HTML</strong> part.
    --===============5796968212609317359==--

### A more complex example

To generate a three-part `multipart/alternative` message,
with one `text/plain` part, one `text/x-markdown` part, and finally a
`text/html` part and `image/png` contained in a `multipart/related`
sub-part:

    mimecraft \
      --to lars@oddbit.com \
      --from lars@oddbit.com \
      --subject "MIME TEST" \
      --attach text/plain README.txt \
      --attach text/x-markdown README.md \
      --begin related \
        --attach text/html README.html \
        --attach image/png mimecraft.png \
      --end

Within the `text/html` part, you could link to the logo using
`src="cid:mimecraft.png"` in your image links.

License
-------

MIMECraft, a tool for generating MIME email.  
Copyright (C) 2012 Lars Kellogg-Stedman

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

