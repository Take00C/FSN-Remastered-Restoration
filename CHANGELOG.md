# Changelog

## 1.3.1
- Fixed: after a patcher update, the launcher could keep the previous build installed because the game files looked unchanged. It now also checks that the installed files are the current build.
- Fixed: the game version is read from dep.dat (ver.dat only holds a build date), so the version warning no longer appears by mistake.
- Restored lines no longer carry Ultimate Edition-only command options the remaster never uses.

## 1.3.0
- Chinese (中文) mode: a launcher option chooses whether restored lines, which have no Chinese translation, show in Japanese or English. Switching is instant, because both are prepared.
- Full restored scenes now reuse the remaster's own line wherever the 2004 text is identical, so those lines keep the official Japanese, English and Chinese text. For example, HF Day 12 scene 13: 83 of 131 lines.
- English for the full scenes now handles pages where the translation merges or splits sentences.

## 1.2.0 (review fixes)
- **Fixed:** choosing **Off** after a Steam update or "Verify integrity" could put stale backups over the new game files. Files that are already originals are now kept, and adopted as the backup.
- **Fixed:** an interrupted first backup could later be restored as if it were complete. Backups, builds and settings are now all written atomically and verified by checksum. The window can't be closed while a step is running.
- **Fixed:** changing the game or Ultimate Edition folder after a failed attempt could keep using the old folders. The launcher now restarts itself and continues.
- **Fixed:** when set as Steam's launch option, starting the launcher directly could open it a second time.
- **Fixed:** an update that changes only the remaster's base scripts or game version now triggers a rebuild.
- **Fixed:** two restored English lines in HF Day 11 had shifted translations, caused by a page where the translation merges sentences. The English alignment now handles such pages.
- **Fixed:** a stale backlog index entry for the one silent voice line.
- Lower memory use while building, and no console windows flash from the windowed launcher.

## 1.1.0
- New: a single-file Windows launcher (`FSN Restoration Launcher.exe`). You don't need Python, ffmpeg or the command line.
- The launcher asks before every start: restored with original CGs, restored with uncensored CGs, or Off. Switching takes seconds.
- It finds the game through Steam's library list and auto-detects the Ultimate Edition folder.
- It can be used as a Steam launch option (`"…\FSN Restoration Launcher.exe" %command%`).
- Audio is no longer re-encoded: the UE voice files are used as-is, and the two WAV sound effects are encoded with the bundled libsndfile.

## 1.0.0
First release. Supports game version 1.4.2.391 with Réalta Nua Ultimate Edition v1.1.4.

- Restores 8 full 2004 scenes and the cut content inside 173 more scenes. The remaster's official text is kept everywhere else.
- Adds 85 restored CGs in two variants (`original` and `demosaic`), with in-game-measured placement.
- Adds 28 gallery slots (56 images) with thumbnails. Scene replay plays the restored scenes.
- Adds 7 voice clips and 2 sound effects. The BGM `bgm33` falls back to `bgm40`.
- Preserves every achievement and progress trigger, enforced by the build check.
- Backs up the originals and offers `restore`. It's safe across Steam updates and verify.
