#!/usr/bin/env python3

""" acme_tiny_renew
renew certs made with github.com/diafygi/acme-tiny
"""

import os, sys, time
import types, json
import subprocess, ssl

CFGFILE = "/etc/acme.json"


def cfg(path):
    with open(path, "r") as infile:
        return types.SimpleNamespace(**json.loads(infile.read()))


def acme_test(retcode, crt, key):
    # check return code
    if retcode != 0:
        sys.exit("# !!! Exit code check failed: " + str(retcode))
    # check cert can load and matches key
    ctx = ssl.create_default_context()
    try:
        ctx.load_cert_chain(crt, key)
    except Exception as err:
        sys.exit("# !!! Sanity testing failed: " + str(err))


def acme_renew(path, date):
    csr = os.path.join(path, "domain.csr")
    crt = os.path.join(path, date + ".cert.crt")
    key = os.path.join(path, "domain.key")
    crtsym = os.path.join(path, "cert.crt")

    print("# Creating new cert for: " + path)
    outfile = open(crt, "w")
    proc = subprocess.Popen(
        [
            "sudo",
            "-u",
            CFG.ACMEUSER,
            "acme_tiny.py",
            "--contact",
            "mailto:" + CFG.MAILADDR,
            "--account-key",
            CFG.ETCDIR + "account.key",
            "--csr",
            csr,
            "--acme-dir",
            CFG.WEBDIR,
        ],
        stdout=outfile,
    )
    proc.wait()

    print("# Checking: " + crt)
    acme_test(proc.returncode, crt, key)
    try:
        os.unlink(crtsym)
    except FileNotFoundError:
        pass
    os.symlink(crt, crtsym)
    print("# Creation complete, symlink changed")

    crtint = crtsym + ".int"
    beginstr = "-----BEGIN CERTIFICATE-----"
    print("# Writing intermediate cert to: " + crtint)
    with open(crtsym, "r") as infile:
        certraw = infile.read()
    certsplit = certraw.split(beginstr)
    assert len(certsplit) == 3
    with open(crtint, "w") as outfile:
        outfile.write(beginstr + certsplit[2])


def main():
    date = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    dirs = [
        f for f in os.listdir(CFG.ETCDIR) if os.path.isdir(os.path.join(CFG.ETCDIR, f))
    ]
    print("##### Found dirs: " + str(dirs))
    for dom in dirs:
        print("### Processing dir: " + dom)
        path = os.path.join(CFG.ETCDIR, dom)
        acme_renew(path, date)


if __name__ == "__main__":
    CFG = cfg(CFGFILE)
    main()
