import sys
import os
from unittest.mock import patch, MagicMock, mock_open

# Add the src directory to the sys.path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
)

from ublue_update.update_inhibitors.hardware import (
    check_network_status,
    check_network_not_metered,
    check_battery_status,
    check_cpu_load,
    check_mem_percentage,
    check_hardware_inhibitors,
)


class BatteryStatus:
    def __init__(self, percent, secsleft=None, power_plugged=False):
        self.percent = percent
        self.secsleft = secsleft
        self.power_plugged = power_plugged


@patch("ublue_update.update_inhibitors.hardware.log")
@patch("ublue_update.update_inhibitors.hardware.psutil")
def test_check_network_status_up(mock_psutil, mock_log):
    mock_psutil.net_if_stats.return_value = {"eth0": "snicstats"}
    assert check_network_status()["passed"]
    mock_psutil.net_if_stats.assert_called_once_with()


@patch("ublue_update.update_inhibitors.hardware.log")
@patch("ublue_update.update_inhibitors.hardware.psutil")
def test_check_network_status_down(mock_psutil, mock_log):
    mock_psutil.net_if_stats.return_value = {"lo": "snicstats"}
    assert not check_network_status()["passed"]
    mock_psutil.net_if_stats.assert_called_once_with()


@patch("ublue_update.update_inhibitors.hardware.cfg")
@patch("ublue_update.update_inhibitors.hardware.subprocess.run")
def test_check_network_not_metered_metered(mock_run, mock_cfg):
    mock_cfg.network_not_metered = False
    assert check_network_not_metered()["passed"]


@patch("ublue_update.update_inhibitors.hardware.cfg")
@patch("ublue_update.update_inhibitors.hardware.subprocess.run")
def test_check_network_not_metered_unmetered(mock_run, mock_cfg):
    mock_run.return_value = MagicMock(stdout="u 1")
    mock_cfg.network_not_metered = True
    assert not check_network_not_metered()["passed"]
    mock_run.assert_called_once_with(
        [
            "busctl",
            "get-property",
            "org.freedesktop.NetworkManager",
            "/org/freedesktop/NetworkManager",
            "org.freedesktop.NetworkManager",
            "Metered",
        ],
        capture_output=True,
        check=True,
        text=True,
    )


@patch("ublue_update.update_inhibitors.hardware.cfg")
@patch("ublue_update.update_inhibitors.hardware.psutil")
def test_check_battery_status_min_percent_above(mock_psutil, mock_cfg):
    mock_cfg.min_battery_percent = 75
    mock_psutil.sensors_battery.return_value = BatteryStatus(20)
    assert not check_battery_status()["passed"]


@patch("ublue_update.update_inhibitors.hardware.cfg")
@patch("ublue_update.update_inhibitors.hardware.psutil")
def test_check_battery_status_min_percent_below(mock_psutil, mock_cfg):
    mock_cfg.min_battery_percent = 75
    mock_psutil.sensors_battery.return_value = BatteryStatus(99)
    assert check_battery_status()["passed"]


@patch("ublue_update.update_inhibitors.hardware.cfg")
@patch("ublue_update.update_inhibitors.hardware.psutil")
def test_check_battery_status_min_percent_no_battery(mock_psutil, mock_cfg):
    mock_cfg.min_battery_percent = 75
    mock_psutil.sensors_battery.return_value = None
    assert check_battery_status()["passed"]


@patch("ublue_update.update_inhibitors.hardware.cfg")
@patch("ublue_update.update_inhibitors.hardware.psutil")
def test_check_battery_status_min_percent_above_plugged(mock_psutil, mock_cfg):
    mock_cfg.min_battery_percent = 75
    mock_psutil.sensors_battery.return_value = BatteryStatus(20, power_plugged=True)
    assert check_battery_status()["passed"]


@patch("ublue_update.update_inhibitors.hardware.cfg")
@patch("ublue_update.update_inhibitors.hardware.psutil")
def test_check_battery_status_no_min_percent(mock_psutil, mock_cfg):
    mock_cfg.min_battery_percent = False
    assert check_battery_status()["passed"]


@patch("ublue_update.update_inhibitors.hardware.psutil")
@patch("ublue_update.update_inhibitors.hardware.cfg")
def test_check_cpu_load_max_percent_above(mock_cfg, mock_psutil):
    mock_cfg.max_cpu_load_percent = 50
    mock_psutil.getloadavg.return_value = [0.50, 0.49]
    mock_psutil.cpu_count.return_value = 1
    assert check_cpu_load()


@patch("ublue_update.update_inhibitors.hardware.psutil")
@patch("ublue_update.update_inhibitors.hardware.cfg")
def test_check_cpu_load_max_percent_below(mock_cfg, mock_psutil):
    mock_cfg.max_cpu_load_percent = 50
    mock_psutil.getloadavg.return_value = [0.50, 0.51]
    mock_psutil.cpu_count.return_value = 1
    assert not check_cpu_load()["passed"]


@patch("ublue_update.update_inhibitors.hardware.psutil")
@patch("ublue_update.update_inhibitors.hardware.cfg")
def test_check_cpu_load_no_max_percent(mock_cfg, mock_psutil):
    mock_cfg.max_cpu_load_percent = False
    assert check_cpu_load()["passed"]


@patch("ublue_update.update_inhibitors.hardware.psutil")
@patch("ublue_update.update_inhibitors.hardware.cfg")
def test_check_mem_percentage_max_percent_above(mock_cfg, mock_psutil):
    mock_cfg.max_mem_percent = 50
    memory = MagicMock()
    memory.percent = 49
    mock_psutil.virtual_memory.return_value = memory
    assert check_mem_percentage()["passed"]


@patch("ublue_update.update_inhibitors.hardware.psutil")
@patch("ublue_update.update_inhibitors.hardware.cfg")
def test_check_mem_percentage_max_percent_below(mock_cfg, mock_psutil):
    mock_cfg.max_mem_percent = 50
    memory = MagicMock()
    memory.percent = 51
    mock_psutil.virtual_memory.return_value = memory
    assert not check_mem_percentage()["passed"]


@patch("ublue_update.update_inhibitors.hardware.cfg")
def test_check_mem_percentage_no_max_percent(mock_cfg):
    mock_cfg.max_mem_percent = None
    assert check_mem_percentage()["passed"]


@patch("ublue_update.update_inhibitors.hardware.check_network_status")
@patch("ublue_update.update_inhibitors.hardware.check_network_not_metered")
@patch("ublue_update.update_inhibitors.hardware.check_battery_status")
@patch("ublue_update.update_inhibitors.hardware.check_cpu_load")
@patch("ublue_update.update_inhibitors.hardware.check_mem_percentage")
def test_check_hardware_inhibitors_pass(
    mock_check_network_status,
    mock_check_network_not_metered,
    mock_check_battery_status,
    mock_check_cpu_load,
    mock_check_mem_percentage,
):
    mock_check_network_status.return_value = {"passed": True}
    mock_check_network_not_metered.return_value = {"passed": True}
    mock_check_battery_status.return_value = {"passed": True}
    mock_check_cpu_load.return_value = {"passed": True}
    mock_check_mem_percentage.return_value = {"passed": True}

    assert not check_hardware_inhibitors()[0]


@patch("ublue_update.update_inhibitors.hardware.check_network_status")
@patch("ublue_update.update_inhibitors.hardware.check_network_not_metered")
@patch("ublue_update.update_inhibitors.hardware.check_battery_status")
@patch("ublue_update.update_inhibitors.hardware.check_cpu_load")
@patch("ublue_update.update_inhibitors.hardware.check_mem_percentage")
def test_check_hardware_inhibitors_fail(
    mock_check_network_status,
    mock_check_network_not_metered,
    mock_check_battery_status,
    mock_check_cpu_load,
    mock_check_mem_percentage,
):
    failure_message = "Test failure."
    mock_check_network_status.return_value = {
        "passed": False,
        "message": failure_message,
    }
    mock_check_network_not_metered.return_value = {"passed": True}
    mock_check_battery_status.return_value = {"passed": True}
    mock_check_cpu_load.return_value = {"passed": True}
    mock_check_mem_percentage.return_value = {"passed": True}

    result = check_hardware_inhibitors()
    assert result[0]
    assert result[1][0] == failure_message
    assert len(result[1]) == 1
