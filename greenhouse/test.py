import os

uid = os.getuid()
os.setuid(int(os.environ['SUDO_UID']))
print(os.getenv('TEST'))
os.setuid(uid)
