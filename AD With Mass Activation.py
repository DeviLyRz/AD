import customtkinter as ctk
from tkinter import messagebox, PhotoImage

# Função para gerar o comando dsadd
def gerar_comando_usuario(usuario):
    dc1, dc2 = "campos", "local"
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
        f'-title "{usuario["desc"]}" '
        f'-office "{usuario["dept"]}" '
        f'-display "{usuario["cn"]}"\n'
    )

    return dsadd_command

# Função para gerar o comando dsmod
def gerar_comando_dsmod(nome, desativar=True):
    dc1, dc2 = "campos", "local"
    status = "yes" if desativar else "no"
    dsmod_command = (
        f'dsmod user "CN={nome},DC={dc1},DC={dc2}" -disabled {status}\n'
    )
    return dsmod_command

# Função para gerar o arquivo .bat de criação de usuários
def gerar_bat():
    if not usuarios:
        messagebox.showerror("Erro", "Por favor, adicione ao menos um usuário.")
        return

    with open("adicionar_usuarios.bat", 'w') as bat_file:
        for usuario in usuarios:
            bat_file.write(gerar_comando_usuario(usuario))

    messagebox.showinfo("Sucesso", "Foi gerado o arquivo adicionar_usuarios.bat")

# Função para gerar o arquivo .bat para desativação/ativação de usuários
def desativar_ou_ativar_bat():
    nomes_usuarios = entry_nome_desativar.get("1.0", ctk.END).strip().splitlines()
    if not nomes_usuarios:
        messagebox.showerror("Erro", "Por favor, insira ao menos um nome de usuário.")
        return

    desativar = var_ativar_ou_desativar.get()  # Se for True, desativar; se False, ativar
    arquivo_bat = "desativar_usuarios.bat" if desativar else "ativar_usuarios.bat"

    with open(arquivo_bat, 'w') as bat_file:
        for nome_usuario in nomes_usuarios:
            if nome_usuario.strip():
                bat_file.write(gerar_comando_dsmod(nome_usuario.strip(), desativar))

    status = "desativados" if desativar else "ativados"
    messagebox.showinfo("Sucesso", f"Comandos para {status} foram exportados para o arquivo {arquivo_bat}")

# Função para adicionar usuários à lista
def adicionar_usuario():
    usuario = {
        'cn': entry_nome_completo.get(),
        'samid': entry_login.get(),
        'fn': entry_primeiro_nome.get(),
        'ln': entry_ultimo_nome.get(),
        'email': entry_email.get(),
        'ou_path': ",".join([f"OU={ou.strip().upper()}" for ou in entry_ou_path.get().split(',')]),
        'dept': entry_departamento.get(),
        'desc': entry_descricao.get(),
        'pwd': entry_senha.get(),
        'enable': var_enable.get(),
        'changepwd': var_changepwd.get()
    }
    campos_obrigatorios = ['cn', 'samid', 'fn', 'ln', 'email', 'ou_path', 'pwd', 'dept']
    if not all(usuario[campo] for campo in campos_obrigatorios):
        messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")
        return

    usuarios.append(usuario)
    limpar_campos()
    messagebox.showinfo("Sucesso", f"Usuário '{usuario['cn']}' adicionado com sucesso!")

# Função para limpar campos após o preenchimento
def limpar_campos():
    for entry in entries:
        entry.delete(0, ctk.END)
    var_enable.set(True)
    var_changepwd.set(True)

# Inicializa a lista de usuários
usuarios = []

# Configuração inicial
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

# Criando a janela principal
root = ctk.CTk()
root.title("UNIMED")
root.geometry("500x900")

# Inicializa as variáveis para os checkboxes **após** a criação do root
var_enable = ctk.BooleanVar(value=True)
var_changepwd = ctk.BooleanVar(value=True)
var_ativar_ou_desativar = ctk.BooleanVar(value=True)

try:
    root.iconbitmap("icone.ico")
except Exception:
    icon = PhotoImage(file="C:/Users/erick.penna/Downloads/unimed.png")
    root.iconphoto(True, icon)

# Frame principal
frame = ctk.CTkFrame(root)
frame.grid(sticky="nsew", padx=43, pady=40)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)

# Título da janela
titulo = ctk.CTkLabel(frame, text="Gerenciamento de Usuários AD", font=("Arial", 16, "bold"))
titulo.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

# Campos de entrada
txt_labels = [
    "Nome completo:", "Login (SAMID):", "Primeiro nome:", "Último nome:",
    "Email:", "Caminho da OU:", "Departamento:", "Descrição:", "Senha:"
]
entries = []
for i, text in enumerate(txt_labels):
    label = ctk.CTkLabel(frame, text=text, font=("Arial", 11))
    label.grid(row=i+1, column=0, sticky="e", padx=10, pady=5)
    entry = ctk.CTkEntry(frame, width=200, show="*" if "Senha" in text else "")
    entry.grid(row=i+1, column=1, pady=5)
    entries.append(entry)

entry_nome_completo, entry_login, entry_primeiro_nome, entry_ultimo_nome, entry_email, entry_ou_path, entry_departamento, entry_descricao, entry_senha = entries

# Checkbox para seleção de senha e habilitação
chk_enable = ctk.CTkCheckBox(frame, text="Usuário habilitado", variable=var_enable, fg_color="#028251")
chk_enable.grid(row=len(txt_labels)+1, column=0, columnspan=2, pady=5, sticky="w")

chk_changepwd = ctk.CTkCheckBox(frame, text="Usuário deve alterar a senha", variable=var_changepwd, fg_color="#028251")
chk_changepwd.grid(row=len(txt_labels)+2, column=0, columnspan=2, pady=5, sticky="w")

# Título da seção de desativação
titulo_desativar = ctk.CTkLabel(frame, text="Desativação/Ativação de Usuários", font=("Arial", 16, "bold"))
titulo_desativar.grid(row=len(txt_labels)+3, column=0, columnspan=2, pady=10, sticky="n")

# Campo para nomes de usuários a serem desativados/ativados
label_nome_desativar = ctk.CTkLabel(frame, text="Nomes para desativar/ativar:", font=("Arial", 11))
label_nome_desativar.grid(row=len(txt_labels)+4, column=0, sticky="n", padx=10, pady=0)

# Caixa de texto para inserção dos nomes dos usuários a serem desativados/ativados
entry_nome_desativar = ctk.CTkTextbox(frame, width=200, height=25)
entry_nome_desativar.grid(row=len(txt_labels)+4, column=1, pady=0)

# Checkbox para selecionar a opção de desativar ou ativar
chk_ativar_ou_desativar = ctk.CTkCheckBox(frame, text="Desativar usuários em massa", variable=var_ativar_ou_desativar, fg_color="#028251")
chk_ativar_ou_desativar.grid(row=len(txt_labels)+5, column=0, columnspan=2, pady=5, sticky="w")

# Botões de ação
btn_adicionar = ctk.CTkButton(frame, text="Adicionar Usuário", command=adicionar_usuario, fg_color="#028251")
btn_adicionar.grid(row=len(txt_labels)+6, column=0, columnspan=2, pady=10)

btn_gerar_bat = ctk.CTkButton(frame, text="Gerar Arquivo .BAT", command=gerar_bat, fg_color="#028251")
btn_gerar_bat.grid(row=len(txt_labels)+7, column=0, columnspan=2, pady=10)

btn_desativar_bat = ctk.CTkButton(frame, text="Gerar Comandos para Ativar/Desativar", command=desativar_ou_ativar_bat, fg_color="#028251")
btn_desativar_bat.grid(row=len(txt_labels)+8, column=0, columnspan=2, pady=10)

root.mainloop()
