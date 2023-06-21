import psutil
import notify2
notify2.init('ubluepdater')

battery_status = psutil.sensors_battery()
cpu_usage = psutil.cpu_percent()
print(cpu_usage)
if battery_status.percent < 70 or cpu_usage > 50:
	n = notify2.Notification("System Updater","System doesn't pass checks, aborting...","notification-message-im")
	n.show()
	exit(1)

	n = notify2.Notification("System Updater","System doesn't pass checks, aborting...","notification-message-im")
	n.show()

# execute update commands

