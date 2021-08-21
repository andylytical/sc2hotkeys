Design a Starcraft hotkey layout and generate the config file

# Usage

### Create Custom Keymap Layout
- Make a copy of
   [this Google
   Spreadsheet](https://docs.google.com/spreadsheets/d/11IbMmtnZ-CFz4Jwdcv1voa4l1YZd3FsB9hsZByuPVO0)
- Edit the `SC2Commands` tab
- Export the `SC2Commands` tab as `commands.csv`
- Export the `SC2CommandCodes` tab as `commandcodes.csv`

### Setup
- `git clone https://github.com/andylytical/sc2hotkeys.git`
- `cd sc2hotkeys/`
- `bash setup.sh`

### Make a new Hotkey file
- `./csv2hotkeys.py -C commandcodes.csv -c commands.csv > SC2Hotkeys`

# References
- [Empty SC2Hotkeys file](https://gist.github.com/pedz/3ab6b1aa7fb4f41b354a7a82f5ba522b)
- [The
  Core](https://drive.google.com/drive/folders/1ui2HNwaUa4FkHzRwATgXHNVEpolLNOzA)
  - Especially
    [TheCore 6.0 Spreadsheet - An account of all important keys and their bindings](https://docs.google.com/spreadsheets/d/1CiJwE46S_Kt_ZkVNyXnrjMD15ZSZlv3JSG8nkpjHHtc)
