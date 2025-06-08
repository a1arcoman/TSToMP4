import subprocess
import sys
import os

def install_requirements():
    """Instala as dependências necessárias"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✓ Dependências instaladas com sucesso!")
    except subprocess.CalledProcessError:
        print("✗ Erro ao instalar dependências")
        return False
    return True

def check_ffmpeg():
    """Verifica se o FFmpeg está instalado"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        print("✓ FFmpeg encontrado!")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ FFmpeg não encontrado!")
        print("\nPara instalar o FFmpeg:")
        print("1. Windows: Baixe de https://ffmpeg.org/download.html")
        print("2. Ou use chocolatey: choco install ffmpeg")
        print("3. Ou use winget: winget install FFmpeg")
        return False

if __name__ == "__main__":
    print("Configurando o Conversor de Vídeo...")
    
    if install_requirements():
        if check_ffmpeg():
            print("\n🎉 Configuração concluída! Você pode usar o conversor agora.")
        else:
            print("\n⚠️  Instale o FFmpeg para usar o conversor.")
    else:
        print("\n❌ Falha na configuração.")