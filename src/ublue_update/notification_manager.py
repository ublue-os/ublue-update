import dbus
from dbus.mainloop.glib import DBusGMainLoop


class NotificationManager:
    """Manages DBus notifications and action dispatching"""

    def __init__(self, app_name):
        item = "org.freedesktop.Notifications"
        path = "/" + item.replace(".", "/")
        self.dbus_loop = DBusGMainLoop()
        self._bus = dbus.SessionBus(mainloop=self.dbus_loop)
        self._bus.add_signal_receiver(self._on_action, "ActionInvoked")
        self._app_name = app_name
        self._actions = []
        self._notify_interface = dbus.Interface(self._bus.get_object(item, path), item)


    def get_action_list(self, actions):
        dbus_actions = []
        for action in actions:
            dbus_actions.append(action["key"])
            dbus_actions.append(action["text"])
        return dbus_actions

    def add_action(self, action):
        self._actions.append(action)

    def _on_action(self, id, action_key):
        triggered_action = [
            action for action in self._actions if action["key"] == action_key
        ][0]
        triggered_action["handler"]()

    def notify(self, id, title, body, timeout):
        actions = self.get_action_list(self._actions)
        self._notify_interface.Notify(
            self._app_name,
            id,
            "weather-clear",  # not sure what this is
            title,
            body,
            actions,
            {"urgency": 1},
            timeout * 1000,
        )
