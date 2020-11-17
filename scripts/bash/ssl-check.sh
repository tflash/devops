#!/bin/bash

EXPIRYALERTDAYS=60
REPORTEMAIL="tflash8@gmail.com"
LOGFILE=SSLreport.txt

for file in /etc/nginx/ssl/*.crt; do
    OUT=$(openssl x509 -noout -subject -in "$file" | awk -F'[=/]' '{print $NF}')
    EXPIRY=$( echo | openssl x509 -enddate -in "$file" -noout  2>/dev/null | grep notAfter | sed 's/notAfter=//')
    EXPIRYSIMPLE=$( date -d "$EXPIRY" +%F )
    EXPIRYSEC=$(date -d "$EXPIRY" +%s)
    TODAYSEC=$(date +%s)
    EXPIRYCALC=$(echo "($EXPIRYSEC-$TODAYSEC)/86400" | bc )

    if [ $? != 0 ] || [ $EXPIRYCALC -lt $EXPIRYALERTDAYS ] ; then
        echo "SSL certificate for $OUT needs to be renewed by $EXPIRYSIMPLE (expires across $EXPIRYCALC days)" >> $LOGFILE
        # Report to email
        mail -s "### ALERT ### SSL Report from Staging on $(date)" $REPORTEMAIL <$LOGFILE
    fi
done

# Clear file
if [ -f SSLreport.txt ]; then
    rm SSLreport.txt
fi
