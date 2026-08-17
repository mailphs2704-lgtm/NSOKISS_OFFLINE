@echo off
setlocal
cd /d "%~dp0"

echo ========================================
echo        NSOKISS OFFLINE SERVER
echo ========================================
echo.

if not exist "config.properties" (
    echo [ERROR] Khong tim thay config.properties
    pause
    exit /b 1
)

if not exist "target\Nso-jar-with-dependencies.jar" (
    echo [INFO] Chua co file server da build.
    echo [INFO] Dang build bang Maven...
    call mvn -q -DskipTests package
    if errorlevel 1 (
        echo.
        echo [ERROR] Build that bai. Kiem tra Java va Maven.
        pause
        exit /b 1
    )
)

echo [INFO] Dang khoi dong server local...
echo [INFO] Database: 127.0.0.1:3306/nso
echo [INFO] Game port: 14444
echo.

java -server -Dfile.encoding=UTF-8 -Xms1G -Xmx2G -jar "target\Nso-jar-with-dependencies.jar"

pause
