@echo off
setlocal
cd /d "%~dp0.."

echo ========================================
echo NSOKISS OFFLINE - Database setup
echo ========================================

echo.
where mysql >nul 2>nul
if %errorlevel%==0 goto MYSQL_FOUND
where mariadb >nul 2>nul
if %errorlevel%==0 goto MARIADB_FOUND

echo [ERROR] mysql.exe or mariadb.exe was not found in PATH.
echo Install MariaDB/MySQL locally and add its bin directory to PATH.
pause
exit /b 1

:MYSQL_FOUND
set "DB_CLIENT=mysql"
goto IMPORT

:MARIADB_FOUND
set "DB_CLIENT=mariadb"

goto IMPORT

:IMPORT
set "SQL_FILE="
if exist "database\database.sql" set "SQL_FILE=database\database.sql"
if not defined SQL_FILE if exist "database.sql" set "SQL_FILE=database.sql"
if not defined SQL_FILE (
    echo [ERROR] database.sql was not found.
    echo Put the supplied reference SQL file at database\database.sql.
    pause
    exit /b 1
)

echo Importing %SQL_FILE% into the local MariaDB/MySQL server...
%DB_CLIENT% -h 127.0.0.1 -P 3306 -u root < "%SQL_FILE%"
if errorlevel 1 (
    echo.
    echo [ERROR] Database import failed.
    pause
    exit /b 1
)

echo.
echo [OK] Database import completed.
echo Database name from the reference dump: nsotien_0
pause
exit /b 0
