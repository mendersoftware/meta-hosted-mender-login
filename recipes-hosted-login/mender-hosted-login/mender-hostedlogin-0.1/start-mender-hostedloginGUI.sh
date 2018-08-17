#!/bin/sh
#

if grep -q TenantToken.*dummy /etc/mender/mender.conf; then
    export DISPLAY=:0
    export QT_QPA_FONTDIR=/usr/share/fonts/ttf
    /usr/bin/python /etc/mender/login/menderLogin.py
fi
