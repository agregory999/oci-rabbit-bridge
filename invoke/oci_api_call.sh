#!/bin/bash
 
 
########################## Fill these in with your values ##########################
#OCID of the tenancy calls are being made in to
tenancy_ocid="ocid1.tenancy.oc1..aaaaaaaa5arrzhx6wibc7iotaztfkt5bofbrfkw4x56kaplt36tat63lexgq"
 
# OCID of the user making the rest call
user_ocid="ocid1.user.oc1..aaaaaaaaradfpfpjogoytgqvbi3u2mpqolhw67nqo5ixdvk73ddhvma3fc2a"
 
# path to the private PEM format key for this user
privateKeyPath="/Users/argregor/Downloads/oracleidentitycloudservice_andrew.gregory-02-16-16-13.pem"
#privateKeyPath="/Users/argregor/.oci/oci_api_key.pem"
 
# fingerprint of the private key for this user
fingerprint="56:44:93:6f:37:6a:16:b7:d8:28:f7:6f:f5:c5:11:83"
#fingerprint="5b:0a:43:58:38:3c:47:e7:77:e9:9e:4b:78:46:cb:54"
 
# The REST api you want to call, with any required paramters.
#rest_api="/20160918/instances?compartmentId=ocid1.compartment.oc1..<unique_id>"
rest_api="/20181201/functions/ocid1.fnfunc.oc1.iad.aaaaaaaaaaexsqq4z6xrcyikogrvpqqnvmpi3fo2kndsfjvqp4f3bkaaj7fq/actions/invoke"
#rest_api="/20181201/functions/ocid1.fnfunc.oc1.iad.aaaaaaaaaaexsqq4z6xrcyikogrvpqqnvmpi3fo2kndsfjvqp4f3bkaaj7fq"
#rest_api="/20181201/applications/ocid1.fnapp.oc1.iad.aaaaaaaaae4yfxpskji7w4izxpddjkgvbixgj3gdlrx42r3okildnnoibneq"
 
# The host you want to make the call against
#host="iaas.us-ashburn-1.oraclecloud..."
host="ildnnoibneq.us-ashburn-1.functions.oci.oraclecloud.com"

# the json file containing the data you want to POST to the rest endpoint
body="./request.json"
####################################################################################
 
 
# extra headers required for a POST/PUT request
body_arg=(--data-binary @${body})
content_sha256="$(openssl dgst -binary -sha256 < $body | openssl enc -e -base64)";
content_sha256_header="x-content-sha256: $content_sha256"
content_length="$(wc -c < $body | xargs)";
content_length_header="content-length: $content_length"
headers="(request-target) date host"
# add on the extra fields required for a POST/PUT
headers=$headers" x-content-sha256 content-type content-length"
content_type_header="content-type: application/json";
 
date=`date -u "+%a, %d %h %Y %H:%M:%S GMT"`
date_header="date: $date"
host_header="host: $host"
request_target="(request-target): post $rest_api"
 
# note the order of items. The order in the signing_string matches the order in the headers, including the extra POST fields
signing_string="$request_target\n$date_header\n$host_header"
# add on the extra fields required for a POST/PUT
signing_string="$signing_string\n$content_sha256_header\n$content_type_header\n$content_length_header"
 
 
 
 
echo "====================================================================================================="
printf '%b' "signing string is $signing_string \n"
signature=`printf '%b' "$signing_string" | openssl dgst -sha256 -sign $privateKeyPath | openssl enc -e -base64 | tr -d '\n'`
printf '%b' "Signed Request is  \n$signature\n"
 
echo "====================================================================================================="
set -x
curl -X POST --data-binary "@request.json" -sS https://$host$rest_api -H "date: $date" -H "x-content-sha256: $content_sha256" -H "content-type: application/json" -H "content-length: $content_length" -H "Authorization: Signature version=\"1\",keyId=\"$tenancy_ocid/$user_ocid/$fingerprint\",algorithm=\"rsa-sha256\",headers=\"$headers\",signature=\"$signature\""
