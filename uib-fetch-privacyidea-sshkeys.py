#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#  privacyIDEA
#  2022-03-29 Joan Arbona <joan.arbona@uib.es>
#             Adapted and simplified this script using request library
#  2018-03-16 Cornelius Kölbel <cornelius.koelbel@nektnights.it>
#             Dario Salerno <info@dariosalerno.com>
#             Make nosslcheck and hostname optional
#  2015-03-05 Cornelius Kölbel, <cornelius@privacyidea.org>
#             Adapt authitems to new version 2.1
#
#  (c) 2014-2015 Cornelius Kölbel, cornelius@privacyidea.org
#
# This code is free software; you can redistribute it and/or
# modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
# License as published by the Free Software Foundation; either
# version 3 of the License, or any later version.
#
# This code is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU AFFERO GENERAL PUBLIC LICENSE for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
This tool is used to fetch the ssh public keys for 
the given user on this machine. 

This tool is to be used with the sshd_config entry

 AuthorizedKeysCommand
 
Run this script as the user specified in

 AuthorizedKeysCommandUser.
 
The settings, where the privacyIDEA server is located and which
realm is used, is located in the file
/etc/privacyidea/authorizedkeyscommand.

You need to create the following section:

   [Default]
   url = https://privacyidea
   admin = admin
   password = secret
   # nosslcheck = False
   # hostname = <hostname>   

"""
from __future__ import print_function
import argparse
import socket
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import sys
import traceback
import requests

VERSION = '1.0.0'
DEBUG = False
DESCRIPTION = __doc__
DEFAULT_CONFIG = "/etc/privacyidea/authorizedkeyscommand"


def create_arguments():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("user",
                        help="The username of the user who is trying"
                        "to authenticate")
    parser.add_argument("-v", "--version",
                        help="Print the version of the program.",
                        action='version', version='%(prog)s ' + VERSION)
    parser.add_argument("--nosslcheck",
                        help="Do not check SSL certificates.",
                        action="store_true")
    args = parser.parse_args()
    return args


def main():
    args = create_arguments()
    # Mandatory Settings
    try:
        config = configparser.RawConfigParser()
        config.read(DEFAULT_CONFIG)
        url = config.get("Default", "url")
        admin = config.get("Default", "admin")
        password = config.get("Default", "password")

    except Exception as ex:
        print("You need to provide the config file!")
        print(ex)
        sys.exit(1)

    # Optional Settings
    try:
        nosslcheck = config.get("Default", "nosslcheck")
    except configparser.NoOptionError:
        nosslcheck = False
    
    try:
        hostname = config.get("Default", "hostname")
    except configparser.NoOptionError:
        hostname = socket.gethostname()

    # Auth and get token
    x = requests.post(url+"/auth",data={"username":admin,"password":password},verify=not(bool(nosslcheck)))
    token = x.json()['result']['value']['token']
    params = {"hostname": hostname, "user": args.user}
    # Get ssh keys for host
    response = requests.get(url+"/machine/authitem/ssh", params=params, headers={"PI-Authorization":token},verify=not(bool(nosslcheck)))
    result = response.json()["result"]
    if result["status"]:
        value = result["value"]
        ssh_key_list = value["ssh"]
        for sshkey in ssh_key_list:
            if sshkey["user"]:
                user = sshkey["user"]
            else:
                user = "root"
            key = sshkey["sshkey"]
            # print all keys for the requested user
            if user == args.user:
                print("%s" % key)
    else:
        print("error fetching list")


if __name__ == '__main__':
    if DEBUG:
        main()
    else:
        try:
            main()
        except Exception as ex:
            print("%s" % traceback.format_exc())
            print("Error: %s" % ex)
            sys.exit(5)
