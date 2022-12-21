#!/bin/bash

die() { echo "ERROR: $@" >&2; exit 1; }

# for f in /to-sign/*; do
#     if [[ $f == "/to-sign/*" ]]; then
#         echo "INFO: No files were found to sign in /to-sign. Exiting."
#         exit 0
#     else
#         break
#     fi
# done

if [[ -z $GPG_PRIVATE_KEY ]]; then
    die "You must specify your private key via GPG_PRIVATE_KEY"
fi

# if [[ -z $GPG_PASSPHRASE ]]; then
#     die "You must specify your passphrase via GPG_PASSPHRASE"
# fi

echo Importing private key:
# import private key
echo "$GPG_PRIVATE_KEY" > ~/private-key.pem
if ! gpg --import --batch --yes ~/private-key.pem; then
    die "Unable to import private key into GPG"
fi

# Run CMD
exec "$@"
