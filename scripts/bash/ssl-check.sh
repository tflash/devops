#!/bin/bash

EXPIRYALERTDAYS=157
REPORTEMAIL="tflash8@gmail.com"
LOGFILE=SSLreport.txt

for file in /etc/nginx/ssl/*.crt; do
    OUT=$(openssl x509 -noout -subject -in "$file" | awk -F'[=/]' '{print $NF}')
    EXPIRY=$( echo | openssl x509 -enddate -in "$file" -noout  2>/dev/null | grep notAfter | sed 's/notAfter=//')
    EXPIRYSIMPLE=$( date -d "$EXPIRY" +%F )
    EXPIRYSEC=$(date -d "$EXPIRY" +%s)
    TODAYSEC=$(date +%s)
    EXPIRYCALC=$(echo "($EXPIRYSEC-$TODAYSEC)/86400" | bc )

    if [ $EXPIRYCALC -lt $EXPIRYALERTDAYS ] ; then
        echo "SSL certificate for $OUT needs to be renewed by $EXPIRYSIMPLE (expires across $EXPIRYCALC days)" >> $LOGFILE
    #if [ $? != 0 ]; then
    #    echo "SSL certificate for $file has expired $EXPIRYSIMPLE (in $EXPIRYCALC days)" >> $LOGFILE
    #fi
    fi
done

# Report
mail -s "### ALERT ### SSL Report from STG on $(date)" $REPORTEMAIL <$LOGFILE

# Clear file
if [ -f SSLreport.txt ]; then
    rm SSLreport.txt
fi