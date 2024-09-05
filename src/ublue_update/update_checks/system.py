from json import loads
from json.decoder import JSONDecodeError
from logging import getLogger
from subprocess import run

"""Setup logging"""
log = getLogger(__name__)


def skopeo_inspect(latest_image: str):
    """Inspect latest image with Skopeo"""
    skopeo_inspect = ["skopeo", "inspect", latest_image]
    inspect = run(skopeo_inspect, capture_output=True).stdout
    """Parse and return digest"""
    digest = loads(inspect)["Digest"]
    return digest


def system_update_check():
    """Pull deployment status via rpm-ostree"""
    rpm_ostree_status = ["rpm-ostree", "status", "--json"]
    status = run(rpm_ostree_status, capture_output=True).stdout
    """Parse installation digest and image"""
    try:
        deployments = loads(status)["deployments"][0]
        installation_digest = deployments["base-commit-meta"]["ostree.manifest-digest"]
        current_image = deployments["container-image-reference"].split(":", 1)
    except (JSONDecodeError, KeyError):
        log.error(
            "update check failed, system isn't managed by rpm-ostree container native"
        )
        return False

    """Dissect current image to form URL to latest image"""
    protocol = "docker://"
    url = current_image[1]

    if url == "oci:/var/ublue-os/image":
        return True

    """Add protocol if URL doesn't contain it"""
    if protocol not in url:
        url = protocol + url

    """Pull digest from latest image"""
    latest_digest = skopeo_inspect(url)

    """Compare current digest to latest digest"""
    if installation_digest == latest_digest:
        """Digests match, so no updates"""
        log.info("No system update available.")
        return False
    """Digests do not match, so updates are available"""
    log.info("System update available.")
    return True


def pending_deployment_check():
    rpm_ostree_cmd = ["rpm-ostree", "status", "--pending-exit-77"]
    status = run(rpm_ostree_cmd, capture_output=True)
    if status.returncode == 77:  # pending deployment
        return True
    return False
