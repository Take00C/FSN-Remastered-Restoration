"""Fate/stay night REMASTERED - cut content restoration patcher.

    python fsn_restore.py --ue "<Ultimate Edition folder>" install [--cg original|demosaic]
    python fsn_restore.py restore
    python fsn_restore.py status

Options (before the command):
    --ue    your Fate/stay night Realta Nua Ultimate Edition v1.1.4 folder (needed for install/build)
    --game  the remaster folder (default: the standard Steam location)
    --work  where backups, caches and builds are kept (default: ./work next to this file)
The --ue/--game/--work values are remembered in work/settings.json after the first run.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_WORK = os.path.join(HERE, "work")


def main():
    args, rest = sys.argv[1:], []
    opts = {}
    i = 0
    while i < len(args):
        if args[i] in ("--ue", "--game", "--work") and i + 1 < len(args):
            opts[args[i][2:]] = os.path.abspath(args[i + 1])
            i += 2
        else:
            rest.append(args[i])
            i += 1
    work = opts.get("work") or DEFAULT_WORK
    settings_path = os.path.join(work, "settings.json")
    saved = json.load(open(settings_path, encoding="utf-8")) if os.path.exists(settings_path) else {}
    saved.update(opts)
    saved["work"] = work
    os.makedirs(work, exist_ok=True)
    json.dump(saved, open(settings_path, "w", encoding="utf-8"), indent=2)
    os.environ["FSNR_WORK"] = work
    if saved.get("ue"):
        os.environ["FSNR_UE"] = saved["ue"]
    if not saved.get("game"):  # find the Steam install the same way the launcher does
        try:
            sys.path.insert(0, HERE)
            from launcher import find_game
            found = find_game()
            if found:
                saved["game"] = found
                json.dump(saved, open(settings_path, "w", encoding="utf-8"), indent=2)
        except Exception:  # noqa: BLE001
            pass
    if saved.get("game"):
        os.environ["FSNR_GAME"] = saved["game"]
    sys.path.insert(0, os.path.join(HERE, "fsnr"))
    import restore  # noqa: E402  (reads the environment set above)
    if not rest:
        print(__doc__)
        return
    restore.main(rest)


if __name__ == "__main__":
    main()
