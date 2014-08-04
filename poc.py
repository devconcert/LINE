# -*- coding: utf-8 -*-
"""
    poc.py
    ~~~~

    POC code for LINE python library.

    Warning!! This is a quick-and-dirty code!

    Requirements:
        1. Install thirft and python-thirft module
        2. Get a line.thrift code from "https://gist.github.com/ssut/9150461"
        3. thrift -r -gen py line.thrift
        4. python poc.py

    :copyright: (c) 2014 by Taehoon Kim.
    :license: BSD, see LICENSE for more details.
"""

from linethrift import Line
from thrift.transport import TTransport
from thrift.transport import TSocket
from thrift.transport import THttpClient
from thrift.protocol import TCompactProtocol
import time
import pprint
import thrift
import requests
import json
import rsa
import datetime, time


##########################################
# Below is a settings you need to enter!
##########################################

comname  = "" # computer name
user     = "" # LINE email address
password = "" # LINE password
ip       = "" # IP address of your computer


################
# Login part
################

version_string = "3.5.0"
user_agent = "DESKTOP:MAC:10.9.1-MAVERICKS-x64(%s)" % version_string
header_line_application = "DESKTOPMAC\t%s\tMAC\t%s-MAVERICKS-x64" % (version_string, version_string)
url="http://gd2.line.naver.jp/authct/v1/keys/line"
header = {"User-Agent":user_agent, "X-Line-Application": header_line_application}

try:
    f=open('line.cert','r')
    cert = f.read()
    f.close()
except:
    sess = requests.Session()
    r=sess.get(url, headers=header)
    t=r.text
    j=json.loads(t)
    session_key = j['session_key']
    password = chr(len(session_key)) + session_key\
            + chr(len(user)) + user\
            + chr(len(password)) + password
    print "[*] Result : " + password
    rsa_key=j['rsa_key'].split(",")
    keyname=rsa_key[0]
    n=rsa_key[1]
    e=rsa_key[2]
    public_key=rsa.PublicKey(int(n,16),int(e,16))
    cipher=rsa.encrypt(password.encode('utf-8'), public_key).encode('hex')

    uri="http://gd2.line.naver.jp/api/v4/TalkService.do"
    transport = THttpClient.THttpClient(uri)
    print header
    transport.setCustomHeaders(header)
    protocol=TCompactProtocol.TCompactProtocol(transport)

    client=Line.Client(protocol)
    msg=client.loginWithIdentityCredentialForCertificate(user,password.encode('utf-8'),keyname,cipher,False,ip,comname,Line.Provider.LINE, "")
    print msg
    s=raw_input("Finished ?")

    header['X-Line-Access']=msg.verifier
    r=sess.get("http://gd2.line.naver.jp/Q", headers=header)
    t=r.text
    j=json.loads(t)
    print j
    v=j['result']['verifier']

    msg=client.loginWithVerifierForCertificate(v)
    cert=msg.certificate

    f=open('line.cert','w')
    f.write(cert)
    f.close()

print """      ___                   ___           ___
     /\__\      ___        /\__\         /\  \
    /:/  /     /\  \      /::|  |       /::\  \
   /:/  /      \:\  \    /:|:|  |      /:/\:\  \
  /:/  /       /::\__\  /:/|:|  |__   /::\~\:\  \
 /:/__/     __/:/\/__/ /:/ |:| /\__\ /:/\:\ \:\__\\
 \:\  \    /\/:/  /    \/__|:|/:/  / \:\~\:\ \/__/
  \:\  \   \::/__/         |:/:/  /   \:\ \:\__\
   \:\  \   \:\__\         |::/  /     \:\ \/__/
    \:\__\   \/__/         /:/  /       \:\__\
     \/__/                 \/__/         \/__/    """
print
print "                                     by carpedm20"

header['X-Line-Access'] = cert

from cmd import Cmd

class PPrinter(pprint.PrettyPrinter):
    def format(self, _object, context, maxlevels, level):
        if isinstance(_object, unicode):
            return "'%s'" % _object.encode('utf8'), True, False
        elif isinstance(_object, str):
            _object = unicode(_object,'utf8')
            return "'%s'" % _object.encode('utf8'), True, False
        return pprint.PrettyPrinter.format(self, _object, context, maxlevels, level)

class LineCMD(Cmd):
    def __init__(self, header):
        self.transport = THttpClient.THttpClient("http://gd2.line.naver.jp/api/v4/TalkService.do")
        self.transport_in = THttpClient.THttpClient("http://gd2.line.naver.jp/P4")

        self.transport.setCustomHeaders(header)
        self.transport_in.setCustomHeaders(header)

        self.protocol = TCompactProtocol.TCompactProtocol(self.transport)
        self.protocol_in = TCompactProtocol.TCompactProtocol(self.transport_in)

        self.client = Line.Client(self.protocol)
        self.client_in = Line.Client(self.protocol_in)

        self.transport.open()
        self.transport_in.open()

        Cmd.__init__(self)

    def get_name_and_id(self, account):
        return "%s (%s)" % (account.displayName, self.filter_id(account.mid))

    def filter_id(self, id):
        return id[:len(id)/2] + "*"*(len(id)/2)

    def do_groups(self, args):
        """Get group information"""
        groups=prompt.client.getGroups(prompt.client.getGroupIdsJoined())

        gs = []

        for group in groups:
            g = {}
            g['_name'] = group.name
            g['_id'] = group.id
            g['creator'] = self.get_name_and_id(group.creator)
            g['members'] = []
            for member in group.members:
                g['members'].append(self.get_name_and_id(member))

            gs.append(g)

        PPrinter().pprint(gs)

    def do_send(self, args):
        to, text = args.split(",")
        text = text.strip()

        m=Line.Message(to=to,text=text)
        self.client.sendMessage(0, m)

        print "To : %s, MSG :  %s" % (to, text)

    def do_image(self, args):
        to, url= args.split(",")
        url = url.strip()

        m=Line.Message(to=to, text=url)
        m.contentType = Line.ContentType.IMAGE
        m.contentPreview = url
        m.contentMetadata = {"PREVIEW_URL":url,
                             "DOWNLOAD_URL":url,
                             "PUBLIC":"TRUE"}
        self.client.sendMessage(1, m)

        print "To : %s, URL : %s" % (to, url)

    def do_quit(self, args):
        """Quits the program."""
        print "Quitting."
        raise SystemExit


if __name__ == '__main__':
    prompt = LineCMD(header=header)
    prompt.prompt = '> '
    prompt.cmdloop('Starting prompt...')

