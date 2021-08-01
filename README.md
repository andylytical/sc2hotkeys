Remap an existing SC2Hotkeys file with a given substitution map.

# Usage
- `git clone https://github.com/andylytical/sc2hotkeys.git`
- `bash setup.sh`
- `cp Keymaps/same Keymaps/my-custom-map`
- `vim Keymaps/my-custom-map`
- `./mk_keymap.py -k Keymaps/core6g_US_right-to-xbows SC2Hotkeys/TheCore6g_right_US_qwerty.SC2Hotkeys SC2Hotkeys/core6g_xbows.SC2Hotkeys`

## Adding Direct Overrides
- `grep '^\[\|BuildAdvanced' SC2Hotkeys/core6g_xbows >override`
- Make custom changes to override file
  - `vim override`
- `./mk keymap.py -k Keymaps/core6g_US_right-to-xbows -o override SC2Hotkeys/TheCore6g_right_US_qwerty.SC2Hotkeys
  >SC2Hotkeys/core6g_xbows.SC2Hotkeys`
