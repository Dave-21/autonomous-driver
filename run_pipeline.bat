@echo off
echo ===================================
echo   Running Local Agent Pipeline
echo ===================================

:: Pull upstream remote changes before execution
git pull --rebase origin main

python src\agent.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Agent execution failed! Aborting commit.
    exit /b %ERRORLEVEL%
)

echo.
echo Running Verification Guardrails...
python -m pytest tests/
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Pytest guardrail failed! Aborting commit.
    exit /b %ERRORLEVEL%
)

echo.
echo [SUCCESS] Guardrails passed. Staging artifacts...
set /p COMMIT_MSG=<.commit_msg.tmp

git add .
git commit -m "%COMMIT_MSG%"
git pull --rebase origin main
git push origin main

if exist .commit_msg.tmp del .commit_msg.tmp

echo ===================================
echo   Automated Pipeline Run Complete!
echo ===================================