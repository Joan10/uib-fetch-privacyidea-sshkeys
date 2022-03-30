# uib-fetch-privacyidea-sshkeys
## SETUP

Install prerequisites

```
apt-get install python3 python3-pip
pip3 install requests
```

Unpack in /opt

```
mkdir /etc/privacyidea
cp authorizedkeyscommand /etc/privacyidea
chmod +x uib-fetch-privacyidea-sshkeys.py
```

Edit sshd_config and add
```
AuthorizedKeysCommand /opt/uib-fetch-privacyidea-sshkeys/uib-fetch-privacyidea-sshkeys.py
AuthorizedKeysCommandUser nobody
```

