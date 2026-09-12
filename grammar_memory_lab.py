import sys, json, random
from pathlib import Path
from PySide6.QtWidgets import QApplication,QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QLabel,QPushButton,QComboBox,QTabWidget,QFrame,QRadioButton,QLineEdit,QListWidget,QProgressBar,QSpinBox
from PySide6.QtCore import Qt

BASE=Path(__file__).parent
DATA=json.loads((BASE/"data/grammar.json").read_text(encoding="utf-8"))

class GrammarLab(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧠 Grammar Memory Lab 3.0 — Complete Grammar Edition")
        self.resize(1450,900)
        self.lang="English"; self.i=0; self.score=0; self.total=0; self.streak=0
        self.mastery={}; self.notes={}; self.load_state(); self.build_ui(); self.load_lesson()

    def load_state(self):
        p=BASE/"grammar_progress.json"
        if p.exists():
            try:
                d=json.loads(p.read_text(encoding="utf-8"))
                self.mastery=d.get("mastery",{}); self.notes=d.get("notes",{})
                self.score=d.get("score",0); self.total=d.get("total",0)
            except Exception: pass

    def save_state(self):
        (BASE/"grammar_progress.json").write_text(json.dumps({
            "mastery":self.mastery,"notes":self.notes,"score":self.score,"total":self.total
        },ensure_ascii=False,indent=2),encoding="utf-8")

    def build_ui(self):
        c=QWidget(); self.setCentralWidget(c); main=QVBoxLayout(c); main.setContentsMargins(24,20,24,18)
        head=QHBoxLayout(); titles=QVBoxLayout()
        title=QLabel("🧠 Grammar Memory Lab 3.0"); title.setObjectName("title")
        sub=QLabel("Complete Grammar Edition  •  Learn → Understand → Remember → Recall")
        sub.setObjectName("sub"); titles.addWidget(title); titles.addWidget(sub); head.addLayout(titles); head.addStretch()
        head.addWidget(QLabel("LANGUAGE")); self.langbox=QComboBox(); self.langbox.addItems(DATA)
        self.langbox.currentTextChanged.connect(self.change_lang); head.addWidget(self.langbox); main.addLayout(head)
        self.tabs=QTabWidget(); main.addWidget(self.tabs,1)

        learn=QWidget(); l=QVBoxLayout(learn)
        top=QHBoxLayout(); self.topic=QLabel(); self.topic.setObjectName("section"); self.counter=QLabel()
        top.addWidget(self.topic); top.addStretch(); top.addWidget(self.counter); l.addLayout(top)
        self.card=QFrame(); self.card.setObjectName("card"); cl=QVBoxLayout(self.card)
        self.rule=QLabel(); self.rule.setWordWrap(True); self.rule.setObjectName("rule")
        self.use=QLabel(); self.use.setWordWrap(True); self.use.setObjectName("use")
        self.form=QLabel(); self.form.setWordWrap(True); self.form.setObjectName("form")
        self.hook=QLabel(); self.hook.setWordWrap(True); self.hook.setObjectName("hook")
        self.examples=QLabel(); self.examples.setWordWrap(True); self.examples.setObjectName("examples")
        self.mistakes=QLabel(); self.mistakes.setWordWrap(True); self.mistakes.setObjectName("mistakes")
        for x in (self.rule,self.use,self.form,self.hook,self.examples,self.mistakes): cl.addWidget(x)
        l.addWidget(self.card,1)
        nav=QHBoxLayout()
        for text,fn in [("← Previous",self.prev),("Next →",self.next)]:
            b=QPushButton(text); b.clicked.connect(fn); nav.addWidget(b)
        nav.addStretch()
        practice=QPushButton("🧠 Practice This Rule"); practice.clicked.connect(lambda:self.tabs.setCurrentIndex(1)); nav.addWidget(practice)
        l.addLayout(nav); self.tabs.addTab(learn,"  Learn  ")

        practice=QWidget(); p=QVBoxLayout(practice)
        ph=QHBoxLayout(); qt=QLabel("🎯 Recall Practice"); qt.setObjectName("section"); self.stats=QLabel()
        ph.addWidget(qt); ph.addStretch(); ph.addWidget(self.stats); p.addLayout(ph)
        self.question=QLabel(); self.question.setWordWrap(True); self.question.setObjectName("question"); p.addWidget(self.question)
        self.opts=QVBoxLayout(); p.addLayout(self.opts)
        self.answerbox=QLineEdit(); self.answerbox.setPlaceholderText("Optional: type the answer from memory before choosing…"); p.addWidget(self.answerbox)
        cb=QHBoxLayout(); self.check=QPushButton("✓ Check"); self.check.clicked.connect(self.check_answer); cb.addWidget(self.check)
        self.feedback=QLabel(); self.feedback.setWordWrap(True); self.feedback.setObjectName("feedback"); p.addWidget(self.feedback)
        for txt,val in [("Again",-2),("Hard",-1),("Good",1),("Easy",2)]:
            b=QPushButton(txt); b.clicked.connect(lambda _,v=val:self.rate(v)); cb.addWidget(b)
        p.addLayout(cb); nxt=QPushButton("↻ New Question"); nxt.clicked.connect(self.new_question); p.addWidget(nxt,alignment=Qt.AlignRight)
        self.tabs.addTab(practice,"  Practice  ")

        review=QWidget(); r=QVBoxLayout(review)
        rh=QHBoxLayout(); rr=QLabel("📚 Review Dashboard"); rr.setObjectName("section"); rh.addWidget(rr); rh.addStretch()
        self.filter=QComboBox(); self.filter.addItems(["All languages","English","Spanish","French"]); self.filter.currentTextChanged.connect(self.build_review); rh.addWidget(self.filter); r.addLayout(rh)
        self.reviewlist=QListWidget(); r.addWidget(self.reviewlist,1)
        self.bar=QProgressBar(); r.addWidget(self.bar); self.reviewtext=QLabel(); r.addWidget(self.reviewtext)
        self.tabs.addTab(review,"  Review  ")

        compare=QWidget(); co=QVBoxLayout(compare); ct=QLabel("🌍 Compare Grammar Across Languages"); ct.setObjectName("section"); co.addWidget(ct)
        self.compare=QListWidget(); co.addWidget(self.compare,1); self.tabs.addTab(compare,"  Compare  ")

        notes=QWidget(); no=QVBoxLayout(notes); nt=QLabel("📝 My Memory Note"); nt.setObjectName("section"); no.addWidget(nt)
        self.note=QLineEdit(); self.note.setPlaceholderText("Write your own memory trick, example or reminder…"); no.addWidget(self.note)
        sb=QPushButton("Save Note"); sb.clicked.connect(self.save_note); no.addWidget(sb); no.addStretch(); self.tabs.addTab(notes,"  My Notes  ")

        self.setStyleSheet("""QMainWindow,QWidget{background:#0d1117;color:#edf2f7}
        QLabel#title{font-size:31px;font-weight:800} QLabel#sub{color:#94a3b8;font-size:14px}
        QLabel#section{font-size:23px;font-weight:800} QFrame#card{background:#171d27;border:1px solid #2c3747;border-radius:16px;padding:18px}
        QLabel#rule{background:#202938;border-radius:10px;padding:14px;color:#c4b5fd;font-size:17px}
        QLabel#use{background:#172b27;border-radius:10px;padding:13px;color:#9fe3c0}
        QLabel#form{background:#202731;border-radius:10px;padding:13px}
        QLabel#hook{background:#352b16;border:1px solid #725d28;border-radius:10px;padding:14px;color:#f5d78e;font-size:18px;font-weight:750}
        QLabel#examples{font-size:17px;padding:10px} QLabel#mistakes{background:#2b1d24;border-radius:10px;padding:13px;color:#ffb4c0}
        QLabel#question{font-size:25px;font-weight:750;padding:18px} QLabel#feedback{background:#202731;border-radius:10px;padding:14px}
        QPushButton{background:#202834;border:1px solid #394658;border-radius:9px;padding:10px 15px;color:#f4f7fa;font-weight:650}
        QPushButton:hover{background:#303b4c} QComboBox,QLineEdit{background:#202834;border:1px solid #394658;border-radius:8px;padding:9px}
        QTabWidget::pane{border:1px solid #293342;border-radius:10px} QTabBar::tab{background:#171d27;padding:11px 20px;border-radius:8px;margin-right:3px}
        QTabBar::tab:selected{background:#6d4aff;color:white} QListWidget{background:#171d27;border:1px solid #2c3747;border-radius:10px;padding:8px}
        QRadioButton{padding:7px;font-size:16px} QProgressBar{border:1px solid #394658;border-radius:7px;text-align:center;height:23px}""")

    def current(self): return DATA[self.lang][self.i]

    def load_lesson(self):
        r=self.current()
        self.topic.setText(f"{r['topic']}   ·   {r['level']}")
        self.counter.setText(f"Lesson {self.i+1} of {len(DATA[self.lang])}")
        self.rule.setText("📘 RULE\n"+r["rule"]); self.use.setText("🎯 WHEN TO USE\n"+r["use"])
        self.form.setText("🔧 FORMATION / PATTERN\n"+r["formation"])
        self.hook.setText("🧠 MEMORY HOOK\n"+r["hook"])
        self.examples.setText("💬 SENTENCES\n"+"\n".join("• "+x for x in r["examples"]))
        self.mistakes.setText("⚠ COMMON MISTAKES\n"+"\n".join("• "+x for x in r["mistakes"]))
        key=self.lang+":"+r["topic"]; self.note.setText(self.notes.get(key,""))
        self.new_question(); self.build_review(); self.build_compare()

    def new_question(self):
        self.current_question=random.choice(self.current()["questions"])
        self.question.setText(self.current_question[0]); self.answerbox.clear(); self.feedback.clear(); self.check.setEnabled(True)
        while self.opts.count():
            z=self.opts.takeAt(0)
            if z.widget(): z.widget().deleteLater()
        self.radios=[]
        for option in self.current_question[1]:
            x=QRadioButton(option); self.opts.addWidget(x); self.radios.append(x)
        self.stats.setText(f"Score {self.score}/{self.total}  •  Streak {self.streak}")

    def check_answer(self):
        chosen=next((i for i,x in enumerate(self.radios) if x.isChecked()),None)
        if chosen is None:
            self.feedback.setText("Choose an answer first."); return
        correct=chosen==self.current_question[2]; key=self.lang+":"+self.current()["topic"]
        self.total+=1
        if correct:
            self.score+=1; self.streak+=1; self.feedback.setText("✅ Correct — excellent recall.")
        else:
            self.streak=0; self.feedback.setText("❌ Not quite. Re-read the memory hook and review the examples.")
        self.check.setEnabled(False); self.save_state(); self.stats.setText(f"Score {self.score}/{self.total}  •  Streak {self.streak}")

    def rate(self,v):
        key=self.lang+":"+self.current()["topic"]; self.mastery[key]=self.mastery.get(key,0)+v
        self.save_state(); self.build_review()

    def save_note(self):
        self.notes[self.lang+":"+self.current()["topic"]]=self.note.text(); self.save_state()

    def change_lang(self,x): self.lang=x; self.i=0; self.load_lesson()
    def next(self): self.i=(self.i+1)%len(DATA[self.lang]); self.load_lesson(); self.tabs.setCurrentIndex(0)
    def prev(self): self.i=(self.i-1)%len(DATA[self.lang]); self.load_lesson(); self.tabs.setCurrentIndex(0)

    def build_review(self):
        self.reviewlist.clear(); selected=self.filter.currentText() if hasattr(self,"filter") else "All languages"
        for lang,lessons in DATA.items():
            if selected!="All languages" and lang!=selected: continue
            for r in lessons:
                v=self.mastery.get(lang+":"+r["topic"],0)
                icon="🟢" if v>=3 else "🟡" if v>=0 else "🔴"
                self.reviewlist.addItem(f"{icon} {lang}  •  {r['level']}  •  {r['topic']}    mastery {v}")
        pct=round(self.score/self.total*100) if self.total else 0
        self.bar.setValue(pct); self.reviewtext.setText(f"Recall accuracy: {pct}%   •   {self.reviewlist.count()} lessons shown")

    def build_compare(self):
        self.compare.clear()
        topic=self.current()["topic"]; self.compare.addItem("Concept: "+topic)
        for lang,lessons in DATA.items():
            hit=next((x for x in lessons if x["topic"].lower()==topic.lower()),None)
            self.compare.addItem(lang+": "+(hit["rule"] if hit else "This exact topic has a different structure in this curriculum."))

if __name__=="__main__":
    app=QApplication(sys.argv); w=GrammarLab(); w.show(); sys.exit(app.exec())
