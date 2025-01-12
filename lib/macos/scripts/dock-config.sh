#!/bin/sh

defaults write com.apple.dock persistent-apps -array

#Add Safari
defaults write com.apple.dock persistent-apps -array-add '{"tile-type"="file-tile";"tile-data"={"file-data"={"_CFURLString"="/Applications/Safari.app";"_CFURLStringType"=0;};};}'

#Add System Settings
defaults write com.apple.dock persistent-apps -array-add '{"tile-type"="file-tile";"tile-data"={"file-data"={"_CFURLString"="/System/Applications/System Settings.app";"_CFURLStringType"=0;};};}'

# Restart the dock
killall Dock

echo "Dock configured with Safari and System Settings."