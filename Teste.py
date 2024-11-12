import tkinter as tk
from tkinter import messagebox

# Função para gerar o comando dsadd
def gerar_comando_usuario(cn, ou_path, dc1, dc2, samid, fn, ln, email, pwd, enable, changepwd, dept, desc):
    # Montar o UPN (User Principal Name)
    upn = f"{samid}@{dc1}.{dc2}"

    # Gerar o comando dsadd user com o caminho completo da OU
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
        # Coletar os domínios
        dc1 = entry_dc1.get()
        dc2 = entry_dc2.get()

        # Verificar se temos usuários adicionados
        if not usuarios:
            messagebox.showerror("Erro", "Por favor, adicione ao menos um usuário.")
            return

        # Criando ou abrindo o arquivo .bat para escrita
        bat_filename = "adicionar_usuarios.bat"
        with open(bat_filename, 'w') as bat_file:
            for usuario in usuarios:
                # Gerar o comando para o usuário atual
                comando_usuario = gerar_comando_usuario(
                    usuario['cn'],
                    usuario['ou_path'],
                    dc1, dc2,
                    usuario['samid'],
                    usuario['fn'],
                    usuario['ln'],
                    usuario['email'],
                    usuario['pwd'],
                    usuario['enable'],
                    usuario['changepwd'],
                    usuario['dept'],
                    usuario['desc']
                )
                # Escrever o comando no arquivo .bat
                bat_file.write(comando_usuario)

        messagebox.showinfo("Sucesso", f"Comandos DSADD foram exportados para o arquivo {bat_filename}")

    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um número válido de usuários.")


# Função para adicionar um usuário à lista
def adicionar_usuario():
    try:
        # Coletar os dados do usuário
        ou_path_input = entry_ou_path.get()
        # Dividir os valores da OU por vírgulas e adicionar "OU=" a cada valor
        ou_path_list = [f"OU={ou.strip()}" for ou in ou_path_input.split(',')]
        ou_path = ",".join(ou_path_list)

        usuario = {
            'cn': entry_nome_completo.get(),
            'samid': entry_login.get(),
            'fn': entry_primeiro_nome.get(),
            'ln': entry_ultimo_nome.get(),
            'email': entry_email.get(),
            'ou_path': ou_path,  # Lista de OUs formatada
            'dept': entry_departamento.get(),
            'desc': entry_descricao.get(),
            'pwd': entry_senha.get(),
            'enable': var_enable.get(),
            'changepwd': var_changepwd.get()
        }

        # Validar se todos os campos estão preenchidos
        for key, value in usuario.items():
            if not value:
                messagebox.showerror("Erro", f"Por favor, preencha o campo '{key}'.")
                return

        # Adicionar o usuário à lista de usuários
        usuarios.append(usuario)

        # Limpar os campos para o próximo usuário
        limpar_campos()
        messagebox.showinfo("Sucesso", f"Usuário '{usuario['cn']}' adicionado com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao adicionar o usuário: {str(e)}")


# Função para limpar os campos após o preenchimento dos dados de um usuário
def limpar_campos():
    entry_nome_completo.delete(0, tk.END)
    entry_login.delete(0, tk.END)
    entry_primeiro_nome.delete(0, tk.END)
    entry_ultimo_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_ou_path.delete(0, tk.END)
    entry_departamento.delete(0, tk.END)
    entry_descricao.delete(0, tk.END)
    entry_senha.delete(0, tk.END)
    var_enable.set(True)
    var_changepwd.set(True)

# Inicializar a lista de usuários
usuarios = []

# Criando a janela principal
root = tk.Tk()
root.title("Criar usuário no AD")

# Definir o tamanho da janela
root.geometry("500x500")

# Campos de entrada
tk.Label(root, text="Domínio antes do ponto (DC1):").grid(row=0, column=0, sticky="e")
entry_dc1 = tk.Entry(root)
entry_dc1.grid(row=0, column=1)

tk.Label(root, text="Domínio depois do ponto (DC2):").grid(row=1, column=0, sticky="e")
entry_dc2 = tk.Entry(root)
entry_dc2.grid(row=1, column=1)

# Campos do usuário (preenchidos para cada novo usuário)
tk.Label(root, text="Nome completo do usuário:").grid(row=2, column=0, sticky="e")
entry_nome_completo = tk.Entry(root)
entry_nome_completo.grid(row=2, column=1)

tk.Label(root, text="Login do domínio (SAMID):").grid(row=3, column=0, sticky="e")
entry_login = tk.Entry(root)
entry_login.grid(row=3, column=1)

tk.Label(root, text="Primeiro nome:").grid(row=4, column=0, sticky="e")
entry_primeiro_nome = tk.Entry(root)
entry_primeiro_nome.grid(row=4, column=1)

tk.Label(root, text="Último nome:").grid(row=5, column=0, sticky="e")
entry_ultimo_nome = tk.Entry(root)
entry_ultimo_nome.grid(row=5, column=1)

tk.Label(root, text="Email:").grid(row=6, column=0, sticky="e")
entry_email = tk.Entry(root)
entry_email.grid(row=6, column=1)

tk.Label(root, text="Caminho da OU (digite nomes separados por vírgulas):").grid(row=7, column=0, sticky="e")
entry_ou_path = tk.Entry(root)
entry_ou_path.grid(row=7, column=1)

tk.Label(root, text="Departamento:").grid(row=8, column=0, sticky="e")
entry_departamento = tk.Entry(root)
entry_departamento.grid(row=8, column=1)

tk.Label(root, text="Descrição:").grid(row=9, column=0, sticky="e")
entry_descricao = tk.Entry(root)
entry_descricao.grid(row=9, column=1)

tk.Label(root, text="Senha:").grid(row=10, column=0, sticky="e")
entry_senha = tk.Entry(root, show="*")
entry_senha.grid(row=10, column=1)

# Opções para usuário desabilitado e senha a alterar
var_enable = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Usuário habilitado", variable=var_enable).grid(row=11, column=0, columnspan=2)

var_changepwd = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Usuário deve alterar a senha", variable=var_changepwd).grid(row=12, column=0, columnspan=2)

# Botões para adicionar usuário e gerar arquivo .bat
btn_adicionar = tk.Button(root, text="Adicionar usuário", command=adicionar_usuario)
btn_adicionar.grid(row=13, column=0, columnspan=2, pady=10)

btn_gerar_bat = tk.Button(root, text="Gerar Arquivo .BAT", command=gerar_bat)
btn_gerar_bat.grid(row=14, column=0, columnspan=2, pady=10)

# Rodar a interface gráfica
root.mainloop()
