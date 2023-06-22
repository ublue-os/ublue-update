import psutil
import notify2
import os
import subprocess
import logging


def main():

	logging.basicConfig(
			format="[%(asctime)s] %(name)s:%(levelname)s | %(message)s",
			level=os.getenv("UBLUE_LOG", default=logging.INFO),
	)

	notify2.init('ubluepdater')

	battery_status = psutil.sensors_battery()
# get load average percentage in last 5 minutes: https://psutil.readthedocs.io/en/latest/index.html?highlight=getloadavg
	cpu_usage = psutil.getloadavg()[1] / psutil.cpu_count() * 100
	network_status = psutil.net_if_stats()

# check each network interface
	network_up = False
	for key in network_status.keys():
		if key != "lo":
			if network_status[key][0]:
				network_up = True
				break

	if (battery_status.percent < 50 and not battery_status.power_plugged) or cpu_usage > 50 or not network_up:
# system checks failed
		n = notify2.Notification("System Updater","System doesn't pass checks, aborting ...","notification-message-im")
		n.show()
		exit(0)

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
