@echo off
echo Exemplos de uso do Conversor de Video
echo.
echo Conversao simples TS para MP4:
python video_converter.py input.ts -o output.mp4
echo.
echo Conversao otimizada TS para MP4:
python video_converter.py input.ts -o output.mp4 --ts-optimized
echo.
echo Conversao para audio:
python video_converter.py input.ts --audio-only -f mp3
echo.
echo Conversao em lote:
python video_converter.py pasta_videos\ --batch -f mp4
echo.
echo Conversao com qualidade alta:
python video_converter.py input.ts -q high -r 1920x1080
pause