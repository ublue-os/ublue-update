import subprocess
from typing import List, Optional
from logging import getLogger
from ublue_update.config import cfg

"""Setup logging"""
log = getLogger(__name__)


def run_custom_check_script(script) -> dict:
    if "run" in script and "shell" not in script:
        raise Exception(
            "checks.scripts.*: 'shell' must be specified when 'run' is used"
        )

    if "run" in script and "file" in script:
        raise Exception(
            "checks.scripts.*: Only one of 'run' and 'file' must be set for a given script"
        )

    log.debug(f"Running script {script}")

    # Run the specified custom script
    if "run" in script:
        run_args = [script["shell"], "-c", script["run"]]
    elif "shell" in script:
        run_args = [script["shell"], script["file"]]
    else:
        run_args = [script["file"]]
    script_result = subprocess.run(
        run_args, capture_output=True, text=True, check=False
    )

    # An exit code of 0 means "OK", a non-zero exit code
    # means "Do not download or perform updates right now"
    script_pass: bool = script_result.returncode == 0

    # Use either the message specified in the config,
    # the output of the script (if not empty), or a fallback
    script_output: Optional[str] = script_result.stdout.strip()
    if len(script_output) == 0:
        script_output = None

    # Write error messages to our log in case of failure
    # to catch any interpreter errors etc.
    script_stderr = script_result.stderr.strip()
    if not script_pass and len(script_stderr) > 0:
        log.warning(
            f"A custom check script failed and wrote the following to STDERR:\n====\n{script_stderr}\n===="
        )

    fallback_message = "A custom check script returned a non-0 exit code"
    script_message = script.get("message") or script_output or fallback_message

    return {
        "passed": script_pass,
        "message": script_message,
    }


def run_custom_check_scripts() -> List[dict]:
    results = []
    for script in cfg.custom_check_scripts or []:
        results.append(run_custom_check_script(script))
    return results


def check_custom_inhibitors() -> tuple[bool, list]:
    custom_inhibitors = run_custom_check_scripts()

    failures = []
    custom_checks_failed = False
    for inhibitor_result in custom_inhibitors:
        if not inhibitor_result["passed"]:
            custom_checks_failed = True
            failures.append(inhibitor_result["message"])
    if not custom_checks_failed:
        log.info("System passed custom checks")
    return custom_checks_failed, failures
