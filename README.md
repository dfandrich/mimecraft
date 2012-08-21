![MIMECraft][logo]

MIMECraft
=========

MIMECraft is a tool for crafting complex MIME messages from the command line.

Usage
-----

    usage: mimecraft.py [-h] [--type TYPE] [--to TO_ADDR] [--from FROM_ADDR]
                        [--subject SUBJECT] [--cc CC] [--begin CONTENT-TYPE]
                        [--attach TYPE FILE] [--attach-literal PARTS PARTS]
                        [--end]

    optional arguments:
      -h, --help            show this help message and exit
      --type TYPE, -c TYPE
      --to TO_ADDR, -t TO_ADDR
      --from FROM_ADDR, -f FROM_ADDR
      --subject SUBJECT, -s SUBJECT
      --cc CC

    attachment options:
      --begin CONTENT-TYPE, -b CONTENT-TYPE
      --attach TYPE FILE, -a TYPE FILE
      --attach-literal PARTS PARTS, -l PARTS PARTS
      --end, -e

[logo]: cid:mimecraft.png

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

