import psutil
import notify2
import os
import subprocess
import logging
import configparser


default_config = """
[checks]
battery_percent = 50
cpu_load = 50
"""

def checks(config):
	check_battery_percent = float(config['checks']['battery_percent'])
	check_cpu_load = float(config['checks']['cpu_load'])
	
	battery_status = psutil.sensors_battery()
# get load average percentage in last 5 minutes: https://psutil.readthedocs.io/en/latest/index.html?highlight=getloadavg
	cpu_load = psutil.getloadavg()[1] / psutil.cpu_count() * 100
	network_status = psutil.net_if_stats()

# check each network interface
	network_up = False
	for key in network_status.keys():
		if key != "lo":
			if network_status[key][0]:
				network_up = True
				break
	
	errors = {
		battery_status: [battery_status.percent > check_battery_percent or battery_status.power_plugged, "battery"],
		cpu_load: [cpu_load < check_cpu_load, "CPU load"],
		network_up: [network_up, "network"]
	}
	return errors


def main():
# load config values
	config_paths = [
		os.path.expanduser('~/.config/auto-update/auto-update.conf'),
		"/etc/auto-update/auto-update.conf",
		"/usr/etc/auto-update/auto-update.conf"
		]

	config_path = ""

	for path in config_paths:
		if os.path.isfile(path):
			config_path = path
			break

	if config_path == "":
		config_path = config_paths[0]
		os.makedirs(os.path.dirname(config_path))
		with open(config_path, "w") as f:
			f.write(default_config)

	config = configparser.ConfigParser()
	config.read(config_path)
	logging.basicConfig(
			format="[%(asctime)s] %(name)s:%(levelname)s | %(message)s",
			level=os.getenv("UBLUE_LOG", default=logging.INFO),
	)

	notify2.init('auto-update')

	errors = checks(config)
	for key in errors:
		if not errors[key][0]:
			n = notify2.Notification("System Updater","System doesn't pass " + errors[key][1] + " check; aborting ...","notification-message-im")
			n.show()
			exit(0)
# system checks failed
	

# system checks passed
	n = notify2.Notification("System Updater","System passed checks, updating ...","notification-message-im")
	n.show()

	root_dir = str(os.path.dirname(__file__)) + "/update-scripts"

# execute update commands
	for root, dirs, files in os.walk(root_dir):
		for file in files:
			full_path = root_dir + "/" + str(file)
			list_files = subprocess.run([full_path])

main()
