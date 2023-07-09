import dbus

from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib


class NotificationObject:
    """Holds all of the data in a notification"""

    def __init__(self, notification_manager, app_name, icon="", title="", body=""):
        self.notification_manager = notification_manager
        self.app_name = app_name
        self.id = 0
        self.icon = icon
        self.title = title
        self.body = body
        self.actions = {}
        self.hints = {}

    def add_action(self, key, text, handler):
        self.actions.update({key: {"text": text, "handler": handler}})

    def add_hint(self, hint):
        self.hints.update(hint)

    def show(self, timeout_sec):
        #self.notification_manager.loop.run()
        actions = self.notification_manager.get_action_list(self.actions)
        self.id = self.notification_manager.notify_interface.Notify(
            self.app_name,
            self.id,
            self.icon,
            self.title,
            self.body,
            actions,
            self.hints,
            timeout_sec * 1000,
        )
        self.notification_manager.notifications.update({self.id: self})
        if self.actions:
            self.notification_manager.loop.run()


class NotificationManager:
    """Manages DBus notifications and action dispatching"""

    def __init__(self, app_name):
        item = "org.freedesktop.Notifications"
        path = "/" + item.replace(".", "/")
        self.dbus_loop = DBusGMainLoop()
        self.loop = GLib.MainLoop()
        self._bus = dbus.SessionBus(mainloop=self.dbus_loop)
        self._bus.add_signal_receiver(self._on_action, "ActionInvoked")
        self._bus.add_signal_receiver(self._on_closed, "NotificationClosed")
        self._app_name = app_name
        self.notifications = {}
        self.notify_interface = dbus.Interface(self._bus.get_object(item, path), item)

    def get_action_list(self, actions):
        dbus_actions = []
        for action in actions:
            action_dict = actions.get(action)
            dbus_actions.append(action)
            dbus_actions.append(action_dict["text"])
        return dbus_actions

    def add_action(self, action):
        self._actions.append(action)

    def _on_action(self, id, action_key):
        notification = self.notifications.get(id)
        if notification:
            triggered_action = notification.actions.get(action_key)
            triggered_action["handler"]()
        self.loop.quit()

    def _on_closed(self, id, reason):
        if self.loop.is_running():
            self.loop.quit()

    def notification(self, title, body, icon=""):
        return NotificationObject(self, self._app_name, icon, title, body)
