from django.contrib.sessions.backends.db import SessionStore


class OrderSessionStore(SessionStore):
    """Теперь есть возможность сохранять данные сессии после login()"""
    def cycle_key(self):
        super().cycle_key()
        self.save()
