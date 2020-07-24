================
acme_tiny_renew
================

description
============

acme_tiny_renew automates the renewal of certs made with acme_tiny_

installation
=============

works with Ubuntu 14.04 (py3.4) / 18.04 (py3.6)

no dependencies are required, only the python stdlib

usage
======

place config in /etc/acme.json

run acme_tiny_renew once to initialise the cert

to automate renewal, place an entry in the crontab, followed by a webserver reload, e.g:
"0 0 1 * * /usr/local/bin/acme_tiny_renew.py && service apache2 reload"

internals
==========

acme_tiny_renew:
* takes a dir, finds all subdirs
* finds the CSR for each subdir
* renews them with acme_tiny, writing out a datestamped cert
* sanity checks the renewed cert
* updates a symlink to the new cert (cert.crt)
* copies the intermediate cert to a separate file (cert.crt.int)



.. _acme_tiny: https://github.com/diafygi/acme-tiny/
