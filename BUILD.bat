@echo off
REM ===== Build IDE with Nuitka =====

python -m nuitka --standalone --windows-console-mode=disable --enable-plugin=tk-inter CYeditor.py

echo.
echo Build finished!
pause