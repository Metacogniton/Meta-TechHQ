# -*- coding: utf-8 -*-
import os, ssl, sys, urllib.request
import xbmc, xbmcaddon, xbmcgui, xbmcvfs

ADDON      = xbmcaddon.Addon()
ADDON_ID   = ADDON.getAddonInfo('id')
ADDON_NAME = ADDON.getAddonInfo('name')

# Raw URL for your build (Git LFS works via raw/media URL)
BUILD_URL = "https://raw.githubusercontent.com/Metacogniton/Meta-TechHQ/main/mt4.9.zip"

# Save to Kodi's temp folder
dest_path = xbmcvfs.translatePath("special://home/temp/mt4.9.zip")

def download(url, dest):
    try:
        # ensure temp folder exists
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

def notify(heading, message, ms=5000):
    xbmcgui.Dialog().notification(heading, message, time=ms)

def ensure_backup_addon():
    # Install Backup add-on if missing
    if not xbmc.getCondVisibility('System.HasAddon(script.xbmcbackup)'):
        notify(ADDON_NAME, "Installing Backup add-on…")
        xbmc.executebuiltin('InstallAddon(script.xbmcbackup)')
        # give Kodi a moment
        xbmc.sleep(2000)
    return xbmc.getCondVisibility('System.HasAddon(script.xbmcbackup)')

def main():
    notify(ADDON_NAME, "Downloading build…")
    ok, err = download(BUILD_URL, dest_path)
    if not ok:
        xbmcgui.Dialog().ok(ADDON_NAME, "Download failed:", str(err))
        return

    notify(ADDON_NAME, "Build saved to temp.\nOpening Backup add-on…", 6000)

    if ensure_backup_addon():
        # Open Backup add-on UI; user selects the downloaded zip for restore
        xbmc.executebuiltin('RunAddon(script.xbmcbackup)')
    else:
        xbmcgui.Dialog().ok(ADDON_NAME, "Could not install/open Backup add-on.",
                            "Please install 'Backup' (script.xbmcbackup) from Kodi repo and try again.")

if __name__ == "__main__":
    main()
