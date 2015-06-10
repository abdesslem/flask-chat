#!/bin/sh

[ $# -ne 1 ] && exit 0

out="/root/mail-agent/files"
pki="/root/easy-rsa/easyrsa3/pki"

rm -r $out
mkdir /root/mail-agent/files
rm /tmp/config.*

#code=$(tr -dc a-z0-9 </dev/urandom|head -c 8)
code=$(openssl rand -hex  3)

email=$(echo $1 | replace '@' '_')
#password=$(tr -dc A-Za-z0-9 </dev/urandom|head -c 10)
password=$(openssl rand -hex  5)
ssid="ashdworf_"$code
passphrase="ashdworf"

cat << EOF > $out/config
email = "$1"
password = "$password"
ssid = "$ssid"
passphrase = "$passphrase"
EOF

cd $pki/..
echo yes|./easyrsa revoke $email
./easyrsa gen-crl
rm $pki/reqs/$email.req
rm $pki/private/$email.key
rm $pki/issued/$email.crt
./easyrsa build-client-full $email nopass
cp $pki/ca.crt $out
cp $pki/private/$email.key $out/client.key
cp $pki/issued/$email.crt $out/client.crt
cd /tmp
tar zcf config.tar $out
gpg -o config.tar.sig --no-tty --always-trust --passphrase 1234 --sign config.tar

