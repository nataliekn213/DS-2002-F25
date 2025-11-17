#!/usr/bin/env bash

# positional arguments:
# $1 = local file to upload
# $2 = bucket name
# $3 = expiration time in seconds

aws s3 cp "$1" "s3://$2/"

aws s3 presign --expires-in "$3" "s3://$2/$(basename "$1")"
