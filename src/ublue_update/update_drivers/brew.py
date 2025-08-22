import os
from ublue_update.session import run_uid
import logging

log = logging.getLogger(__name__)

BREW_PREFIX = "/home/linuxbrew/.linuxbrew"
BREW_CELLAR = f"{BREW_PREFIX}/Cellar"
BREW_REPO = f"{BREW_PREFIX}/Homebrew"
BREW_PATH: str = f"{BREW_PREFIX}/bin/brew"



def detect_user() -> int:
    if not os.path.isdir(BREW_PREFIX):
        return -1
    return os.stat(BREW_PREFIX).st_uid


def brew_update(dry_run: bool):
    uid: int = detect_user()
    if uid == -1 or dry_run:
        return
    log.info(f"running brew updates for uid: {uid}")
    args: list[str] = [
        f"--setenv=HOMEBREW_PREFIX='{BREW_PREFIX}'",
        f"--setenv=HOMEBREW_CELLAR='{BREW_CELLAR}'",
        f"--setenv=HOMEBREW_REPOSITORY='{BREW_REPO}'",
    ]

    out = run_uid(uid, args + [f"{BREW_PATH}", "update"])
    if out.returncode != 0:
        log.error(
            f"brew update failed, returned code {out.returncode}, program output:"
        )
        log.error(out.stderr.decode("utf-8"))
        return

    out = run_uid(uid, args + [f"{BREW_PATH}", "upgrade"])
    if out.returncode != 0:
        log.error(
            f"brew upgrade failed, returned code {out.returncode}, program output:"
        )
        log.error(out.stderr.decode("utf-8"))
        return

    log.info("brew updates completed")
