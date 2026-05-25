import random, json
import tkinter as tk
from  tkinter import font as tkfont, messagebox
from Entidades import Jugador, Enemigo, Dragon, Item
from Estilos import C, LOGO
from datos_highscores import cargar_hs, guardar_puntuacion

# ══════════════════════ APP ══════════════════════
class GotApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GAME OF THRONES — Torneos de Combate")
        self.geometry("1080x600"); self.minsize(860,580)
        self.configure(bg=C["bg"]); self.resizable(False,False)
        self.jugador=None; self.enemigo=None; self.enemigos=[]; self.idx=0; self.ring=0
        self._fonts()
        self._pantalla_inicio()

    def _fonts(self):
        self.FT  = tkfont.Font(family="Georgia",size=28,weight="bold")
        self.FS  = tkfont.Font(family="Georgia",size=13,weight="bold")
        self.FB  = tkfont.Font(family="Georgia",size=11,weight="bold")
        self.FC  = tkfont.Font(family="Courier",size=9)
        self.FSM = tkfont.Font(family="Georgia",size=9)
        self.FE  = tkfont.Font(family="Georgia",size=9,slant="italic")

    def _limpiar(self):
        for w in self.winfo_children(): w.destroy()

    def _sep(self, p, c=None, px=20):
        tk.Frame(p,bg=c or C["oro"],height=1).pack(fill="x",padx=px,pady=4)

    def _btn(self, p, txt, bg, cmd, fg="white", ipy=8):
        return tk.Button(p,text=txt,font=self.FB,bg=bg,fg=fg,
                         activebackground=C["oro2"],activeforeground=C["bg"],
                         relief="flat",bd=0,cursor="hand2",command=cmd)

    # ══════════ INICIO ══════════
    def _pantalla_inicio(self):
        self._limpiar()
        cv=tk.Canvas(self,bg=C["bg"],highlightthickness=0)
        cv.pack(fill="both",expand=True)

        # Estrellas decorativas
        for _ in range(60):
            x,y=random.randint(0,1080),random.randint(0,600)
            r=random.choice([1,1,1,2])
            cv.create_oval(x,y,x+r,y+r,fill=random.choice([C["oro"],C["dim"],C["gris"]]),outline="")

        # Marco central ornamentado
        f=tk.Frame(cv,bg=C["panel"],highlightbackground=C["oro"],highlightthickness=2)
        cv.create_window(540,300,window=f,width=500,height=500)

        # Ornamento superior
        tk.Label(f,text="✦ ——— ✦ ——— ✦",font=self.FSM,bg=C["panel"],fg=C["dim"]).pack(pady=(22,4))
        tk.Label(f,text="GAME  OF  THRONES",font=self.FT,bg=C["panel"],fg=C["oro"]).pack()
        tk.Label(f,text="Torneos de Combate",font=self.FE,bg=C["panel"],fg=C["gris"]).pack()
        tk.Label(f,text="✦ ——— ✦ ——— ✦",font=self.FSM,bg=C["panel"],fg=C["dim"]).pack(pady=(4,16))

        self._sep(f)

        tk.Label(f,text="NOMBRE DE TU GUERRERO",font=self.FSM,bg=C["panel"],fg=C["dim"]).pack(pady=(14,4))
        self.entry=tk.Entry(f,font=tkfont.Font(family="Georgia",size=13),
                            bg=C["card"],fg=C["oro2"],insertbackground=C["oro2"],
                            relief="flat",highlightbackground=C["borde"],highlightthickness=1,
                            width=24,justify="center",bd=0)
        self.entry.pack(ipady=9,pady=(0,18))
        self.entry.bind("<Return>",lambda e:self._iniciar())
        self.entry.focus()

        self._btn(f,"⚔   ENTRAR AL TORNEO",C["rojo"],self._iniciar).pack(ipadx=22,ipady=10,pady=(0,10))
        self._btn(f,"🏆   SALÓN DE LA FAMA",C["card"],self._hs_win,fg=C["oro"]).pack(ipadx=16,ipady=7,pady=(0,22))

        self._sep(f)
        tk.Label(f,text="7 enemigos · 3 combates cada uno · ¡Demuestra tu valentia!",
                 font=self.FSM,bg=C["panel"],fg=C["dim"]).pack(pady=12)

    def _iniciar(self):
        n=self.entry.get().strip()
        if len(n)<2: messagebox.showwarning("Casa inválida","El nombre debe tener al menos 2 caracteres."); return
        self.jugador=Jugador(n)
        self.jugador.inventario.agregar_item(Item("Vino del Maestre",50,"cura"))
        self.jugador.inventario.agregar_item(Item("Vino del Maestre",50,"cura"))
        self.jugador.inventario.agregar_item(Item("Ungüento de Sanador",20,"cura"))
        self.enemigos=[Enemigo() for _ in range(6)]+[Dragon()]
        random.shuffle(self.enemigos)
        self.idx=0; self.ring=1
        self._nuevo_enemigo()
        self._pantalla_combate()

    def _nuevo_enemigo(self):
        b=self.enemigos[self.idx]
        self.enemigo=Dragon() if isinstance(b,Dragon) else Enemigo(nb=b.nombre)

    # ══════════ COMBATE ══════════
    def _pantalla_combate(self):
        self._limpiar()
        # ── Header ──
        hdr=tk.Frame(self,bg=C["card"],highlightbackground=C["borde"],highlightthickness=1)
        hdr.pack(fill="x")
        tk.Label(hdr,text="⚔ GAME OF THRONES — TORNEOS",font=self.FS,bg=C["card"],fg=C["oro"]).pack(side="left",padx=16,pady=7)
        self.lbl_info=tk.Label(hdr,text="",font=self.FSM,bg=C["card"],fg=C["gris"])
        self.lbl_info.pack(side="left",padx=8)
        self.lbl_pts=tk.Label(hdr,text="",font=self.FB,bg=C["card"],fg=C["oro2"])
        self.lbl_pts.pack(side="right",padx=16)

        # ── Layout 3 columnas ──
        body=tk.Frame(self,bg=C["bg"]); body.pack(fill="both",expand=True,padx=8,pady=6)

        izq=tk.Frame(body,bg=C["bg"],width=250); izq.pack(side="left",fill="y"); izq.pack_propagate(False)
        self._panel_jugador(izq); self._panel_acciones(izq); self._panel_inv(izq)

        ctr=tk.Frame(body,bg=C["bg"]); ctr.pack(side="left",fill="both",expand=True,padx=6)
        self._panel_log(ctr)

        der=tk.Frame(body,bg=C["bg"],width=250); der.pack(side="right",fill="y"); der.pack_propagate(False)
        self._panel_enemigo(der)

        self._ui(); self._log(f"『 Combate 1/3 — {self.enemigo.nombre} 』",C["oro"])
        self._log("¡Que los Siete los guíen!",C["gris"])

    def _card(self, parent, borde=None):
        f=tk.Frame(parent,bg=C["card"],highlightbackground=borde or C["borde"],highlightthickness=1)
        f.pack(fill="x",pady=(0,5)); return f

    def _barra(self, parent, color):
        bg=tk.Frame(parent,bg=C["borde"],height=12); bg.pack(fill="x",padx=10,pady=(0,6))
        bg.pack_propagate(False)
        bar=tk.Frame(bg,bg=color,height=12); bar.place(x=0,y=0,relheight=1); return bar, bg

    def _panel_jugador(self, p):
        f=self._card(p,C["hielo"])
        tk.Label(f,text="☘ TU GUERRERO",font=self.FSM,bg=C["card"],fg=C["hielo"]).pack(anchor="w",padx=10,pady=(8,2))
        self.lbl_jn=tk.Label(f,text="",font=self.FB,bg=C["card"],fg=C["gris2"]); self.lbl_jn.pack(anchor="w",padx=10)
        self.lbl_jhp=tk.Label(f,text="",font=self.FC,bg=C["card"],fg=C["dim"]); self.lbl_jhp.pack(anchor="w",padx=10,pady=(4,0))
        self.bar_j,self.bar_jbg=self._barra(f,C["verde2"])
        self.lbl_jdef=tk.Label(f,text="",font=self.FSM,bg=C["card"],fg=C["dim"]); self.lbl_jdef.pack(anchor="w",padx=10,pady=(0,8))

    def _panel_acciones(self, p):
        f=self._card(p)
        tk.Label(f,text="ACCIONES",font=self.FSM,bg=C["card"],fg=C["dim"]).pack(pady=(8,5))
        BOTS=[("⚔  ATACAR",C["rojo"],self._atacar),("🛡  DEFENDER",C["hielo"],self._defender),
              ("🍷  USAR ÍTEM",C["verde"],self._item),("🏃  HUIR",C["dim"],self._huir),
              ("🏆  SALÓN DE LA FAMA",C["borde"],self._hs_win)]
        self.bots=[]
        for txt,bg,cmd in BOTS:
            b=self._btn(f,txt,bg,cmd)
            b.pack(fill="x",padx=8,pady=2,ipady=7)
            self.bots.append(b)
        tk.Frame(f,height=6,bg=C["card"]).pack()

    def _panel_inv(self, p):
        f=self._card(p)
        tk.Label(f,text="🎒 INVENTARIO",font=self.FSM,bg=C["card"],fg=C["dim"]).pack(anchor="w",padx=10,pady=(8,4))
        self.finv=tk.Frame(f,bg=C["card"]); self.finv.pack(fill="x",padx=10,pady=(0,8))

    def _panel_log(self, p):
        tk.Label(p,text="— CAMPO DE BATALLA —",font=self.FSM,bg=C["bg"],fg=C["dim"]).pack(pady=(2,4))
        lf=tk.Frame(p,bg=C["card"],highlightbackground=C["oro"],highlightthickness=1); lf.pack(fill="both",expand=True)
        self.log=tk.Text(lf,font=self.FC,bg=C["card"],fg=C["texto"],state="disabled",
                          wrap="word",relief="flat",bd=0,padx=10,pady=8,cursor="arrow")
        self.log.pack(side="left",fill="both",expand=True)
        sc=tk.Scrollbar(lf,command=self.log.yview,bg=C["borde"],troughcolor=C["card"],relief="flat")
        sc.pack(side="right",fill="y"); self.log.configure(yscrollcommand=sc.set)
        for tag,col,bold in [("oro",C["oro"],True),("rojo",C["rojo2"],False),("verde",C["verde2"],False),
                              ("hielo",C["hielo"],False),("crit",C["critico"],True),("dim",C["dim"],False),
                              ("gris",C["gris"],False),("borde",C["borde"],False)]:
            kw={"foreground":col}
            if bold: kw["font"]=("Courier",9,"bold")
            self.log.tag_config(tag,**kw)

    def _panel_enemigo(self, p):
        f=self._card(p,C["rojo"])
        tk.Label(f,text="☠ ENEMIGO",font=self.FSM,bg=C["card"],fg=C["rojo2"]).pack(anchor="w",padx=10,pady=(8,2))
        self.lbl_es=tk.Label(f,text="",font=tkfont.Font(size=38),bg=C["card"]); self.lbl_es.pack(pady=4)
        self.lbl_en=tk.Label(f,text="",font=self.FB,bg=C["card"],fg=C["rojo2"]); self.lbl_en.pack(anchor="w",padx=10)
        self.lbl_ehp=tk.Label(f,text="",font=self.FC,bg=C["card"],fg=C["dim"]); self.lbl_ehp.pack(anchor="w",padx=10,pady=(4,0))
        self.bar_e,self.bar_ebg=self._barra(f,C["rojo2"])
        self.lbl_edef=tk.Label(f,text="",font=self.FSM,bg=C["card"],fg=C["dim"]); self.lbl_edef.pack(anchor="w",padx=10,pady=(0,4))
        tk.Label(f,text="ATAQUES:",font=self.FSM,bg=C["card"],fg=C["dim"]).pack(anchor="w",padx=10)
        self.fatk=tk.Frame(f,bg=C["card"]); self.fatk.pack(fill="x",padx=10,pady=(2,10))

    # ── Update UI ──
    def _ui(self):
        j=self.jugador; e=self.enemigo
        self.lbl_info.config(text=f"Enemigo {self.idx+1}/{len(self.enemigos)}  ·  Combate {self.ring}/3")
        self.lbl_pts.config(text=f"🏆 {j.puntos} victorias")
        self.lbl_jn.config(text=j.nombre)
        self.lbl_jhp.config(text=f"Vida: {j.vida} / {j.vida_maxima}")
        p=j.vida/j.vida_maxima
        col=C["verde2"] if p>.5 else (C["critico"] if p>.25 else C["rojo2"])
        self.bar_j.config(bg=col); self.bar_j.place(relwidth=max(.02,p))
        self.lbl_jdef.config(text="🛡 EN GUARDIA" if j.defendiendo else f"Defensa: {j.defensa}",
                              fg=C["hielo"] if j.defendiendo else C["dim"])
        # inv
        for w in self.finv.winfo_children(): w.destroy()
        if j.inventario.items:
            for i,it in enumerate(j.inventario.items):
                tk.Label(self.finv,text=f"[{i}] {it}",font=self.FSM,bg=C["card"],fg=C["verde2"]).pack(anchor="w")
        else:
            tk.Label(self.finv,text="— vacía —",font=self.FSM,bg=C["card"],fg=C["dim"]).pack(anchor="w")
        # enemigo
        self.lbl_es.config(text=LOGO(e.nombre))
        self.lbl_en.config(text=e.nombre)
        self.lbl_ehp.config(text=f"Vida: {e.vida} / {e.vida_maxima}")
        pe=e.vida/e.vida_maxima
        ce=C["verde2"] if pe>.5 else (C["critico"] if pe>.25 else C["rojo2"])
        self.bar_e.config(bg=ce); self.bar_e.place(relwidth=max(.02,pe))
        self.lbl_edef.config(text=f"Defensa: {e.defensa}")
        for w in self.fatk.winfo_children(): w.destroy()
        for a in e.ataques:
            tk.Label(self.fatk,text=f"· {a.nombre}",font=self.FSM,bg=C["card"],fg=C["rojo"]).pack(anchor="w")

    def _log(self, txt, color=None):
        tag_map={C["oro"]:"oro",C["rojo2"]:"rojo",C["verde2"]:"verde",C["hielo"]:"hielo",
                 C["critico"]:"crit",C["dim"]:"dim",C["gris"]:"gris",C["borde"]:"borde"}
        tag=tag_map.get(color,"gris")
        self.log.config(state="normal")
        self.log.insert("end",txt+"\n",tag)
        self.log.see("end"); self.log.config(state="disabled")

    def _off(self): [b.config(state="disabled") for b in self.bots]
    def _on(self): [b.config(state="normal") for b in self.bots]

    # ── Acciones ──
    def _atacar(self):
        self._off()
        r=self.jugador.atacar(self.enemigo)
        if r["tipo"]=="fallo": self._log(f"  💨 {r['msg']}",C["dim"])
        elif r["tipo"]=="critico": self._log(f"  ⚡ {r['msg']}",C["critico"])
        else: self._log(f"  ⚔  {r['msg']}",C["oro"])
        self._ui(); self.after(300,self._turno_e)

    def _defender(self):
        self._off()
        r=self.jugador.defender()
        self._log(f"  🛡 {r['msg']}",C["hielo"])
        self._ui(); self.after(300,self._turno_e)

    def _item(self):
        items=self.jugador.inventario.items
        if not items: self._log("  ⚠ El inventario está vacío.",C["dim"]); return
        win=tk.Toplevel(self); win.title("Inventario"); win.geometry("350x280")
        win.configure(bg=C["panel"]); win.resizable(False,False); win.grab_set(); win.transient(self)
        tk.Label(win,text="🍷 USAR ÍTEM",font=self.FS,bg=C["panel"],fg=C["oro"]).pack(pady=(16,4))
        self._sep(win)
        for i,it in enumerate(items):
            row=tk.Frame(win,bg=C["card"],highlightbackground=C["borde"],highlightthickness=1)
            row.pack(fill="x",padx=20,pady=4)
            tk.Label(row,text=str(it),font=self.FC,bg=C["card"],fg=C["verde2"]).pack(side="left",padx=10,pady=8)
            def usar(idx=i,w=win):
                self._off()
                it2=self.jugador.inventario.usar_item(idx)
                if it2:
                    c=self.jugador.sanar(it2.efecto)
                    self._log(f"  🍷 {it2.nombre} restaura {c} de vida.",C["verde2"])
                w.destroy(); self._ui(); self.after(300,self._turno_e)
            self._btn(row,"USAR",C["verde"],usar).pack(side="right",padx=8,ipadx=8,ipady=4)
        self._btn(win,"Cancelar",C["borde"],win.destroy,fg=C["dim"]).pack(pady=10,ipadx=12,ipady=5)

    def _huir(self):
        self._off()
        if random.random()<0.45:
            self._log("  🏃 Escapaste deshonrosamente del combate.",C["dim"])
            self.after(500,self._sig_ring_forzado)
        else:
            self._log("  ❌ ¡No lograste huir! El combate continúa.",C["rojo2"])
            self._ui(); self.after(300,self._turno_e)

    def _turno_e(self):
        if not self.enemigo.esta_vivo(): self._fin_combate(); return
        r=self.enemigo.atacar(self.jugador)
        if self.jugador.defendiendo: self._log(f"  🛡 Bloqueaste parte del daño!",C["hielo"])
        self.jugador.defendiendo=False
        self._log(f"  ☠  {r['msg']}  [{r['dano']} dmg]",C["rojo2"] if r["tipo"]=="critico" else C["rojo"])
        self._ui(); self.after(200,self._fin_combate)

    def _fin_combate(self):
        if not self.jugador.esta_vivo(): self._derrota(); return
        if not self.enemigo.esta_vivo():
            self.jugador.puntos+=1
            self._log(f"\n  🌟 ¡Victoria en el Combate {self.ring}! (+1 punto)",C["oro"])
            self._ui(); self.after(700,self._sig_ring)
        else:
            self._on()

    def _sig_ring(self):
        if self.ring<3:
            if self.jugador.vida<self.jugador.vida_maxima:
                r=random.randint(10,20); self.jugador.vida=min(self.jugador.vida+r,self.jugador.vida_maxima)
                self._log(f"  💚 Recuperas {r} de vida entre combates.",C["verde2"])
            self.ring+=1; self._nuevo_enemigo()
            self._log(f"\n  ⚔ Combate {self.ring}/3 — {self.enemigo.nombre}",C["oro"])
            self._ui(); self._on()
        else:
            if self.jugador.vida<self.jugador.vida_maxima:
                r=random.randint(25,40); self.jugador.vida=min(self.jugador.vida+r,self.jugador.vida_maxima)
                self._log(f"  💚 Recuperación: +{r} vida.",C["verde2"])
            self.idx+=1
            if self.idx>=len(self.enemigos): self._victoria(); return
            self.ring=1; self._nuevo_enemigo()
            self._log(f"\n  ══ NUEVO ADVERSARIO: {LOGO(self.enemigo.nombre)} {self.enemigo.nombre} ══",C["oro"])
            self._ui(); self._on()

    def _sig_ring_forzado(self):
        if self.ring<3: self.ring+=1
        else:
            self.idx+=1
            if self.idx>=len(self.enemigos): self._victoria(); return
            self.ring=1
        self._nuevo_enemigo()
        self._log(f"  ⚔ Siguiente: {self.enemigo.nombre}",C["oro"])
        self._ui(); self._on()

    # ══════════ HIGHSCORES ══════════
    def _hs_win(self):
        win=tk.Toplevel(self); win.title("Salón de la Fama"); win.geometry("360,400".replace(",","x"))
        win.geometry("360x400"); win.configure(bg=C["panel"]); win.resizable(False,False)
        win.grab_set(); win.transient(self)
        tk.Label(win,text="🏆 SALÓN DE LA FAMA",font=self.FS,bg=C["panel"],fg=C["oro"]).pack(pady=(18,4))
        self._sep(win,px=30)
        hs=cargar_hs()
        medallas=["🥇","🥈","🥉"]+["  "]*17
        if not hs:
            tk.Label(win,text="Aún no hay registros.",font=self.FC,bg=C["panel"],fg=C["dim"]).pack(pady=20)
        for i,(nombre,pts) in enumerate(hs[:10]):
            row=tk.Frame(win,bg=C["card"],highlightbackground=C["borde"],highlightthickness=1)
            row.pack(fill="x",padx=24,pady=2)
            col=C["oro"] if i==0 else (C["gris"] if i>2 else C["texto"])
            tk.Label(row,text=f"{medallas[i]} {i+1:2}. {nombre:<16}",font=self.FC,bg=C["card"],fg=col).pack(side="left",padx=8,pady=5)
            tk.Label(row,text=f"{pts} pts",font=tkfont.Font(family="Courier",size=9,weight="bold"),
                     bg=C["card"],fg=C["oro2"]).pack(side="right",padx=8)
        self._btn(win,"Cerrar",C["borde"],win.destroy,fg=C["dim"]).pack(pady=14,ipadx=14,ipady=6)

    # ══════════ FIN ══════════
    def _derrota(self):
        guardar_puntuacion(self.jugador.nombre,self.jugador.puntos)
        self._limpiar()
        f=tk.Frame(self,bg=C["bg"]); f.place(relx=.5,rely=.5,anchor="center")
        tk.Label(f,text="☠",font=tkfont.Font(size=60),bg=C["bg"]).pack()
        tk.Label(f,text="HAS CAÍDO EN COMBATE",font=tkfont.Font(family="Georgia",size=20,weight="bold"),
                 bg=C["bg"],fg=C["rojo2"]).pack(pady=6)
        tk.Label(f,text=f"{self.jugador.nombre}  —  {self.jugador.puntos} victorias",
                 font=self.FS,bg=C["bg"],fg=C["dim"]).pack()
        self._sep(f,C["rojo"])
        self._btn(f,"⚔  JUGAR DE NUEVO",C["rojo"],self._pantalla_inicio).pack(ipadx=20,ipady=10,pady=10)
        self._btn(f,"🏆  SALÓN DE LA FAMA",C["borde"],self._hs_win,fg=C["oro"]).pack(ipadx=14,ipady=7)

    def _victoria(self):
        guardar_puntuacion(self.jugador.nombre,self.jugador.puntos)
        self._limpiar()
        f=tk.Frame(self,bg=C["bg"]); f.place(relx=.5,rely=.5,anchor="center")
        tk.Label(f,text="👑",font=tkfont.Font(size=60),bg=C["bg"]).pack()
        tk.Label(f,text="EL TRONO ES TUYO",font=tkfont.Font(family="Georgia",size=22,weight="bold"),
                 bg=C["bg"],fg=C["oro"]).pack(pady=6)
        tk.Label(f,text=f"¡{self.jugador.nombre} domina los Siete Reinos!",
                 font=self.FS,bg=C["bg"],fg=C["gris2"]).pack()
        tk.Label(f,text=f"Victorias: {self.jugador.puntos}",
                 font=tkfont.Font(family="Georgia",size=15,weight="bold"),
                 bg=C["bg"],fg=C["oro2"]).pack(pady=6)
        self._sep(f,C["oro"])
        self._btn(f,"⚔  JUGAR DE NUEVO",C["oro"],self._pantalla_inicio,fg=C["bg"]).pack(ipadx=20,ipady=10,pady=10)
        self._btn(f,"🏆  SALÓN DE LA FAMA",C["borde"],self._hs_win,fg=C["oro"]).pack(ipadx=14,ipady=7)