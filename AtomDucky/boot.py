import storage
import supervisor

# Uncomment the line below to hide usb drive
#storage.disable_usb_drive()
storage.remount('/', disable_concurrent_write_protection=True)
supervisor.runtime.autoreload = False
