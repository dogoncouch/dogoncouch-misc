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
    echo "Usage: ${0##*/} [-hv] [options...] HOST"
    echo "  -h                  Print this help message"
    echo "  -v                  Print the version number"
    echo "  -f                  Full ssl certificate check"
    echo "  -i                  Accept untrusted certificates"
    echo "  -l                  Use color output for light background"
    echo "  -c CERTFILE         Set a CA certificate for verification"
    echo "  -o 'CURLOPTS'       Set additional options for curl"
    echo "  -p PORT             Set SSH port"
    echo "  -s PORT             Set HTTPS port"
}

CURLCMD="curl -s"
OPENSSLCMD="openssl s_client"
SSHPORT="22"
SSLPORT="443"

while getopts ":vhfilc:o:p:s:" o; do
    case "${o}" in
        v)
            echo ssltest-$VERSION
            exit 0
            ;;
        h)
            usage
            exit 0
            ;;
        f)
            FULLCERTCHECK=1
            ;;
        i)
            INSECUREMODE=1
            CURLCMD="${CURLCMD} -k"
            ;;
        l)
            LIGHTBG=1
            ;;
        c)
            OPENSSLCMD="${OPENSSLCMD} -cert '${OPTARG}'"
            CURLCMD="${CURLCMD} --cacert '${OPTARG}'"
            ;;
        o)
            CURLCMD="${CURLCMD} ${OPTARG}"
            ;;
        p)
            SSHPORT="${OPTARG}"
            ;;
        s)
            SSLPORT="${OPTARG}"
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
    if [ $LIGHTBG ]; then
        DEFAULTCOLOR="\e[0m"
        REDCOLOR="\e[101m"
        GREENCOLOR="\e[102m"
        YELLOWCOLOR="\e[103m"
        CYANCOLOR="\e[34m"
    else
        DEFAULTCOLOR="\e[0m"
        REDCOLOR="\e[91m"
        GREENCOLOR="\e[92m"
        YELLOWCOLOR="\e[93m"
        CYANCOLOR="\e[96m"
    fi
else
    DEFAULTCOLOR=""
    REDCOLOR=""
    GREENCOLOR=""
    YELLOWCOLOR=""
    CYANCOLOR=""
fi


checksslconn() {
    echo
    if [ -z "$(which curl)" ]; then
        echo "${REDCOLOR}Error:${DEFAULTCOLOR} curl not found in path."
        exit 1
    fi
    echo -e "${CYANCOLOR}=== Web server info for ${TARGETHOST} ===${DEFAULTCOLOR}"
    # Print web server info
    SERVERTYPESSL=$(${CURLCMD} -I "https://${TARGETHOST}:${SSLPORT}" | grep "^Server: ")
    SERVERTYPEHTTP=$(${CURLCMD} -I "http://${TARGETHOST}" | grep "^Server: ")
    SERVERTYPE8K=$(${CURLCMD} -I "http://${TARGETHOST}:8000" | grep "^Server: ")

    # Check for unsecured HTTP
    HTTPMOVED=$(${CURLCMD} -I "http://${TARGETHOST}" | grep "^HTTP" | grep "301 Moved Permanently")
    HTTPFOUND=$(${CURLCMD} -I "http://${TARGETHOST}" | grep "^HTTP" | grep "302 Found")
    if [ -n "$HTTPMOVED" ]; then
        echo -e "[${GREENCOLOR}...${DEFAULTCOLOR}] HTTP redirects on port 80."
    elif [ -n "$HTTPFOUND" ]; then
        echo -e "[${REDCOLOR}!!!${DEFAULTCOLOR}] Unsecured HTTP is enabled on port 80! ${SERVERTYPEHTTP}"
    else
        echo -e "[${GREENCOLOR}...${DEFAULTCOLOR}] HTTP is disabled on port 80."
    fi

    HTTP8KFOUND=$(${CURLCMD} -I "http://${TARGETHOST}:8000" | grep "^HTTP" | grep "302 Found")
    if [ -n "$HTTP8KFOUND" ]; then
        echo -e "[${REDCOLOR}!!!${DEFAULTCOLOR}] Unsecured HTTP is enabled on port 8000! ${SERVERTYPE8K}"
    else
        echo -e "[${GREENCOLOR}...${DEFAULTCOLOR}] HTTP is disabled on port 8000."
    fi
    # Check for HTTPS
    HTTPSFOUND=$(${CURLCMD} -I "https://${TARGETHOST}:${SSLPORT}" | grep "^HTTP")
    if [ -n "$HTTPSFOUND" ]; then
        echo -e "[${GREENCOLOR}...${DEFAULTCOLOR}] HTTPS is enabled on port ${SSLPORT}. ${SERVERTYPESSL}"

        # Check supported SSL/TLS protocols
        echo
        echo -e "${CYANCOLOR}=== Supported HTTPS protocols ===${DEFAULTCOLOR}"
        ISSSLV2=$(${CURLCMD} --sslv2 -I "https://${TARGETHOST}" | grep "^HTTP")
        ISSSLV3=$(${CURLCMD} --sslv3 -I "https://${TARGETHOST}" | grep "^HTTP")
        ISTLSV10=$(${CURLCMD} --tlsv1.0 -I "https://${TARGETHOST}" | grep "^HTTP")
        ISTLSV11=$(${CURLCMD} --tlsv1.1 -I "https://${TARGETHOST}" | grep "^HTTP")
        ISTLSV12=$(${CURLCMD} --tlsv1.2 -I "https://${TARGETHOST}" | grep "^HTTP")
        if [ -n "$ISSSLV2" ]; then
            echo -e "[${REDCOLOR}!!!${DEFAULTCOLOR}] SSLv2 is enabled!"
        else
            echo -e "[${GREENCOLOR}...${DEFAULTCOLOR}] SSLv2 is disabled."
        fi
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
            echo -e "[${YELLOWCOLOR}---${DEFAULTCOLOR}] TLSv1.2 is disabled."
        fi

        echo
        echo -e "${CYANCOLOR}=== Header attributes ===${DEFAULTCOLOR}"
        # Check for HSTS http header
        HSTSHEADER=$(${CURLCMD} -I "https://${TARGETHOST}" | grep "^Strict")
        if [ -n "$HSTSHEADER" ]; then
            echo -e "[${GREENCOLOR}...${DEFAULTCOLOR}] Strict transport security header enabled."
        else
            echo -e "[${REDCOLOR}!!!${DEFAULTCOLOR}] Strict transport security header not found!"
        fi

        # Check content embedding protections
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

        # Check ciphers with nmap
        echo
        echo -e "${CYANCOLOR}=== Key lengths and supported symmetric ciphers ===${DEFAULTCOLOR}"
        if [ -z "$(which nmap)" ]; then
            echo -e "${REDCOLOR}Error:${DEFAULTCOLOR} nmap not found in path. Skipping cipher enumeration."
        else
            nmap --script ssl-enum-ciphers -p "${SSLPORT}" "${TARGETHOST}"
        fi

    else
        if [ "$INSECUREMODE" ]; then
            echo -e "[${YELLOWCOLOR}---${DEFAULTCOLOR}] HTTPS is disabled on port ${SSLPORT}."
        else
            echo -e "[${YELLOWCOLOR}---${DEFAULTCOLOR}] HTTPS is disabled or cert not trusted on port ${SSLPORT}. Try -i option."
        fi
    fi
    echo
}

checksslcert() {
    # Check server certificate
    echo
    if [ -z "$(which openssl)" ]; then
        echo "${REDCOLOR}Error:${DEFAULTCOLOR} openssl not found in path. Skipping certificate check."
    else
        echo -e "${CYANCOLOR}=== Server certificate ===${DEFAULTCOLOR}"
        echo -e "${CYANCOLOR}= Server public key: 4096 bits recommended, 2048 bits minimum =${DEFAULTCOLOR}"
        CERTINFO=$(${OPENSSLCMD} -showcerts -connect "${TARGETHOST}:${SSLPORT}" -verify_hostname "${TARGETHOST}" |& grep -e "^Server public key" -e "^depth=" -e "^verify error:" -e "^verify return:" -e "Verify return code:")
        if [ -n "$CERTINFO" ]; then
            echo "$CERTINFO"
        else
            echo -e "[${YELLOWCOLOR}---${DEFAULTCOLOR}] No server public key."
        fi

        # Check DH key length
        echo
        echo -e "${CYANCOLOR}= Diffie-Hellman temp key: should be no shorter than public key =${DEFAULTCOLOR}"
        DHTEMPKEY=$(${OPENSSLCMD} -connect "${TARGETHOST}:${SSLPORT}" -cipher "EDH" |& grep "^Server Temp Key")
        if [ -n "$DHTEMPKEY" ]; then
            echo "$DHTEMPKEY"
        else
            echo -e "[${YELLOWCOLOR}---${DEFAULTCOLOR}] No DH temp key."
        fi
        echo
    fi
}

checksshconn() {
    echo
    if [ -z "$(which ssh)" ]; then
        echo "${REDCOLOR}Error:${DEFAULTCOLOR} ssh not found in path."
        exit 1
    fi
    echo -e "${CYANCOLOR}=== SSH protocol information ===${DEFAULTCOLOR}"
    NOSSH=$(ssh -v -o PasswordAuthentication=no -o PubkeyAuthentication=no -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p "${SSHPORT}" "user@${TARGETHOST}" |& grep "^ssh: connect to host ${TARGETHOST} port ${SSHPORT}: Connection refused")
    if [ -n "$NOSSH" ]; then
        echo -e "[${YELLOWCOLOR}---${DEFAULTCOLOR}] SSH is disabled on port ${SSHPORT}."
    else
        echo -e "${CYANCOLOR}= SSH version 1 =${DEFAULTCOLOR}"
        NOSSHV1=$(ssh -1v -o PasswordAuthentication=no -o PubkeyAuthentication=no -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p "${SSHPORT}" "user@${TARGETHOST}" |& grep "^Protocol major versions differ")
        if [ -n "$NOSSHV1" ]; then
            echo -e "[${GREENCOLOR}...${DEFAULTCOLOR}] SSH version 1 is disabled."
        else
            echo -e "[${REDCOLOR}!!!${DEFAULTCOLOR}] SSH version 1 is enabled!"
        fi
        echo
        echo -e "${CYANCOLOR}= SSH version 2 =${DEFAULTCOLOR}"
        SSHV2=$(ssh -2 -v -o PasswordAuthentication=no -o PubkeyAuthentication=no -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p "${SSHPORT}" "user@${TARGETHOST}" |& grep -o -e "Remote protocol version .*$" -e "Server host key: .*$" -e "Authentications that can continue: .*$")
        if [ -n "$SSHV2" ]; then
            echo -e "[${GREENCOLOR}...${DEFAULTCOLOR}] SSH version 2 is enabled."
            echo
            echo "$SSHV2"
        else
            echo -e "[${YELLOWCOLOR}---${DEFAULTCOLOR}] SSH version 2 is disabled."
        fi
    fi
    echo
}

checksslconn
if [ $FULLCERTCHECK ]; then
    checksslcert
fi
checksshconn
exit 0
