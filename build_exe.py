import subprocess
import sys
import os
from pathlib import Path

def install_pyinstaller():
    """Instalar PyInstaller se não estiver disponível"""
    try:
        import PyInstaller
        print("✅ PyInstaller já está instalado")
        return True
    except ImportError:
        print("📦 Instalando PyInstaller...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
            print("✅ PyInstaller instalado com sucesso")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao instalar PyInstaller: {e}")
            return False

def build_executable():
    """Construir o executável"""
    print("🔨 Construindo executável...")
    
    # Comando PyInstaller
    cmd = [
        'pyinstaller',
        '--onefile',                    # Arquivo único
        '--windowed',                   # Sem console (GUI)
        '--name=VideoConverter',        # Nome do executável
        '--icon=icon.ico',             # Ícone (se existir)
        '--add-data=video_converter.py;.',  # Incluir módulo
        '--hidden-import=tkinterdnd2',  # Importação oculta
        '--hidden-import=PIL',          # Importação oculta
        '--hidden-import=cv2',          # Importação oculta
        'video_converter_gui_final.py'  # Arquivo principal
    ]
    
    # Remover --icon se não existir
    if not os.path.exists('icon.ico'):
        cmd = [c for c in cmd if not c.startswith('--icon')]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Executável criado com sucesso!")
        print("📁 Localização: dist/VideoConverter.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar executável: {e}")
        return False
    except FileNotFoundError:
        print("❌ PyInstaller não encontrado. Execute: pip install pyinstaller")
        return False

def main():
    print("🚀 Gerador de Executável - Video Converter")
    print("=" * 50)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists('video_converter_gui_final.py'):
        print("❌ Arquivo video_converter_gui_final.py não encontrado!")
        print("   Execute este script no diretório do projeto.")
        return
    
    if not os.path.exists('video_converter.py'):
        print("❌ Arquivo video_converter.py não encontrado!")
        return
    
    # Instalar PyInstaller
    if not install_pyinstaller():
        return
    
    # Construir executável
    if build_executable():
        print("\n🎉 Processo concluído!")
        print("\n📋 Próximos passos:")
        print("   1. Teste o executável: dist/VideoConverter.exe")
        print("   2. Para debug: VideoConverter.exe --debug")
        print("   3. Distribua o arquivo .exe")
    else:
        print("\n❌ Falha na criação do executável")

if __name__ == "__main__":
    main()