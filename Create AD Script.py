import customtkinter as ctk
from tkinter import messagebox, PhotoImage  # Importação adicional para suporte a ícones .png

# Função para gerar o comando dsadd
def gerar_comando_usuario(usuario):
    dc1, dc2 = "campos", "local"  # Define os valores padrão
    upn = f"{usuario['samid']}@{dc1}.{dc2}"
    dsadd_command = (
        f'dsadd user "CN={usuario["cn"]},{usuario["ou_path"]},DC={dc1},DC={dc2}" '
        f'-samid {usuario["samid"]} '
        f'-fn {usuario["fn"]} '
        f'-ln {usuario["ln"]} '
        f'-email {usuario["email"]} '
        f'-upn "{upn}" '
        f'-pwd "{usuario["pwd"]}" '
        f'-mustchpwd {"yes" if usuario["changepwd"] else "no"} '
        f'-disabled {"yes" if not usuario["enable"] else "no"} '
        f'-dept "{usuario["dept"]}" '
        f'-desc "{usuario["desc"]}" '
        f'-title "{usuario["desc"]}" '  # Título recebe o valor da descrição
        f'-office "{usuario["dept"]}" '  # Office recebe o valor do departamento
        f'-display "{usuario["cn"]}"\n'  # DisplayName recebe o valor do CN
    )

    return dsadd_command

# Função para gerar o arquivo .bat
def gerar_bat():
    if not usuarios:
        messagebox.showerror("Erro", "Por favor, adicione ao menos um usuário.")
        return

    with open("adicionar_usuarios.bat", 'w') as bat_file:
        for usuario in usuarios:
            bat_file.write(gerar_comando_usuario(usuario))

    messagebox.showinfo("Sucesso", "Comandos DSADD foram exportados para o arquivo adicionar_usuarios.bat")

# Função para adicionar um usuário à lista
def adicionar_usuario():
    usuario = {
        'cn': entry_nome_completo.get(),
        'samid': entry_login.get(),
        'fn': entry_primeiro_nome.get(),
        'ln': entry_ultimo_nome.get(),
        'email': entry_email.get(),
        'ou_path': ",".join([f"OU={ou.strip()}" for ou in entry_ou_path.get().split(',')]),
        'dept': entry_departamento.get(),
        'desc': entry_descricao.get(),
        'pwd': entry_senha.get(),
        'enable': var_enable.get(),
        'changepwd': var_changepwd.get()
    }

    # Verifica apenas os campos obrigatórios
    campos_obrigatorios = ['cn', 'samid', 'fn', 'ln', 'email', 'ou_path', 'pwd', 'dept']
    if not all(usuario[campo] for campo in campos_obrigatorios):
        messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")
        return

    usuarios.append(usuario)
    limpar_campos()
    messagebox.showinfo("Sucesso", f"Usuário '{usuario['cn']}' adicionado com sucesso!")

# Função para limpar os campos após o preenchimento dos dados de um usuário
def limpar_campos():
    for entry in entries:
        entry.delete(0, ctk.END)
    var_enable.set(True)
    var_changepwd.set(True)

# Inicializar a lista de usuários
usuarios = []

# Configuração inicial para customtkinter
ctk.set_appearance_mode("Dark")  # Tema escuro
ctk.set_default_color_theme("green")  # Tema verde

# Criando a janela principal
root = ctk.CTk()
root.title("UNIMED")
root.geometry("500x700")

# Define o ícone da janela
try:
    root.iconbitmap("icone.ico")  # Usa um arquivo .ico no Windows
except Exception:
    icon = PhotoImage(file="C:/Users/erick.penna/Downloads/unimed.png")  # Alternativa para outros sistemas com .png
    root.iconphoto(True, icon)

# Frame principal para centralizar o conteúdo
frame = ctk.CTkFrame(root)
frame.grid(sticky="nsew", padx=43, pady=40)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)

# Título da janela
titulo = ctk.CTkLabel(frame, text="Criar Usuário AD", font=("Arial", 16, "bold"))
titulo.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

# Campos de entrada e labels
labels_texts = [
    "Nome completo do usuário:", "Login do domínio (SAMID):",
    "Primeiro nome:", "Último nome:", "Email:",
    "Caminho da OU (separado por vírgulas):", "Departamento:", "Descrição:", "Senha:"
]

entries = []
for i, text in enumerate(labels_texts):
    label = ctk.CTkLabel(frame, text=text, font=("Arial", 11))
    label.grid(row=i+1, column=0, sticky="e", padx=10, pady=5)

    entry = ctk.CTkEntry(frame, width=200, show="*" if "Senha" in text else "")
    entry.grid(row=i+1, column=1, pady=5)
    entries.append(entry)

entry_nome_completo, entry_login, entry_primeiro_nome, \
entry_ultimo_nome, entry_email, entry_ou_path, entry_departamento, \
entry_descricao, entry_senha = entries

# Checkbox para habilitar/desabilitar o usuário
var_enable = ctk.BooleanVar(value=True)
chk_enable = ctk.CTkCheckBox(frame, text="Usuário habilitado", variable=var_enable, fg_color="#028251")
chk_enable.grid(row=len(labels_texts)+1, column=0, columnspan=2, pady=5)

# Checkbox para senha a ser alterada
var_changepwd = ctk.BooleanVar(value=True)
chk_changepwd = ctk.CTkCheckBox(frame, text="Usuário deve alterar a senha", variable=var_changepwd, fg_color="#028251")
chk_changepwd.grid(row=len(labels_texts)+2, column=0, columnspan=2, pady=5)

# Botões com cor personalizada
btn_adicionar = ctk.CTkButton(frame, text="Adicionar Usuário", command=adicionar_usuario, fg_color="#028251")
btn_adicionar.grid(row=len(labels_texts)+3, column=0, columnspan=2, pady=10)

btn_gerar_bat = ctk.CTkButton(frame, text="Gerar Arquivo .BAT", command=gerar_bat, fg_color="#028251")
btn_gerar_bat.grid(row=len(labels_texts)+4, column=0, columnspan=2, pady=10)

# Rodando a interface
root.mainloop()
