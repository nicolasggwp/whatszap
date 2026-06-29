import tkinter as tk
import socket
from threading import Thread



class Cliente:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(("127.0.0.1", 5000))

    def send(self, msg):
        self.socket.send(msg.encode())

    def recv(self):
        return self.socket.recv(1024).decode()



class App:
    def __init__(self):
        self.cliente = Cliente()

        self.root = tk.Tk()
        self.root.title("Chat App")

        container = tk.Frame(self.root)
        container.pack(fill="both", expand=True)

        self.frames = {}

        for F in (HomeFrame, LoginFrame, RegisterFrame, ListaFrame, ChatFrame):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show(HomeFrame)

    def show(self, frame_class):
        self.frames[frame_class].tkraise()

    def run(self):
        self.root.mainloop()



class HomeFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        tk.Label(self, text="CHAT APP", font=("Arial", 18)).pack(pady=20)

        tk.Button(self, text="Login",
                  width=20,
                  command=lambda: app.show(LoginFrame)).pack(pady=10)

        tk.Button(self, text="Registrar",
                  width=20,
                  command=lambda: app.show(RegisterFrame)).pack(pady=10)



class LoginFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        tk.Label(self, text="LOGIN", font=("Arial", 14)).pack(pady=10)

        tk.Label(self, text="Usuário").pack()
        self.user = tk.Entry(self)
        self.user.pack()

        tk.Label(self, text="Senha").pack()
        self.passw = tk.Entry(self, show="*")
        self.passw.pack()

        tk.Button(self, text="Entrar", command=self.login).pack(pady=10)

        tk.Button(self, text="Voltar",
                  command=lambda: app.show(HomeFrame)).pack()

        self.status = tk.Label(self, text="")
        self.status.pack()

  
    def login(self):
        Thread(target=self._login_thread).start()

    def _login_thread(self):
        user = self.user.get()
        pwd = self.passw.get()

        self.app.cliente.send(f"AUTH;LOGIN;{user};{pwd}")
        resposta = self.app.cliente.recv()

        self.app.root.after(0, self._handle_login, resposta)

    def _handle_login(self, resposta):
        if resposta == "AUTH;SUCCESS;LOGIN_OK":
            self.status.config(text="Login OK")
            self.app.show(ListaFrame)
        else:
            self.status.config(text="Erro no login")



class RegisterFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        tk.Label(self, text="REGISTRO", font=("Arial", 14)).pack(pady=10)

        tk.Label(self, text="Usuário").pack()
        self.user = tk.Entry(self)
        self.user.pack()

        tk.Label(self, text="Senha").pack()
        self.passw = tk.Entry(self, show="*")
        self.passw.pack()

        tk.Button(self, text="Criar conta", command=self.register).pack(pady=10)

        tk.Button(self, text="Voltar",
                  command=lambda: app.show(HomeFrame)).pack()

        self.status = tk.Label(self, text="")
        self.status.pack()

    def register(self):
        Thread(target=self._register_thread).start()

    def _register_thread(self):
        user = self.user.get()
        pwd = self.passw.get()

        self.app.cliente.send(f"AUTH;REGISTER;{user};{pwd}")
        resposta = self.app.cliente.recv()

        self.app.root.after(0, self._handle_register, resposta)

    def _handle_register(self, resposta):
        if resposta.startswith("CTRL;OK"):
            self.status.config(text="Conta criada!")
        else:
            self.status.config(text="Erro no registro")



class ListaFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        tk.Label(self, text="CONVERSAS", font=("Arial", 14)).pack(pady=10)

        self.container = tk.Frame(self)
        self.container.pack()

        tk.Button(self, text="+ Nova conversa",
                  command=self.nova_conversa).pack(pady=10)

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.carregar_conversas()

  
    def carregar_conversas(self):
        Thread(target=self._carregar_thread).start()

    def _carregar_thread(self):
        self.app.cliente.send("CHAT;LIST")

        buffer = ""
        conversas = []

        while True:
            buffer += self.app.cliente.recv()

            if "CHAT;LIST_END\n" in buffer:
                break

        linhas = buffer.split("\n")
        print(linhas)
        for linha in linhas:
            partes = linha.split(";")

            if len(partes) >= 4 and partes[0] == "CHAT" and partes[1] == "CONVERSA":
                conversas.append((partes[2], partes[3]))

        self.app.root.after(0, self._render, conversas)

    def _render(self, conversas):
        for w in self.container.winfo_children():
            w.destroy()

        if not conversas:
            tk.Label(self.container, text="Nenhuma conversa").pack()
            return

        for uid, nome in conversas:
            tk.Button(
                self.container,
                text=nome,
                width=30,
                command=lambda u=uid: self.abrir_chat(u)
            ).pack(pady=2)

    def abrir_chat(self, user_id):
        Thread(target=self._open_chat_thread, args=(user_id,)).start()

    def abrir_chat(self, user_id):
        chat = self.app.frames[ChatFrame]
        chat.abrir(user_id)
        self.app.show(ChatFrame)

    def nova_conversa(self):
        popup = tk.Toplevel(self)

        tk.Label(popup, text="ID do usuário:").pack()

        entry = tk.Entry(popup)
        entry.pack()

        def abrir():
            uid = entry.get()
            popup.destroy()
            self.abrir_chat(uid)

        tk.Button(popup, text="Abrir", command=abrir).pack()

class ChatFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.chat_id = None

        self.title = tk.Label(self, text="Chat")
        self.title.pack()

        self.text = tk.Text(self, state="disabled", width=50, height=20)
        self.text.pack()

        self.entry = tk.Entry(self)
        self.entry.pack(fill="x")

        tk.Button(self, text="Enviar", command=self.enviar).pack()

    def abrir(self, user_id):
        self.chat_id = user_id
        self.title.config(text=f"Chat com {user_id}")

        self.limpar()

        Thread(target=self.carregar_historico).start()

    def carregar_historico(self):
        self.app.cliente.send(f"CHAT;OPEN;{self.chat_id}")

        buffer = ""

        while True:
            buffer += self.app.cliente.recv()

            if "CHAT;HISTORY_END" in buffer:
                break

        linhas = buffer.split("\n")
        print(linhas)

        for linha in linhas:
            partes = linha.split(";")

            if len(partes) >= 4 and partes[0] == "CHAT" and partes[1] == "HISTORY":
                texto = partes[3]
                self.app.root.after(0, self.adicionar, texto)

    def adicionar(self, msg):
        self.text.config(state="normal")
        self.text.insert("end", msg + "\n")
        self.text.config(state="disabled")

    def limpar(self):
        self.text.config(state="normal")
        self.text.delete("1.0", "end")
        self.text.config(state="disabled")

    def enviar(self):
        texto = self.entry.get()
        self.entry.delete(0, "end")

        self.app.cliente.send(f"CHAT;SEND;{self.chat_id};{texto}")




App().run()