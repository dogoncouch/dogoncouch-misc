#/bin/sh

# Run wordlist simulator. arg = seconds, default is 90.

sh -c "chmod +x runfile ; ./wlsim.sh pwfile.txt 192.168.0.48 ; echo ======== ; echo DONE! ; echo ========" &

if [ ${1} ] ; then
    echo ==== Sleeping for ${1} seconds ====
    sleep ${1}
else
    echo ==== Sleeping for 90 seconds ====
    sleep 90
fi

chmod -x runfile
