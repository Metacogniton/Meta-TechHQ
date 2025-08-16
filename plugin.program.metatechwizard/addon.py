# -*- coding: utf-8 -*-
import ssl, urllib.request
import xbmc, xbmcaddon, xbmcgui, xbmcvfs

ADDON      = xbmcaddon.Addon()
ADDON_NAME = ADDON.getAddonInfo('name')

BUILD_URL = "https://raw.githubusercontent.com/Metacogniton/Meta-TechHQ/main/mt4.9.zip"
dest_path = xbmcvfs.translatePath("special://home/temp/mt4.9.zip")

def download(url, dest):
    try:
        temp_dir = xbmcvfs.translatePath("special://home/temp/")
        if not xbmcvfs.exists(temp_dir):
            xbmcvfs.mkdir(temp_dir)
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(url, context=ctx) as r:
            data = r.read()
        f = xbmcvfs.File(dest, 'w')
        f.write(bytearray(data))
        f.close()
        return True, None
    except Exception as e:
        return False, str(e)

def notify(msg):
    xbmcgui.Dialog().notification(ADDON_NAME, msg, time=5000)

def ensure_backup():
    if not xbmc.getCondVisibility('System.HasAddon(script.xbmcbackup)'):
        notify("Installing Backup add-on…")
        xbmc.executebuiltin('InstallAddon(script.xbmcbackup)')
        xbmc.sleep(2000)
    return xbmc.getCondVisibility('System.HasAddon(script.xbmcbackup)')

def main():
    notify("Downloading build…")
    ok, err = download(BUILD_URL, dest_path)
    if not ok:
        xbmcgui.Dialog().ok(ADDON_NAME, "Download failed", str(err))
        return
    notify("Build saved to temp. Opening Backup add-on…")
    if ensure_backup():
        xbmc.executebuiltin('RunAddon(script.xbmcbackup)')

if __name__ == "__main__":
    main()

