"""Fate/stay night REMASTERED - Restoration Launcher.

Before each start it asks how you want to play (restored 2004 content on/off, original or
demosaiced CGs), puts the matching files in place and starts the game through Steam.

Can also be used as a Steam launch option so Steam's own Play button shows it:
    "C:\\path\\to\\FSN Restoration Launcher.exe" %command%
"""
import json
import os
import queue
import re
import subprocess
import sys
import threading
import time
import traceback

APP_NAME = "FSN Restoration"
APP_ID = "2396980"
GAME_EXE = "fsn2-win64vc14-release.exe"
WORK = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "FSNRestoration")
SETTINGS = os.path.join(WORK, "settings.json")


# ---------------------------------------------------------------- detection
def _reg(root, path, name):
    try:
        import winreg
        with winreg.OpenKey(root, path) as k:
            return winreg.QueryValueEx(k, name)[0]
    except OSError:
        return None


def find_game():
    """Locate the remaster through Steam's own library list (a real Steam install of app 2396980)."""
    import winreg
    steam = _reg(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam", "SteamPath") or \
        _reg(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam", "InstallPath")
    if not steam:
        return None
    libs = [os.path.normpath(steam)]
    vdf = os.path.join(steam, "steamapps", "libraryfolders.vdf")
    if os.path.exists(vdf):
        libs += [os.path.normpath(p.replace("\\\\", "\\")) for p in re.findall(r'"path"\s+"([^"]+)"', open(vdf, encoding="utf-8", errors="ignore").read())]
    for lib in dict.fromkeys(libs):
        acf = os.path.join(lib, "steamapps", f"appmanifest_{APP_ID}.acf")
        if os.path.exists(acf):
            m = re.search(r'"installdir"\s+"([^"]+)"', open(acf, encoding="utf-8", errors="ignore").read())
            if m:
                d = os.path.join(lib, "steamapps", "common", m.group(1))
                if os.path.exists(os.path.join(d, GAME_EXE)):
                    return d
    return None


def looks_like_ue(d):
    return d and all(os.path.exists(os.path.join(d, f)) for f in ("patch.xp3", "patch_h.xp3", "patch_hd_1920.xp3"))


def find_ue():
    """Look for the Realta Nua Ultimate Edition: Windows uninstall entries, then common folders."""
    import winreg
    for root in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
        for base in (r"Software\Microsoft\Windows\CurrentVersion\Uninstall",
                     r"Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"):
            try:
                with winreg.OpenKey(root, base) as k:
                    for i in range(winreg.QueryInfoKey(k)[0]):
                        sub = winreg.EnumKey(k, i)
                        name = _reg(root, base + "\\" + sub, "DisplayName") or ""
                        if "ultimate" in name.lower() and ("fate" in name.lower() or "realta" in name.lower() or "réalta" in name.lower()):
                            loc = _reg(root, base + "\\" + sub, "InstallLocation")
                            if looks_like_ue(loc):
                                return loc
            except OSError:
                pass
    home = os.path.expanduser("~")
    roots = [os.path.join(home, x) for x in ("Downloads", "Desktop", "Documents", "Games")]
    roots += [os.environ.get("ProgramFiles", r"C:\Program Files"), os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")]
    roots += [f"{d}:\\" for d in "CDEFG" if os.path.exists(f"{d}:\\")]
    for r in roots:
        try:
            for name in os.listdir(r):
                d = os.path.join(r, name)
                if os.path.isdir(d) and ("fate" in name.lower() or "fsn" in name.lower() or "realta" in name.lower()):
                    if looks_like_ue(d):
                        return d
                    try:  # one level deeper
                        for n2 in os.listdir(d):
                            if looks_like_ue(os.path.join(d, n2)):
                                return os.path.join(d, n2)
                    except OSError:
                        pass
        except OSError:
            pass
    return None


# ---------------------------------------------------------------- settings
def load_settings():
    try:
        return json.load(open(SETTINGS, encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_settings(s):
    os.makedirs(WORK, exist_ok=True)
    json.dump(s, open(SETTINGS, "w", encoding="utf-8"), indent=2, ensure_ascii=False)


_ENGINE_PATHS = None


class PathsChanged(Exception):
    """The engine modules were already loaded with other folders; the launcher must restart."""


def init_engine(game, ue):
    """Load the engine for these folders. The engine reads its folders once at import time, so a
    different pair of folders in the same process means: restart the launcher (PathsChanged)."""
    global _ENGINE_PATHS
    if _ENGINE_PATHS is not None and _ENGINE_PATHS != (game, ue or ""):
        raise PathsChanged()
    os.environ["FSNR_WORK"] = WORK
    os.environ["FSNR_GAME"] = game
    os.environ["FSNR_UE"] = ue or ""
    here = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(here, "fsnr"))
    sys.path.insert(0, here)
    import restore
    _ENGINE_PATHS = (game, ue or "")
    return restore


def relaunch():
    """Start a fresh launcher process (same arguments) and let this one exit."""
    rest = [a for a in sys.argv[1:] if a != "--autoplay"]
    if getattr(sys, "frozen", False):
        args = [sys.executable, "--autoplay"] + rest
    else:
        args = [sys.executable, os.path.abspath(__file__), "--autoplay"] + rest
    subprocess.Popen(args)


HANDOFF = os.path.join(WORK, "handoff.json")  # "we just started Steam ourselves"


def start_game(command):
    if command:  # launched by Steam as a launch option: run the game command we were given
        subprocess.Popen(command, cwd=os.path.dirname(command[0]) or None)
    else:
        # if the user also set the launcher as Steam's launch option, Steam will start us again
        # with %command%; the handoff marker makes that second start skip the window
        try:
            os.makedirs(WORK, exist_ok=True)
            json.dump({"time": time.time()}, open(HANDOFF, "w"))
        except OSError:
            pass
        os.startfile(f"steam://rungameid/{APP_ID}")


def just_handed_off():
    try:
        t0 = json.load(open(HANDOFF))["time"]
        os.remove(HANDOFF)
        return time.time() - t0 < 120
    except (OSError, ValueError, KeyError):
        return False


# ---------------------------------------------------------------- UI
class Launcher:
    def __init__(self, command):
        import tkinter as tk
        from tkinter import ttk
        self.tk, self.ttk = tk, ttk
        self.command = command
        self.s = load_settings()
        self.root = tk.Tk()
        self.root.title(APP_NAME)
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.resizable(False, False)
        self.q = queue.Queue()
        self.busy = False
        self.engine = None

        pad = {"padx": 12, "pady": 4}
        f = ttk.Frame(self.root, padding=12)
        f.grid()
        ttk.Label(f, text="Fate/stay night REMASTERED", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=3, sticky="w")
        ttk.Label(f, text="2004 cut content restoration").grid(row=1, column=0, columnspan=3, sticky="w", pady=(0, 8))

        ttk.Label(f, text="Game (Steam):").grid(row=2, column=0, sticky="w")
        self.game_var = tk.StringVar(value=self.s.get("game") or find_game() or "")
        ttk.Label(f, textvariable=self.game_var, width=58).grid(row=2, column=1, sticky="w")
        ttk.Button(f, text="Browse…", command=self.browse_game).grid(row=2, column=2, **pad)

        ttk.Label(f, text="Content source:").grid(row=3, column=0, sticky="w")
        self.ue_var = tk.StringVar(value=self.s.get("ue") or "")
        ttk.Label(f, textvariable=self.ue_var, width=58).grid(row=3, column=1, sticky="w")
        ttk.Button(f, text="Browse…", command=self.browse_ue).grid(row=3, column=2, **pad)
        ttk.Label(f, text="(your Fate/stay night [Réalta Nua] Ultimate Edition folder)", foreground="#666").grid(row=4, column=1, sticky="w")

        box = ttk.LabelFrame(f, text="How do you want to play?", padding=10)
        box.grid(row=5, column=0, columnspan=3, sticky="we", pady=10)
        self.mode = tk.StringVar(value=self.s.get("choice", "original"))
        ttk.Radiobutton(box, text="Restored 2004 content — original CGs (mosaic)", variable=self.mode, value="original").grid(sticky="w")
        ttk.Radiobutton(box, text="Restored 2004 content — uncensored CGs (fan demosaic)", variable=self.mode, value="demosaic").grid(sticky="w")
        ttk.Radiobutton(box, text="Off — play the unmodified remaster", variable=self.mode, value="off").grid(sticky="w")
        ckbox = ttk.Frame(box)
        ckbox.grid(sticky="w", pady=(8, 0))
        ttk.Label(ckbox, text="Chinese mode (中文模式): restored lines have no Chinese translation; show them in\n"
                              "恢复的内容没有中文翻译，显示为：").grid(row=0, column=0, columnspan=2, sticky="w")
        self.ck = tk.StringVar(value=self.s.get("ck", "ja"))
        ttk.Radiobutton(ckbox, text="Japanese 日本語", variable=self.ck, value="ja").grid(row=1, column=0, sticky="w")
        ttk.Radiobutton(ckbox, text="English 英语", variable=self.ck, value="en").grid(row=1, column=1, sticky="w", padx=12)
        self.ask = tk.BooleanVar(value=self.s.get("ask", True))
        ttk.Checkbutton(f, text="Ask me every time I start the game", variable=self.ask).grid(row=6, column=0, columnspan=3, sticky="w")

        bar = ttk.Frame(f)
        bar.grid(row=7, column=0, columnspan=3, sticky="we", pady=(10, 4))
        self.play_btn = ttk.Button(bar, text="▶  Play", command=self.play)
        self.play_btn.pack(side="right")
        self.quit_btn = ttk.Button(bar, text="Quit", command=self.close)
        self.quit_btn.pack(side="right", padx=8)
        self.progress = ttk.Progressbar(f, mode="indeterminate", length=560)
        self.progress.grid(row=8, column=0, columnspan=3, sticky="we")
        self.log = tk.Text(f, height=9, width=80, state="disabled", font=("Consolas", 9))
        self.log.grid(row=9, column=0, columnspan=3, pady=(6, 0))

        if not self.ue_var.get():
            self.write("Looking for your Ultimate Edition folder…\n")
            self.root.after(100, self.autodetect_ue)
        if not self.game_var.get():
            self.write("Fate/stay night REMASTERED was not found in your Steam libraries.\n")
        self.root.after(100, self.pump)

    # ---- helpers
    def close(self):
        from tkinter import messagebox
        if self.busy:
            messagebox.showinfo(APP_NAME, "Please wait until the current step has finished.")
            return
        self.root.destroy()

    def write(self, text):
        self.log.configure(state="normal")
        self.log.insert("end", text)
        self.log.see("end")
        self.log.configure(state="disabled")

    def pump(self):
        try:
            while True:
                kind, val = self.q.get_nowait()
                if kind == "log":
                    self.write(val)
                elif kind == "done":
                    self.finish(val)
        except queue.Empty:
            pass
        self.root.after(100, self.pump)

    def autodetect_ue(self):
        d = find_ue()
        if d:
            self.ue_var.set(d)
            self.write(f"Found: {d}\n")
        else:
            self.write("Not found automatically — use Browse… to select it.\n")

    def browse_game(self):
        from tkinter import filedialog, messagebox
        d = filedialog.askdirectory(title="Select the Fate/stay night REMASTERED folder (contains fsn2-win64vc14-release.exe)")
        if d:
            if os.path.exists(os.path.join(d, GAME_EXE)):
                self.game_var.set(os.path.normpath(d))
            else:
                messagebox.showerror(APP_NAME, "That folder does not contain the game.")

    def browse_ue(self):
        from tkinter import filedialog, messagebox
        d = filedialog.askdirectory(title="Select your Realta Nua Ultimate Edition folder (contains patch_h.xp3)")
        if d:
            if looks_like_ue(d):
                self.ue_var.set(os.path.normpath(d))
            else:
                messagebox.showerror(APP_NAME, "That folder is not an Ultimate Edition v1.1.4 install (patch_h.xp3 / patch_hd_1920.xp3 missing).")

    # ---- actions
    def play(self):
        from tkinter import messagebox
        if self.busy:
            return
        game, ue, choice, ck = self.game_var.get(), self.ue_var.get(), self.mode.get(), self.ck.get()
        if not game:
            messagebox.showerror(APP_NAME, "Fate/stay night REMASTERED (Steam) was not found. Use Browse… next to Game.")
            return
        if choice != "off" and not looks_like_ue(ue):
            messagebox.showerror(APP_NAME, "Select your Réalta Nua Ultimate Edition folder first (Browse… next to Content source).")
            return
        self.s.update({"game": game, "ue": ue, "choice": choice, "ck": ck, "ask": self.ask.get()})
        save_settings(self.s)
        self.busy = True
        self.play_btn.configure(state="disabled")
        self.quit_btn.configure(state="disabled")
        self.progress.start(12)
        threading.Thread(target=self.work, args=(game, ue, choice, ck), daemon=True).start()

    def work(self, game, ue, choice, ck):
        q = self.q

        class W:
            def write(self, t):
                q.put(("log", t))

            def flush(self):
                pass
        sys.stdout = sys.stderr = W()
        try:
            run_choice(game, ue, choice, ck)
            q.put(("done", None))
        except PathsChanged:
            q.put(("done", "__relaunch__"))
        except SystemExit as ex:
            q.put(("done", str(ex)))
        except Exception as ex:  # noqa: BLE001
            traceback.print_exc()
            q.put(("done", str(ex)))

    def finish(self, error):
        from tkinter import messagebox
        self.progress.stop()
        self.busy = False
        self.play_btn.configure(state="normal")
        self.quit_btn.configure(state="normal")
        if error == "__relaunch__":  # folders changed: continue in a fresh launcher process
            relaunch()
            self.root.destroy()
            return
        if error:
            messagebox.showerror(APP_NAME, error)
            return
        start_game(self.command)
        self.root.after(800, self.root.destroy)

    def run(self):
        self.root.mainloop()


def already_set(restore, choice, ck):
    if choice == "off":
        return restore.current() == "off"
    return restore.detect() == (choice, ck) and restore.cache_stamp() is not None


def run_choice(game, ue, choice, ck="ja"):
    restore = init_engine(game, ue)
    if already_set(restore, choice, ck):
        print(f"Game files already set ({choice}). Starting the game.")
        return
    if choice == "off":
        restore.go_off()  # keeps files that are already originals (new install, Steam update)
        print("Starting the unmodified game.")
        return
    restore.prepare()
    restore.ensure_built()
    restore.apply(choice, ck)
    print("Starting the game.")


def quick_start(command, s):
    """'Don't ask' mode: start straight away when the game files already match the saved choice.
    Anything that needs work (first build, a Steam update, a different choice) opens the window."""
    try:
        restore = init_engine(s["game"], s.get("ue", ""))
        choice = s.get("choice", "original")
        if already_set(restore, choice, s.get("ck", "ja")):
            start_game(command)
            return True
    except Exception:  # noqa: BLE001
        pass
    return False


def shift_held():
    try:
        import ctypes
        return bool(ctypes.windll.user32.GetAsyncKeyState(0x10) & 0x8000)
    except Exception:  # noqa: BLE001
        return False


def main():
    import multiprocessing
    multiprocessing.freeze_support()
    autoplay = "--autoplay" in sys.argv[1:]
    command = [a for a in sys.argv[1:] if a != "--autoplay"]
    command = command if command and command[0].lower().endswith(".exe") else []
    s = load_settings()
    if command and just_handed_off():  # second start by Steam right after we started it
        start_game(command)
        return
    if s.get("game") and not s.get("ask", True) and not shift_held():
        if quick_start(command, s):
            return
    app = Launcher(command)
    if autoplay:  # restarted after a folder change: continue with Play right away
        app.root.after(500, app.play)
    app.run()


if __name__ == "__main__":
    main()
