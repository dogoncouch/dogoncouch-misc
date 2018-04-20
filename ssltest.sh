#!/bin/bash

# MIT License
# 
# Copyright (c) 2018 Dan Persons (dpersonsdev@gmail.com)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

VERSION="0.1"

usage() {
    echo "Usage: ${0##*/} [-hv] HOST"
    echo "  -h                  Print this help message"
    echo "  -v                  Print the version number"
    echo "  -i                  Accept untrusted certificates"
    echo "  -o 'CURLOPTS'       Set additional options for curl"
    echo "  -c CERTFILE         Set a CA certificate for verification"
}

CURLCMD="curl -s"

while getopts ":vhio:c:" o; do
    case "${o}" in
        v)
            echo putkey-$VERSION
            exit 0
            ;;
        h)
            usage
            exit 0
            ;;
        i)
            CURLCMD="${CURLCMD} -k"
            ;;
        o)
            CURLCMD="${CURLCMD} ${OPTARG}"
            ;;
        c)
            CERTFILE="${OPTARG}"
            CURLCMD="${CURLCMD} --cacert ${CERTFILE}"
            ;;
        *)
            usage
            exit 1
            ;;
    esac
done
shift $((OPTIND-1))

TARGETHOST="${1}"

# Check for color terminal:
if [ "$(tput colors)" -ge 256 ]; then
    DEFAULTCOLOR="\e[39m"
    REDCOLOR="\e[91m"
    GREENCOLOR="\e[92m"
    YELLOWCOLOR="\e[93m"
else
    DEFAULTCOLOR=""
    REDCOLOR=""
    GREENCOLOR=""
    YELLOWCOLOR=""
fi


checksslconf() {
    echo
    echo "=== Web server info for ${TARGETHOST} ==="
    echo
    ${CURLCMD} -I "https://${TARGETHOST}" | grep "^Server: "

    # Checking for HTTPS only
    echo
    HTTPMOVED=$(${CURLCMD} -I "http://${TARGETHOST}" | grep "^HTTP" | grep "301 Moved Permanently")
    HTTPFOUND=$(${CURLCMD} -I "http://${TARGETHOST}" | grep "^HTTP" | grep "302 Found")
    if [ -n "$HTTPMOVED" ]; then
        echo -e "[${GREENCOLOR}...${DEFAULTCOLOR}] HTTP redirects."
    elif [ -n "$HTTPFOUND" ]; then
        echo -e "[${REDCOLOR}!!!${DEFAULTCOLOR}] Unsecured HTTP is enabled!"
    else
        echo -e "[${GREENCOLOR}...${DEFAULTCOLOR}] HTTP disabled."
    fi

    HTTPSFOUND=$(${CURLCMD} -I "https://${TARGETHOST}" | grep "^HTTP")
    if [ -n "$HTTPSFOUND" ]; then
        echo -e "[${GREENCOLOR}...${DEFAULTCOLOR}] HTTPS is enabled."
    else
        echo -e "[${YELLOWCOLOR}---${DEFAULTCOLOR}] HTTPS is not enabled-"
    fi

    # Checking for HSTS http header
    HSTSHEADER=$(${CURLCMD} -I "https://${TARGETHOST}" | grep "^Strict")
    if [ -n "$HSTSHEADER" ]; then
        echo -e "[${GREENCOLOR}...${DEFAULTCOLOR}] Strict transport security header enabled."
    else
        echo -e "[${REDCOLOR}!!!${DEFAULTCOLOR}] Strict transport security header not found!"
    fi


    # Checking supported SSL/TLS protocols
    echo
    ISSSLV3=$(${CURLCMD} --sslv3 -I "https://${TARGETHOST}" | grep "^HTTP")
    ISTLSV10=$(${CURLCMD} --tlsv1.0 -I "https://${TARGETHOST}" | grep "^HTTP")
    ISTLSV11=$(${CURLCMD} --tlsv1.1 -I "https://${TARGETHOST}" | grep "^HTTP")
    ISTLSV12=$(${CURLCMD} --tlsv1.2 -I "https://${TARGETHOST}" | grep "^HTTP")
    if [ -n "$ISSSLV3" ]; then
        echo -e "[${REDCOLOR}!!!${DEFAULTCOLOR}] SSLv3 is enabled!"
    else
        echo -e "[${GREENCOLOR}...${DEFAULTCOLOR}] SSLv3 is disabled."
    fi
    if [ -n "$ISTLSV10" ]; then
        echo -e "[${REDCOLOR}!!!${DEFAULTCOLOR}] TLSv1.0 is enabled!"
    else
        echo -e "[${GREENCOLOR}...${DEFAULTCOLOR}] TLSv1.0 is disabled."
    fi
    if [ -n "$ISTLSV11" ]; then
        echo -e "[${REDCOLOR}!!!${DEFAULTCOLOR}] TLSv1.1 is enabled!"
    else
        echo -e "[${GREENCOLOR}...${DEFAULTCOLOR}] TLSv1.1 is disabled."
    fi
    if [ -n "$ISTLSV12" ]; then
        echo -e "[${GREENCOLOR}...${DEFAULTCOLOR}] TLSv1.2 is enabled."
    else
        echo -e "[${GREENCOLOR}...${DEFAULTCOLOR}] TLSv1.2 is disabled."
    fi

    # Checking content embedding protections
    echo
    XFOPTSSAME=$(${CURLCMD} -I "https://${TARGETHOST}" | grep "^X-Frame-Options" | grep "SAMEORIGIN")
    XFOPTSDENY=$(${CURLCMD} -I "https://${TARGETHOST}" | grep "^X-Frame-Options" | grep "DENY")
    if [ -n "$XFOPTSSAME" ];
    then
        echo -e "[${GREENCOLOR}...${DEFAULTCOLOR}] Content embedding protections enabled."
    elif [ -n "$XFOPTSDENY" ];
    then
        echo -e "[${GREENCOLOR}...${DEFAULTCOLOR}] Content embedding protections enabled."
    else
        echo -e "[${REDCOLOR}!!!${DEFAULTCOLOR}] Content embedding protections not found!"
    fi


    echo
    echo === Checking key lengths and supported symmetric ciphers ===
    echo
    nmap --script ssl-enum-ciphers -p 443 "${TARGETHOST}"
    echo
}

checksslcert() {
    echo
    echo
    echo === Checking server certificate length ===
    echo = 4096 bits recommended, 2048 bits minimum
    echo
    if [ ${CERTFILE} ]; then
        openssl s_client -cert "${CERTFILE}" -showcerts -connect "${TARGETHOST}:443" |& grep "^Server public key"
    else
        openssl s_client -showcerts -connect "${TARGETHOST}:443" |& grep "^Server public key"
    fi
    echo
    echo


    echo === Checking length of Diffie-Hellman prime ===
    echo = Should be no shorter than server certificate
    echo
    if [ ${CERTFILE} ]; then
        openssl s_client -cert "${CERTFILE}" -connect "${TARGETHOST}:443" -cipher "EDH" |& grep "^Server Temp Key"
    else
        openssl s_client -connect "${TARGETHOST}:443" -cipher "EDH" |& grep "^Server Temp Key"
    fi
    echo
}

checksslconf
#checksslcert
