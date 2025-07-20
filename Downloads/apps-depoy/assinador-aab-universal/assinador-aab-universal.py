import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os

def selecionar_keystore():
    caminho = filedialog.askopenfilename(
        title="Selecione o keystore",
        filetypes=[("Keystore", "*.keystore *.jks"), ("Todos os arquivos", "*.*")]
    )
    if not caminho:
        return

    nome = os.path.basename(caminho).lower()

    if nome == "android.keystore":
        alias_entry.delete(0, tk.END)
        alias_entry.insert(0, "androidkey")
        store_pass_entry.delete(0, tk.END)
        store_pass_entry.insert(0, "android")
        key_pass_entry.delete(0, tk.END)
        key_pass_entry.insert(0, "android")
        messagebox.showinfo("Keystore detectado", "Keystore do Kodular detectado.\nDados padrão preenchidos.\nVocê pode alterar se quiser.")

    keystore_entry.delete(0, tk.END)
    keystore_entry.insert(0, caminho)

def selecionar_aab():
    caminho = filedialog.askopenfilename(
        title="Selecione o arquivo .aab",
        filetypes=[("Android App Bundle", "*.aab"), ("Todos os arquivos", "*.*")]
    )
    if caminho:
        aab_entry.delete(0, tk.END)
        aab_entry.insert(0, caminho)

def assinar():
    keystore = keystore_entry.get()
    aab = aab_entry.get()
    alias = alias_entry.get()
    store_pass = store_pass_entry.get()
    key_pass = key_pass_entry.get()

    if not all([keystore, aab, alias, store_pass, key_pass]):
        messagebox.showerror("Erro", "Preencha todos os campos antes de assinar.")
        return

    status_label.config(text="🔄 Assinando...")
    progress_bar.grid()
    progress_bar.start(10)
    root.update_idletasks()

    comando = [
        "jarsigner",
        "-verbose",
        "-sigalg", "SHA256withRSA",
        "-digestalg", "SHA-256",
        "-keystore", keystore,
        "-storepass", store_pass,
        "-keypass", key_pass,
        aab,
        alias
    ]

    try:
        subprocess.run(comando, check=True)
        messagebox.showinfo("Sucesso", "✅ Arquivo AAB assinado com sucesso!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Erro", "❌ Falha ao assinar o arquivo.\nVerifique os dados e tente novamente.")
    finally:
        progress_bar.stop()
        progress_bar.grid_remove()
        status_label.config(text="")

# Interface gráfica
root = tk.Tk()
root.title("Assinador Universal de AAB")
root.resizable(False, False)

tk.Label(root, text="Alias da chave:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
alias_entry = tk.Entry(root, width=40)
alias_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Senha do keystore:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
store_pass_entry = tk.Entry(root, show="*", width=40)
store_pass_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Senha da chave:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
key_pass_entry = tk.Entry(root, show="*", width=40)
key_pass_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Keystore (.jks/.keystore):").grid(row=3, column=0, sticky="e", padx=5, pady=5)
keystore_entry = tk.Entry(root, width=40)
keystore_entry.grid(row=3, column=1, padx=5, pady=5)
tk.Button(root, text="Selecionar", command=selecionar_keystore).grid(row=3, column=2, padx=5, pady=5)

tk.Label(root, text="Arquivo .aab:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
aab_entry = tk.Entry(root, width=40)
aab_entry.grid(row=4, column=1, padx=5, pady=5)
tk.Button(root, text="Selecionar", command=selecionar_aab).grid(row=4, column=2, padx=5, pady=5)

tk.Button(root, text="Assinar AAB", command=assinar).grid(row=5, column=0, columnspan=3, pady=10)

status_label = tk.Label(root, text="", font=("Arial", 10), fg="blue")
status_label.grid(row=6, column=0, columnspan=3)

progress_bar = ttk.Progressbar(root, mode='indeterminate', length=300)
progress_bar.grid(row=7, column=0, columnspan=3, pady=10)
progress_bar.grid_remove()

root.mainloop()