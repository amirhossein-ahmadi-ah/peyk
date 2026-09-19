@ECHO OFF
SET SPHINXBUILD=sphinx-build
SET SOURCEDIR=.
SET BUILDDIR=_build

IF "%1" == "" GOTO html
IF "%1" == "clean" GOTO clean
GOTO help

:html
%SPHINXBUILD% -W -b html %SOURCEDIR% %BUILDDIR%/html
GOTO end

:clean
rmdir /S /Q %BUILDDIR% 2>NUL
GOTO end

:help
ECHO Usage: make.bat [html^|clean]

:end
