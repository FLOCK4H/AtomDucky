import storage
import supervisor

storage.remount('/', disable_concurrent_write_protection=True)
supervisor.runtime.autoreload = False