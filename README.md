Remap an existing SC2Hotkeys file with a given substitution map.

# Usage
## Setup
- `git clone https://github.com/andylytical/sc2hotkeys.git`
- `bash setup.sh`
## Create Custom Mapping
An adjustment of keys from source to target (ie: swap 4 and 0)
- `cp Keymaps/same Keymaps/my-custom-map`
- `vim Keymaps/my-custom-map`
## Make a new Hotkey file
Apply the swaps from custom map to the source hotkey file, print out the new hotkey setup.
- `./mk_keymap.py -h`
- `./mk_keymap.py -k Keymaps/core6g_US_right-to-xbows SC2Hotkeys/TheCore6g_right_US_qwerty.SC2Hotkeys >SC2Hotkeys/core6g_xbows_01.SC2Hotkeys`

## Add Custom Overrides
Override file format is same as SC2Hotkeys file.
Hotkeys listed here will directly replace the given hotkey from the source file.
Print the new hotkey setup.
- `grep '^\[\|BuildAdvanced' SC2Hotkeys/core6g_xbows >override`
- Make custom changes to override file
  - `vim override`
- `./mk_keymap.py -o override SC2Hotkeys/core6g_xbows_01.SC2Hotkeys >SC2Hotkeys/core6g_xbows_02.SC2Hotkeys`

## Keymap and Overrides can be applied together
If both `-k` and `-o` are provided, keymap is applied first, then overrides are applied second. 
- `./mk_keymap.py -k Keymaps/core6g_US_right-to-xbows -o override SC2Hotkeys/TheCore6g_right_US_qwerty.SC2Hotkeys >SC2Hotkeys/core6g_xbows.SC2Hotkeys`

# References
- https://gist.github.com/pedz/3ab6b1aa7fb4f41b354a7a82f5ba522b
