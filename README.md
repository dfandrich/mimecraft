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

