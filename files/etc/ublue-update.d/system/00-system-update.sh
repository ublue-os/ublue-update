#!/usr/bin/env bash

check_for_rebase() {
    IMAGE_REF_FILE="$1"
    if [ -f "$IMAGE_REF_FILE" ]; then

        STATUS_COMMAND="rpm-ostree status --pending-exit-77 -b --json"
        LOCAL_IMAGE_REF=$($STATUS_COMMAND | jq -r '.deployments[0]["container-image-reference"]' | sed 's@ostree-unverified-registry:@ostree-unverified-image:docker://@g')

        if ! $STATUS_COMMAND >/dev/null || [[ "$LOCAL_IMAGE_REF" == "null" ]]; then
            # if jq failed to get the variable, or rpm-ostree had a nonzero exit code, return
            return
        fi

        LOCAL_IMAGE_PREFIX=$(echo "$LOCAL_IMAGE_REF" | awk -F ":" '{print $1}')
        LOCAL_IMAGE_REF_UNTAGGED=$(echo "$LOCAL_IMAGE_REF" | awk -F ":" '{print $1":"$2":"$3}')
        LOCAL_IMAGE_REF_TAG=$(echo "$LOCAL_IMAGE_REF" | awk -F ":" '{print $4}')

        IMAGE_REF=$(jq -r '."image-ref"' < "$IMAGE_REF_FILE")
        IMAGE_TAG=$(jq -r '."image-tag"' < "$IMAGE_REF_FILE")

        if [[ "$LOCAL_IMAGE_REF_UNTAGGED" != "$IMAGE_REF" ]]; then
            if [[ "$LOCAL_IMAGE_PREFIX" == "ostree-unverified-image" ]]; then
                # preserve image tags
                IMAGE_TAG="$LOCAL_IMAGE_REF_TAG"
            fi
            /usr/bin/rpm-ostree rebase "$IMAGE_REF:$IMAGE_TAG"
            exit
        fi
    fi
}

if [ -x /usr/bin/rpm-ostree ]; then
    IMAGE_REF_FILE='/usr/share/ublue-os/image-info.json'
    check_for_rebase "$IMAGE_REF_FILE"
    /usr/bin/rpm-ostree upgrade
fi
