# pydecclipper

Decrypt PGP-encrypted armored clipboard contents

# Requirements

- Tested with Ubuntu 16.04 using Unity Desktop, herbstluftwm with trayer
- Packages needed: `python3 python3-gi python-appindicator`

# Usage

Places a tray icon. Copy armored, PGP-encrypted text into the clipboard and
click `Decrypt` from the icon's menu. If the contents could be decrypted, a
window is spawned showing the plain text.

If `watch` is enabled either from the icon's menu or by using the command 
line parameter `-w`, the clipboard is watched for armored blocks, which 
are instantly shown.

Any clipboard content before and after the start/end markers  
```-----BEGIN PGP MESSAGE-----```  
```-----END PGP MESSAGE-----```  
is omitted. 
