$WallpaperPath = "C:\Path\To\Your\Image.jpg"
$RegistryPath = "HKCU:\Control Panel\Desktop"

Set-ItemProperty -Path $RegistryPath -Name Wallpaper -Value $WallpaperPath
RUNDLL32.EXE user32.dll, UpdatePerUserSystemParameters
