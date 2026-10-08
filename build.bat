@echo off
rem Builds "dist\FSN Restoration Launcher.exe" (single file, no Python needed to run it).
cd /d "%~dp0"
python -m pip install --upgrade pillow soundfile numpy pyinstaller || goto :fail
python -m PyInstaller --noconfirm --clean --onefile --windowed --name "FSN Restoration Launcher" ^
  --paths fsnr ^
  --hidden-import=config --hidden-import=keys --hidden-import=fpd --hidden-import=epk ^
  --hidden-import=xp3 --hidden-import=krtext --hidden-import=resolve_ue --hidden-import=convert_scene ^
  --hidden-import=merge_scene --hidden-import=build_all --hidden-import=make_cgs --hidden-import=ue_gallery ^
  --hidden-import=dec_all_epk --hidden-import=verify_build --hidden-import=restore ^
  --collect-all soundfile ^
  launcher.py || goto :fail
echo.
echo Built: dist\FSN Restoration Launcher.exe
pause
exit /b 0
:fail
echo Build failed.
pause
exit /b 1
