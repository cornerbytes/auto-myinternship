# auto-myintership

## how to run this script
here we go again....

- `git clone https://github.com/cornerbytes/auto-myinternship.git`
- `pip install requests` I am trying to make this script as minimal as possible without requiring any additional installations.
- replace images/ttd.png with your signature
- update conf.py
- and then `python3 myintern.py`
- if you want to run this script automatically on linux server do this `(crontab -l; echo "30 00 * * * cd /path/to/auto-myinternship && /usr/bin/python3 myintern.py") | crontab -`


## future work
- using bash script instead of python
