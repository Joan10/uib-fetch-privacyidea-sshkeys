# uib-fetch-privacyidea-sshkeys
## SETUP

Unpack in /opt

```
mkdir /etc/privacyidea
cp authorizedkeyscommand /etc/privacyidea
chmod +x uib-fetch-privacyidea-sshkeys.py
```

Edit sshd_config and add
```
AuthorizedKeysCommand /opt/uib-fetch-privacyidea-sshkeys/uib-fetch-privacyidea-sshkeys.py
```

