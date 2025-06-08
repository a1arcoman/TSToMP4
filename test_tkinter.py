import sys

def test_tkinter():
    """Testa se o tkinter está funcionando corretamente"""
    print("🧪 Testando tkinter...")
    
    try:
        import tkinter as tk
        print("✅ tkinter importado com sucesso")
        
        # Teste básico de criação de janela
        root = tk.Tk()
        root.title("Teste Tkinter")
        root.geometry("300x200")
        
        label = tk.Label(root, text="Tkinter funcionando!")
        label.pack(pady=50)
        
        button = tk.Button(root, text="Fechar", command=root.destroy)
        button.pack()
        
        print("✅ Janela de teste criada com sucesso")
        print("📝 Feche a janela para continuar...")
        
        root.mainloop()
        print("✅ Teste do tkinter concluído com sucesso!")
        return True
        
    except ImportError as e:
        print(f"❌ Erro ao importar tkinter: {e}")
        print("\n🔧 Soluções:")
        print("   1. Reinstale Python com tkinter incluído")
        print("   2. No Linux: sudo apt-get install python3-tk")
        return False
        
    except Exception as e:
        print(f"❌ Erro no teste do tkinter: {e}")
        return False

def test_tkinterdnd2():
    """Testa se o tkinterdnd2 está funcionando"""
    print("\n🧪 Testando tkinterdnd2...")
    
    try:
        from tkinterdnd2 import TkinterDnD
        print("✅ tkinterdnd2 importado com sucesso")
        
        # Teste básico
        root = TkinterDnD.Tk()
        root.withdraw()  # Esconder janela
        root.destroy()   # Destruir imediatamente
        
        print("✅ tkinterdnd2 funcionando corretamente")
        return True
        
    except ImportError:
        print("⚠️  tkinterdnd2 não disponível (opcional)")
        return False
        
    except Exception as e:
        print(f"⚠️  Problema com tkinterdnd2: {e}")
        print("   Drag-and-drop será desabilitado")
        return False

def main():
    print("🔍 DIAGNÓSTICO DO SISTEMA GUI")
    print("=" * 40)
    
    # Informações do sistema
    print(f"🐍 Python: {sys.version}")
    print(f"💻 Plataforma: {sys.platform}")
    
    # Teste tkinter
    tkinter_ok = test_tkinter()
    
    # Teste tkinterdnd2
    dnd_ok = test_tkinterdnd2()
    
    print("\n" + "=" * 40)
    print("📋 RESUMO DOS TESTES:")
    print(f"   🖼️  Tkinter: {'✅ OK' if tkinter_ok else '❌ ERRO'}")
    print(f"   🖱️  Drag-Drop: {'✅ OK' if dnd_ok else '⚠️  Desabilitado'}")
    
    if tkinter_ok:
        print("\n🎉 Sistema pronto para executar a GUI!")
        print("\n🚀 Execute: python video_converter_gui_lite.py")
    else:
        print("\n❌ Sistema não está pronto para GUI")
        print("   Corrija os problemas do tkinter primeiro")
    
    input("\n⏸️  Pressione Enter para sair...")

if __name__ == "__main__":
    main()