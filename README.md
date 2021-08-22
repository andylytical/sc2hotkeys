Generate a Starcraft2 hotkey config file from the planning spreadsheet.

# Usage

### Create Custom Keymap Layout
- Make a copy of this Google Sheet:
  [Starcraft Hotkey Planner](https://docs.google.com/spreadsheets/d/11IbMmtnZ-CFz4Jwdcv1voa4l1YZd3FsB9hsZByuPVO0)
- Edit the tabs as appropriate for the setup you want
- Export each tab as CSV:

| Spreadsheet Tab   | Filename           |
| ---               |  ---               |
| `SC2Commands`     | `commands.csv`     |
| `SC2CommandCodes` | `commandcodes.csv` |
| `SC2Hotkeys`      | `hotkeys.csv`      |
| `SC2HotkeyCodes`  | `hotkeycodes.csv`  |


### Make a new Hotkey file
- (one-time only) Clone and setup this repo (See: [Setup](#setup) below)
- `./csv2hotkeys.py -C commandcodes.csv -c commands.csv -K hotkeycodes.csv -k hotkeys.csv > autogen.SC2Hotkeys`

# Setup
- `git clone https://github.com/andylytical/sc2hotkeys.git`
- `cd sc2hotkeys/`
- `bash setup.sh`

# References
This work was inspired by and heavily influenced by:
- [The Core](https://drive.google.com/drive/folders/1ui2HNwaUa4FkHzRwATgXHNVEpolLNOz)
  - Especially
    [TheCore 6.0 Spreadsheet - An account of all important keys and their bindings](https://docs.google.com/spreadsheets/d/1CiJwE46S_Kt_ZkVNyXnrjMD15ZSZlv3JSG8nkpjHHtc)
