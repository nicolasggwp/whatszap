import tkinter as tk
from tkinter import ttk, scrolledtext
from cliente import Cliente
from threading import Thread
from datetime import datetime

class App:
    def __init__(self):
        self.cliente = Cliente()

        self.root = tk.Tk()
        self.root.title("Chat App")
        self.root.geometry("500x700")
        self.root.configure(bg="#f0f0f0")

        style = ttk.Style()
        style.theme_use('clam')
        
        self.colors = {
            'bg': '#f0f0f0',
            'primary': '#4CAF50',
            'secondary': '#2196F3',
            'danger': '#f44336',
            'text': '#333333',
            'white': '#ffffff',
            'message_me': '#DCF8C6',
            'message_other': '#FFFFFF'
        }

        container = tk.Frame(self.root, bg=self.colors['bg'])
        container.pack(fill="both", expand=True)

        self.frames = {}

        for F in (HomeFrame, LoginFrame, RegisterFrame, ListaFrame, ChatFrame):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.show(HomeFrame)

    def show(self, frame_class):
        self.frames[frame_class].tkraise()

    def run(self):
        self.root.mainloop()

class HomeFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=app.colors['bg'])
        self.app = app

        center_frame = tk.Frame(self, bg=app.colors['bg'])
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center_frame, text="💬", font=("Segoe UI", 60), 
                bg=app.colors['bg']).pack(pady=20)

        tk.Label(center_frame, text="CHAT APP", 
                font=("Segoe UI", 28, "bold"), 
                fg=app.colors['primary'],
                bg=app.colors['bg']).pack(pady=10)

        tk.Label(center_frame, text="Conecte-se com amigos", 
                font=("Segoe UI", 12), 
                fg="gray",
                bg=app.colors['bg']).pack(pady=(0, 30))

        btn_style = {
            'width': 25,
            'height': 2,
            'font': ("Segoe UI", 11),
            'relief': 'flat',
            'cursor': 'hand2'
        }

        btn_login = tk.Button(center_frame, text="🔑 Login", 
                            command=lambda: app.show(LoginFrame),
                            bg=app.colors['primary'],
                            fg='white',
                            **btn_style)
        btn_login.pack(pady=5)

        btn_register = tk.Button(center_frame, text="📝 Registrar", 
                               command=lambda: app.show(RegisterFrame),
                               bg=app.colors['secondary'],
                               fg='white',
                               **btn_style)
        btn_register.pack(pady=5)

class LoginFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=app.colors['bg'])
        self.app = app

        center_frame = tk.Frame(self, bg=app.colors['bg'])
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center_frame, text="🔐 LOGIN", 
                font=("Segoe UI", 24, "bold"),
                fg=app.colors['secondary'],
                bg=app.colors['bg']).pack(pady=20)

        tk.Label(center_frame, text="Usuário", 
                font=("Segoe UI", 10),
                bg=app.colors['bg'],
                fg=app.colors['text']).pack(anchor="w", pady=(10, 5))

        self.user = tk.Entry(center_frame, font=("Segoe UI", 11),
                           relief='solid', bd=1, width=30)
        self.user.pack(pady=(0, 10))

        tk.Label(center_frame, text="Senha", 
                font=("Segoe UI", 10),
                bg=app.colors['bg'],
                fg=app.colors['text']).pack(anchor="w", pady=(10, 5))

        self.passw = tk.Entry(center_frame, show="*", 
                            font=("Segoe UI", 11),
                            relief='solid', bd=1, width=30)
        self.passw.pack(pady=(0, 20))

        btn_login = tk.Button(center_frame, text="Entrar", 
                            command=self.login,
                            bg=app.colors['primary'],
                            fg='white',
                            font=("Segoe UI", 11),
                            width=25, height=1,
                            relief='flat',
                            cursor='hand2')
        btn_login.pack(pady=5)

        btn_back = tk.Button(center_frame, text="← Voltar", 
                           command=lambda: app.show(HomeFrame),
                           bg=app.colors['bg'],
                           fg=app.colors['secondary'],
                           font=("Segoe UI", 10),
                           relief='flat',
                           cursor='hand2')
        btn_back.pack(pady=5)

        self.status = tk.Label(center_frame, text="", 
                             font=("Segoe UI", 10),
                             bg=app.colors['bg'],
                             fg=app.colors['danger'])
        self.status.pack(pady=10)

    def login(self):
        Thread(target=self._login_thread).start()

    def _login_thread(self):
        user = self.user.get()
        pwd = self.passw.get()

        if not user or not pwd:
            self.app.root.after(0, lambda: self.status.config(text="Preencha todos os campos!"))
            return

        self.app.cliente.send(f"AUTH;LOGIN;{user};{pwd}")
        resposta = self.app.cliente.recv()

        self.app.root.after(0, self._handle_login, resposta)

    def _handle_login(self, resposta):
        if resposta == "AUTH;SUCCESS;LOGIN_OK":
            self.status.config(text="✅ Login OK!", fg=self.app.colors['primary'])
            self.app.show(ListaFrame)
        else:
            self.status.config(text="❌ Erro no login", fg=self.app.colors['danger'])

class RegisterFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=app.colors['bg'])
        self.app = app

        center_frame = tk.Frame(self, bg=app.colors['bg'])
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center_frame, text="📝 REGISTRO", 
                font=("Segoe UI", 24, "bold"),
                fg=app.colors['secondary'],
                bg=app.colors['bg']).pack(pady=20)

        tk.Label(center_frame, text="Usuário", 
                font=("Segoe UI", 10),
                bg=app.colors['bg'],
                fg=app.colors['text']).pack(anchor="w", pady=(10, 5))

        self.user = tk.Entry(center_frame, font=("Segoe UI", 11),
                           relief='solid', bd=1, width=30)
        self.user.pack(pady=(0, 10))

        tk.Label(center_frame, text="Senha", 
                font=("Segoe UI", 10),
                bg=app.colors['bg'],
                fg=app.colors['text']).pack(anchor="w", pady=(10, 5))

        self.passw = tk.Entry(center_frame, show="*", 
                            font=("Segoe UI", 11),
                            relief='solid', bd=1, width=30)
        self.passw.pack(pady=(0, 20))

        btn_register = tk.Button(center_frame, text="Criar conta", 
                               command=self.register,
                               bg=app.colors['secondary'],
                               fg='white',
                               font=("Segoe UI", 11),
                               width=25, height=1,
                               relief='flat',
                               cursor='hand2')
        btn_register.pack(pady=5)

        btn_back = tk.Button(center_frame, text="← Voltar", 
                           command=lambda: app.show(HomeFrame),
                           bg=app.colors['bg'],
                           fg=app.colors['secondary'],
                           font=("Segoe UI", 10),
                           relief='flat',
                           cursor='hand2')
        btn_back.pack(pady=5)

        self.status = tk.Label(center_frame, text="", 
                             font=("Segoe UI", 10),
                             bg=app.colors['bg'])
        self.status.pack(pady=10)

    def register(self):
        Thread(target=self._register_thread).start()

    def _register_thread(self):
        user = self.user.get()
        pwd = self.passw.get()

        if not user or not pwd:
            self.app.root.after(0, lambda: self.status.config(text="Preencha todos os campos!", 
                                                            fg=self.app.colors['danger']))
            return

        self.app.cliente.send(f"AUTH;REGISTER;{user};{pwd}")
        resposta = self.app.cliente.recv()

        self.app.root.after(0, self._handle_register, resposta)

    def _handle_register(self, resposta):
        if resposta.startswith("CTRL;OK"):
            self.status.config(text="✅ Conta criada!", fg=self.app.colors['primary'])
            # Voltar para o login após 2 segundos
            self.app.root.after(2000, lambda: self.app.show(LoginFrame))
        else:
            self.status.config(text="❌ Erro no registro", fg=self.app.colors['danger'])

class ListaFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=app.colors['bg'])
        self.app = app

        header = tk.Frame(self, bg=app.colors['primary'], height=70)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        tk.Label(header, text="💬 Conversas", 
                font=("Segoe UI", 18, "bold"),
                fg='white',
                bg=app.colors['primary']).pack(pady=20)

        self.container = tk.Frame(self, bg=app.colors['bg'])
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        scrollbar = tk.Scrollbar(self.container)
        scrollbar.pack(side="right", fill="y")

        self.list_frame = tk.Frame(self.container, bg=app.colors['bg'])
        self.list_frame.pack(fill="both", expand=True)

        btn_new = tk.Button(self, text="➕ Nova conversa", 
                          command=self.nova_conversa,
                          bg=app.colors['secondary'],
                          fg='white',
                          font=("Segoe UI", 11),
                          height=2,
                          relief='flat',
                          cursor='hand2')
        btn_new.pack(side="bottom", fill="x", padx=20, pady=(0, 20))

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
        for linha in linhas:
            partes = linha.split(";")
            if len(partes) >= 4 and partes[0] == "CHAT" and partes[1] == "CONVERSA":
                conversas.append((partes[2], partes[3]))

        self.app.root.after(0, self._render, conversas)

    def _render(self, conversas):
        for w in self.list_frame.winfo_children():
            w.destroy()

        if not conversas:
            tk.Label(self.list_frame, text="Nenhuma conversa ativa", 
                    font=("Segoe UI", 12),
                    fg="gray",
                    bg=self.app.colors['bg']).pack(pady=50)
            return

        for uid, nome in conversas:
            btn = tk.Button(self.list_frame, 
                          text=f"👤 {nome}",
                          font=("Segoe UI", 11),
                          bg='white',
                          fg=self.app.colors['text'],
                          relief='solid',
                          bd=1,
                          pady=10,
                          anchor='w',
                          command=lambda u=uid: self.abrir_chat(u))
            btn.pack(fill="x", pady=3)

    def abrir_chat(self, user_id):
        Thread(target=self._open_chat_thread, args=(user_id,)).start()

    def _open_chat_thread(self, user_id):
        chat = self.app.frames[ChatFrame]
        chat.abrir(user_id)
        self.app.root.after(0, lambda: self.app.show(ChatFrame))

    def nova_conversa(self):
        popup = tk.Toplevel(self)
        popup.title("Nova Conversa")
        popup.geometry("300x150")
        popup.configure(bg=self.app.colors['bg'])

        tk.Label(popup, text="ID do usuário:", 
                font=("Segoe UI", 11),
                bg=self.app.colors['bg']).pack(pady=20)

        entry = tk.Entry(popup, font=("Segoe UI", 11),
                        relief='solid', bd=1)
        entry.pack(pady=10, padx=20, fill="x")

        def abrir():
            uid = entry.get()
            if uid:
                popup.destroy()
                self.abrir_chat(uid)

        tk.Button(popup, text="Abrir conversa", 
                command=abrir,
                bg=self.app.colors['primary'],
                fg='white',
                font=("Segoe UI", 10),
                relief='flat',
                cursor='hand2').pack(pady=10)

class ChatFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=app.colors['bg'])
        self.app = app
        self.chat_id = None
        self.current_user = None

        header = tk.Frame(self, bg=app.colors['secondary'], height=60)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        self.title = tk.Label(header, text="Chat", 
                            font=("Segoe UI", 16, "bold"),
                            fg='white',
                            bg=app.colors['secondary'])
        self.title.pack(pady=15)

        self.message_area = tk.Frame(self, bg=app.colors['bg'])
        self.message_area.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(self.message_area, bg=app.colors['bg'], highlightthickness=0)
        scrollbar = tk.Scrollbar(self.message_area, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg=app.colors['bg'])
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        input_frame = tk.Frame(self, bg='white', height=60)
        input_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        input_frame.pack_propagate(False)

        self.entry = tk.Entry(input_frame, font=("Segoe UI", 11),
                            relief='solid', bd=1)
        self.entry.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)

        btn_send = tk.Button(input_frame, text="Enviar ▶", 
                           command=self.enviar,
                           bg=self.app.colors['primary'],
                           fg='white',
                           font=("Segoe UI", 10),
                           relief='flat',
                           cursor='hand2',
                           padx=15)
        btn_send.pack(side="right", padx=(0, 10), pady=10)

    def abrir(self, user_id):
        self.chat_id = user_id
        self.title.config(text=f"💬 Chat com {user_id}")

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
        for linha in linhas:
            partes = linha.split(";")
            if len(partes) >= 5 and partes[0] == "CHAT" and partes[1] == "HISTORY":
                sender = partes[2]
                msg = partes[3]
                self.app.root.after(0, self.adicionar_mensagem, sender, msg)

    def adicionar_mensagem(self, sender, msg):
        msg_frame = tk.Frame(self.scrollable_frame, bg=self.app.colors['bg'])
        msg_frame.pack(fill="x", pady=3)

        is_me = sender == "me"

        bubble = tk.Frame(msg_frame, 
                        bg=self.app.colors['message_me'] if is_me else self.app.colors['message_other'],
                        relief='solid', bd=1)
        bubble.pack(side="right" if is_me else "left", 
                   padx=(30, 10) if is_me else (10, 30))

        tk.Label(bubble, text=msg, 
                font=("Segoe UI", 11),
                bg=bubble['bg'],
                fg=self.app.colors['text'],
                wraplength=300,
                justify="left").pack(padx=10, pady=5)

        self.canvas.yview_moveto(1.0)

    def limpar(self):
        for w in self.scrollable_frame.winfo_children():
            w.destroy()

    def enviar(self):
        texto = self.entry.get()
        if not texto or not self.chat_id:
            return

        self.entry.delete(0, "end")
        
        self.adicionar_mensagem("me", texto)

        Thread(target=self._send_thread, args=(texto,)).start()

    def _send_thread(self, texto):
        self.app.cliente.send(f"CHAT;SEND;{self.chat_id};{texto}")

App().run()