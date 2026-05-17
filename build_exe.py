import os
import sys
import subprocess
from PIL import Image
from build_config import APP_NAME, EXE_NAME, COMPANY_NAME, FILE_VERSION

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def main():
    print("=" * 60)
    print("   AUTO-BUILDER EXECUTÁVEL E ATALHO (WINDOWS)   ")
    print("=" * 60)
    print(f"Aplicativo: {APP_NAME}")
    print(f"Fornecedor configurado: {COMPANY_NAME}")
    print(f"Versão do arquivo: {FILE_VERSION}")

    images_dir = "images"
    raw_btc_path = os.path.join(images_dir, "bitcoin.png")

    ico_path = os.path.join(images_dir, "icon.ico")
    if os.path.exists(raw_btc_path):
        try:
            print("🎨 Convertendo logotipo original do Bitcoin para formato .ico...")
            img = Image.open(raw_btc_path)
            img.save(ico_path, format="ICO", sizes=[(128, 128), (64, 64), (32, 32), (16, 16)])
            print(f"✅ Ícone gerado com sucesso: {ico_path}")
        except Exception as e:
            print(f"⚠️ Falha ao criar o arquivo .ico a partir de {raw_btc_path}: {e}. PyInstaller usará ícone padrão.")
            ico_path = None
    else:
        print(f"⚠️ Logotipo original {raw_btc_path} não encontrado, compilando com ícone padrão.")
        ico_path = None

    print("📦 Instalando/Verificando dependência do PyInstaller...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ PyInstaller verificado/instalado.")
    except Exception as e:
        print(f"❌ Erro ao instalar o PyInstaller: {e}")
        sys.exit(1)

    print("🚀 Compilando executável GUI standalone com metadados de versão...")
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--noconfirm",
        "DominanciaCripto.spec",
    ]

    try:
        subprocess.run(cmd, check=True)
        print("\n✅ COMPILAÇÃO CONCLUÍDA COM SUCESSO!")
        exe_path = os.path.abspath(os.path.join("dist", f"{EXE_NAME}.exe"))
        print(f"💾 Executável criado em: {exe_path}")
    except Exception as e:
        print(f"❌ Erro durante o processo de compilação: {e}")
        sys.exit(1)

    print("\n🔗 Criando atalho na sua Área de Trabalho (Desktop)...")
    try:
        working_dir = os.path.abspath(".")
        desktop_dir = os.path.expandvars(r"%USERPROFILE%\Desktop")
        shortcut_path = os.path.join(desktop_dir, f"{APP_NAME}.lnk")

        powershell_script = f"""
        $WshShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut('{shortcut_path}')
        $Shortcut.TargetPath = '{exe_path}'
        $Shortcut.WorkingDirectory = '{working_dir}'
        $Shortcut.Save()
        """

        subprocess.run(["powershell", "-Command", powershell_script], check=True)
        print("🎉 ATALHO CRIADO COM SUCESSO!")
        print(f"📌 Nome do atalho: {APP_NAME}.lnk")
        print(f"📂 Aponta para: {exe_path}")
        print("=" * 60)

    except Exception as e:
        print(f"⚠️ Não foi possível criar o atalho de Área de Trabalho automaticamente: {e}")
        print(f"Você pode criar o atalho manualmente clicando com o botão direito em dist/{EXE_NAME}.exe -> Enviar para -> Área de Trabalho.")
        print("=" * 60)

if __name__ == "__main__":
    main()
