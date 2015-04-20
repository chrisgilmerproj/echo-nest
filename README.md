Echo + Nest
===

This is a project inspired primarily by the project:

https://github.com/ghballiet/echo-api

I've strung together similar code in python using available
code.  Simply rename `secrets-template.py` to `secrets.py`,
fill it with your credentials and run the code:

```sh
$ python app.py
```

Installation
---

```sh
$ virtualenv env
$ source env/bin/activate
(env) $ pip install -r requirements.txt
```

Wolfram Alpha Key
---

[Get key here](https://developer.wolframalpha.com/portal/apisignup.html]


FreeBSD Setup
---

I've set this up on my FreeNAS box at home.  To do this you have to first
install a jail from the GUI.  After doing that follow these steps:

```
# jls
# jls exec /bin/tcsh
echo # pkg install bash
echo # pkg install screen
echo # pkg install python
echo # pkg install py27-pip
echo # pkg install py27-virtualenv
echo # mkdir /srv
echo # cd /srv
echo # git clone https://github.com/chrisgilmerproj/echo-api.git
echo # Ctrl + d
# jls exec /usr/local/bin/bash
echo $ cd /srv/echo-nest
echo $ virtualenv env
echo $ source env/bin/activate
(env) echo $ pip install -r requirements.txt
(env) echo $ screen
$ source env/bin/activate
(env) $ python app.py
(env) $ Ctrl + a + d
```
