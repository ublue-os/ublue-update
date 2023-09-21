#!/usr/bin/env bash

check_for_rebase() {
    IMAGE_REF_FILE="$1"
    LOCAL_IMAGE_REF=$(rpm-ostree status --pending-exit-77 -b --json | jq -r '.deployments[0]["container-image-reference"]')
    if [[ $LOCAL_IMAGE_REF == "null" ]]; then
        return
    fi
    if [ -f $IMAGE_REF_FILE ]; then
        LOCAL_IMAGE_REF_UNTAGGED=$(echo $LOCAL_IMAGE_REF | awk -F ":" '{print $1":"$2":"$3}')
        IMAGE_REF=$(cat $IMAGE_REF_FILE | jq -r '."image-ref"')
        IMAGE_DEFAULT_TAG=$(cat $IMAGE_REF_FILE | jq -r '."image-default-tag"')

        if [[ $LOCAL_IMAGE_REF_UNTAGGED != $IMAGE_REF ]]; then
            /usr/bin/rpm-ostree rebase "$IMAGE_REF:$IMAGE_DEFAULT_TAG"
            exit
        fi
    fi
}

if [ -x /usr/bin/rpm-ostree ]; then
    IMAGE_REF_FILE='/var/home/user/ublue-image-info.json'
    check_for_rebase $IMAGE_REF_FILE
    /usr/bin/rpm-ostree upgrade
fi
