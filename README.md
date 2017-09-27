# pydecclipper

Decrypt PGP encrypted armored clipboard contents

# Requirements

- Ubuntu 16.04
- Unity Desktop

- Run `sudo apt-get install python3 python3-gi python-appindicator`

# Usage

Places a tray icon. Copy armored, GPG-encrypted text into the clipboard and
click `Decrypt` from the icon's menu. If the contents could be decrypted, a
window is spawned showing the plain text.

Any text in the clipboard before and after the start/end markers
`-----BEGIN PGP MESSAGE-----`/`-----END PGP MESSAGE-----` is omitted.
