# Fate/stay night REMASTERED: Cut Content Restoration

A launcher that restores the content cut from the 2004 release into **Fate/stay night REMASTERED** (Steam). Each time you start it, it asks how you want to play:

- **Restored 2004 content, original CGs** (as released in 2004, with mosaic)
- **Restored 2004 content, uncensored CGs** (the Ultimate Edition's fan demosaic)
- **Off:** the unmodified remaster

It puts the matching files in place, then starts the game through Steam. Switching takes a few seconds.

> ⚠️ **18+:** this restores the adult scenes of the original 2004 release, as well as violent and gory content that Réalta Nua toned down.

## What you need

1. **Fate/stay night REMASTERED** on Steam (game version 1.4.2.391). The launcher finds it automatically through Steam.
2. **Fate/stay night [Réalta Nua] Ultimate Edition v1.1.4,** installed. This is where the restored scenes, CGs and voices come from. **This download contains no game content;** everything is built on your PC from your own copies. The launcher looks for the Ultimate Edition folder automatically. If it isn't found, click **Browse…** and pick the folder that contains `patch_h.xp3`.
3. About **5 GB of free disk space** for backups and the prepared files.
4. An internet connection the first time, to fetch one key file (see *How it works*).

You don't need Python, extra tools or the command line.

## How to use

1. Download **`FSN Restoration Launcher.exe`** from the Releases page and put it anywhere.
2. Run it. Windows may show a SmartScreen warning because the program isn't code-signed: click **More info → Run anyway**.
3. Check that both folders were found. Choose how you want to play and click **▶ Play**.
   - The **first time**, it takes a few minutes. It backs up the original game files, then prepares both CG versions.
   - After that, starting or switching takes seconds.
4. Start the game with the launcher from then on.

### Tips

- **Untick "Ask me every time I start the game"** to start straight away with your last choice. Hold **Shift** while opening the launcher to see the options again.
- **To use Steam's own Play button,** set the game's launch option in Steam (right-click the game → Properties → Launch Options) to the line below, with your own path:
  ```
  "C:\path\to\FSN Restoration Launcher.exe" %command%
  ```
- **To go back to the unmodified game,** choose **Off** and click Play. Steam's **Verify integrity of game files** also restores the originals.
- **To remove everything,** choose **Off** once, then delete the launcher and the folder `%LOCALAPPDATA%\FSNRestoration`.
- **After a Steam update,** just use the launcher as usual. It detects the update, backs up the new files and prepares everything again.

## What it restores

- **8 full 2004 scenes** replacing their Réalta Nua versions:
  - 18+ scenes in all three routes.
  - The gore version of HF Day 14 scene 10.
  - Where Réalta Nua merged two 2004 scenes, both play back to back again.
- **Cut content inside 173 more scenes**: 18+ passages, nudity and ecchi text, and the violence and gore Réalta Nua softened. Every line that wasn't cut keeps the remaster's official Japanese, English and Chinese text.
- **85 CGs.** The full 4:3 art is shown uncropped in the widescreen frame, with blurred sides.
- **CG gallery:** 28 new slots (56 images) in the Fate, UBW and HF galleries. They unlock when seen in the story.
- **Scene replay:** restored scenes replay in their restored form.
- **Audio:** 7 voice clips and 2 sound effects the remaster lacks.
- **Achievements, saves and progress:**
  - Every remaster achievement and unlock trigger is preserved. Builds that would lose one are refused.
  - Unchanged lines keep the remaster's own line IDs, so your saves stay valid.

Japanese is the primary target: restored Japanese text is the original 2004 script. Restored lines in English use the Mirror Moon translation that ships with the Ultimate Edition.

**Chinese:** no Chinese translation of the restored 2004 content exists, so Chinese-mode players see restored lines in **Japanese** or **English**. Choose which in the launcher (中文模式). Everything else keeps the official Chinese text, including every line of a restored scene that is identical to the remaster's own.

## Known limitations

- **Song 「抱擁2」 (`bgm33`):** this 2004 track plays as 「抱擁」 (`bgm40`). The remaster's BGM player only accepts its own encrypted audio format.
- **One silent voice line:** `sak1115_sak_0060` has no recording in any source.
- **Two achievements fire at scene end:** 0008 and 0013 sit in fully replaced scenes, so they now unlock at the end of those scenes rather than mid-scene.
- **No in-game uncensor switch:** the remaster has no mod menu, so the CG choice lives in the launcher instead.
- **Game version:** built and tested on game version 1.4.2.391.

## How it works

- **Files touched:** the launcher only rebuilds `obb\patch00m.bin` (scripts and text) and `obb\patch01d.bin` (images and audio). The originals are backed up in `%LOCALAPPDATA%\FSNRestoration\backup-obb`, and the launcher never adopts one of its own builds as an "original".
- **Restoring the content:** the Ultimate Edition's conditional scripts are resolved twice, once with Réalta Nua text and once with the restored content. Only the differences are merged, page by page, into the remaster's own scripts.
- **The two decryption keys:**
  - The epk key table is read from your game executable.
  - The pack key is generated by the game at runtime, so it is downloaded once from the public [FSNr_tools](https://github.com/kurikomoe/FSNr_tools) repository. The download is pinned to one commit and SHA-256 checked.
- **Checks:** every build is verified before use. Each text line must exist in all three languages, every image and sound must exist, every command must be one the remaster knows, and no achievement or progress command may be lost.

## Building from source

Install Python 3.10+, then run `build.bat`. It installs the build dependencies (Pillow, soundfile and PyInstaller) and writes `dist\FSN Restoration Launcher.exe`.

For advanced users, there's also a command-line version:

```bash
python fsn_restore.py --ue "<Ultimate Edition folder>" install --cg original
```

Replace `install` with `restore` or `status` for those commands.

## Credits

- **TYPE-MOON:** Fate/stay night. Please support the official release.
- **The Fate/stay night [Réalta Nua] Ultimate Edition team:** Jacktheinfinite101, Quibi, Kotonoha and everyone credited in their readme.
- **Mirror Moon:** the English translation used for restored lines.
- **Fan demosaic artists:** Bellandy and the others credited by the Ultimate Edition.
- **[kurikomoe/FSNr_tools](https://github.com/kurikomoe/FSNr_tools):** the REMASTERED pack and epk formats and the decryption keys. `fsnr/fpd.py` and `fsnr/epk.py` are based on that work.
- **[DaZombieKiller/FatePackageManager](https://github.com/DaZombieKiller/FatePackageManager):** pack format research.

**AI disclosure:** this launcher was built by an AI coding agent, Claude Code (Claude Opus 5.5, Anthropic), working with and directed by the publisher. The agent:
- reverse-engineered the formats,
- wrote the code, and
- verified the results in the real game (CG placement with test patterns, audio by recording the game's output).

No AI-generated art or audio is included or produced.

## License

The code is released under the MIT License (see `LICENSE`). See `THIRD_PARTY.md` for the parts based on other people's work. Fate/stay night and all game content belong to TYPE-MOON. This project is unofficial and not affiliated with TYPE-MOON, Aniplex or the Ultimate Edition team.
