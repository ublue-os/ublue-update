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
	cpu_usage = psutil.cpu_percent()

	if (battery_status.percent < 70 and not battery_status.power_plugged) or cpu_usage > 50:
# system checks failed
		n = notify2.Notification("System Updater","System doesn't pass checks, aborting ...","notification-message-im")
		n.show()
		exit(1)

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
