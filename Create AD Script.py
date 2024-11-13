import customtkinter as ctk
from tkinter import messagebox

# Função para gerar o comando dsadd
def gerar_comando_usuario(cn, ou_path, dc1, dc2, samid, fn, ln, email, pwd, enable, changepwd, dept, desc):
    upn = f"{samid}@{dc1}.{dc2}"
    dsadd_command = (
        f'dsadd user "CN={cn},{ou_path},DC={dc1},DC={dc2}" '
        f'-samid {samid} '
        f'-fn {fn} '
        f'-ln {ln} '
        f'-email {email} '
        f'-upn "{upn}" '
        f'-pwd "{pwd}" '
        f'-mustchpwd {"yes" if changepwd else "no"} '
        f'-disabled {"yes" if not enable else "no"} '
        f'-dept "{dept}" '
        f'-desc "{desc}"\n'
    )
    return dsadd_command

# Função para gerar o arquivo .bat
def gerar_bat():
    try:
        dc1 = entry_dc1.get()
        dc2 = entry_dc2.get()

        if not usuarios:
            messagebox.showerror("Erro", "Por favor, adicione ao menos um usuário.")
            return

        bat_filename = "adicionar_usuarios.bat"
        with open(bat_filename, 'w') as bat_file:
            for usuario in usuarios:
                comando_usuario = gerar_comando_usuario(
                    usuario['cn'], usuario['ou_path'], dc1, dc2, usuario['samid'],
                    usuario['fn'], usuario['ln'], usuario['email'], usuario['pwd'],
                    usuario['enable'], usuario['changepwd'], usuario['dept'], usuario['desc']
                )
                bat_file.write(comando_usuario)

        messagebox.showinfo("Sucesso", f"Comandos DSADD foram exportados para o arquivo {bat_filename}")

    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um número válido de usuários.")

# Função para adicionar um usuário à lista
def adicionar_usuario():
    try:
        ou_path_input = entry_ou_path.get()
        ou_path_list = [f"OU={ou.strip()}" for ou in ou_path_input.split(',')]
        ou_path = ",".join(ou_path_list)

        # Garantir que o valor de var_enable e var_changepwd sejam sempre booleanos
        enable = var_enable.get() or False  # Se não marcado, assume False (usuário desabilitado)
        changepwd = var_changepwd.get() or False  # Se não marcado, assume False (não alterar a senha)

        usuario = {
            'cn': entry_nome_completo.get(),
            'samid': entry_login.get(),
            'fn': entry_primeiro_nome.get(),
            'ln': entry_ultimo_nome.get(),
            'email': entry_email.get(),
            'ou_path': ou_path,
            'dept': entry_departamento.get(),
            'desc': entry_descricao.get(),
            'pwd': entry_senha.get(),
            'enable': enable,
            'changepwd': changepwd
        }

        # Verifica se algum campo obrigatório está vazio
        if not all([usuario['cn'], usuario['samid'], usuario['fn'], usuario['ln'], usuario['email'], 
                    usuario['ou_path'], usuario['pwd'], usuario['dept']]):
            messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")
            return

        usuarios.append(usuario)
        limpar_campos()
        messagebox.showinfo("Sucesso", f"Usuário '{usuario['cn']}' adicionado com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {str(e)}")

# Função para limpar os campos após o preenchimento dos dados de um usuário
def limpar_campos():
    entry_nome_completo.delete(0, ctk.END)
    entry_login.delete(0, ctk.END)
    entry_primeiro_nome.delete(0, ctk.END)
    entry_ultimo_nome.delete(0, ctk.END)
    entry_email.delete(0, ctk.END)
    entry_ou_path.delete(0, ctk.END)
    entry_departamento.delete(0, ctk.END)
    entry_descricao.delete(0, ctk.END)
    entry_senha.delete(0, ctk.END)
    var_enable.set(True)
    var_changepwd.set(True)

# Inicializar a lista de usuários
usuarios = []

# Configuração inicial para customtkinter
ctk.set_appearance_mode("Dark")  # Tema escuro
ctk.set_default_color_theme("blue")  # Tema azul

# Criando a janela principal
root = ctk.CTk()
root.title("Criar usuário no AD")

# Tamanho da janela
root.geometry("500x700")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Frame principal para centralizar o conteúdo
frame = ctk.CTkFrame(root)
frame.grid(sticky="nsew", padx=20, pady=20)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)

# Título da janela
titulo = ctk.CTkLabel(frame, text="Criar Usuário AD", font=("Arial", 16, "bold"))
titulo.grid(row=0, column=0, columnspan=2, pady=10)

# Definindo os campos de entrada com as cores para o dark mode
labels = [
    ("Domínio antes do ponto (DC1):", 1),
    ("Domínio depois do ponto (DC2):", 2),
    ("Nome completo do usuário:", 3),
    ("Login do domínio (SAMID):", 4),
    ("Primeiro nome:", 5),
    ("Último nome:", 6),
    ("Email:", 7),
    ("Caminho da OU (separado por vírgulas):", 8),
    ("Departamento:", 9),
    ("Descrição:", 10),
    ("Senha:", 11)
]

# Criando os campos de entrada e labels
for text, row in labels:
    label = ctk.CTkLabel(frame, text=text, font=("Arial", 11))
    label.grid(row=row, column=0, sticky="e", padx=10, pady=5)

entry_dc1 = ctk.CTkEntry(frame, width=200)
entry_dc1.grid(row=1, column=1, pady=5)

entry_dc2 = ctk.CTkEntry(frame, width=200)
entry_dc2.grid(row=2, column=1, pady=5)

entry_nome_completo = ctk.CTkEntry(frame, width=200)
entry_nome_completo.grid(row=3, column=1, pady=5)

entry_login = ctk.CTkEntry(frame, width=200)
entry_login.grid(row=4, column=1, pady=5)

entry_primeiro_nome = ctk.CTkEntry(frame, width=200)
entry_primeiro_nome.grid(row=5, column=1, pady=5)

entry_ultimo_nome = ctk.CTkEntry(frame, width=200)
entry_ultimo_nome.grid(row=6, column=1, pady=5)

entry_email = ctk.CTkEntry(frame, width=200)
entry_email.grid(row=7, column=1, pady=5)

entry_ou_path = ctk.CTkEntry(frame, width=200)
entry_ou_path.grid(row=8, column=1, pady=5)

entry_departamento = ctk.CTkEntry(frame, width=200)
entry_departamento.grid(row=9, column=1, pady=5)

entry_descricao = ctk.CTkEntry(frame, width=200)
entry_descricao.grid(row=10, column=1, pady=5)

entry_senha = ctk.CTkEntry(frame, width=200, show="*")
entry_senha.grid(row=11, column=1, pady=5)

# Checkbox para habilitar/desabilitar o usuário
var_enable = ctk.BooleanVar(value=True)
chk_enable = ctk.CTkCheckBox(frame, text="Usuário habilitado", variable=var_enable)
chk_enable.grid(row=12, column=0, columnspan=2, pady=5)

# Checkbox para senha a ser alterada
var_changepwd = ctk.BooleanVar(value=True)
chk_changepwd = ctk.CTkCheckBox(frame, text="Usuário deve alterar a senha", variable=var_changepwd)
chk_changepwd.grid(row=13, column=0, columnspan=2, pady=5)

# Botões
btn_adicionar = ctk.CTkButton(frame, text="Adicionar Usuário", command=adicionar_usuario)
btn_adicionar.grid(row=14, column=0, columnspan=2, pady=10)

btn_gerar_bat = ctk.CTkButton(frame, text="Gerar Arquivo .BAT", command=gerar_bat)
btn_gerar_bat.grid(row=15, column=0, columnspan=2, pady=10)

# Rodando a interface
root.mainloop()
