#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
FILE=${1:-ins.yml}
DAYS=${2:-36500}
BITS=${3-4096}
ES_VERSION=6.5.4
ES_DIR=/usr/share/elasticsearch/
CA_CERT=$DIR/certificates/ca/ca.crt
CA_KEY=$DIR/certificates/ca/ca.key
CERTS_XPACK=${ES_DIR}/certificates
ADDED_PARAMS=

if [ -e "$CA_KEY" ] && [ -e "$CA_CERT" ]
then
  ADDED_PARAMS="--cert $CERTS_XPACK/ca/ca.crt --key $CERTS_XPACK/ca/ca.key"
fi

if [ ! -d "$DIR/certificates"]
then
  mkdir $DIR/certificates
  chmod 0777 $DIR/certificates
fi

docker run -it --rm \
    -v "${DIR}/${FILE}:${ES_DIR}/${FILE}" \
    -v "${DIR}/certificates:${CERTS_XPACK}" \
    -w $ES_DIR \
    "docker.elastic.co/elasticsearch/elasticsearch:$ES_VERSION" \
    bin/elasticsearch-certgen -in $FILE --days $DAYS --keysize $BITS $ADDED_PARAMS \
        -out $ES_DIR/certificates/bundle.zip

unzip -o $DIR/certificates/bundle.zip -d $DIR/certificates/new

rm $DIR/certificates/bundle.zip

find $DIR/certificates/new -type f -name "*.key" -exec openssl pkcs8 -in '{}' -topk8 -nocrypt -out '{}.p8' \;

cp -pr $DIR/certificates/new/* $DIR/certificates/

rm -rf $DIR/certificates/new/