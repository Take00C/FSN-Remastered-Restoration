# Third-party notices

## kurikomoe/FSNr_tools
https://github.com/kurikomoe/FSNr_tools

- `fsnr/fpd.py`: the FPD (`obb/*.bin`) reader follows `scripts/dec.py` from FSNr_tools. Its 56-byte header, big-endian entry table and XOR stream are as documented there.
- `fsnr/epk.py`: a Python port of the `.epk` cipher from FSNr_tools `main.cpp` / `include/*.h`. That cipher is a Blowfish variant with a custom P-array; the S-boxes come from the game executable, and each file is keyed by its own name.
- `fsnr/keys.py`: downloads `scripts/decryptKey.bin` from FSNr_tools at commit `30c277be34c4a68aff9a7c2602579af7d118d259`, checked by SHA-256. The key is not redistributed here.

At the time of writing, FSNr_tools does not include a license file. These parts are credited to its author. If you publish this project, ask the author first, and follow any terms they set.

## Fate/stay night [Réalta Nua] Ultimate Edition
Nothing from the Ultimate Edition is included. The patcher reads it from the user's own install at build time.

## TYPE-MOON
Fate/stay night and all game content (text, images, audio) are © TYPE-MOON. None of it is included in this repository.
