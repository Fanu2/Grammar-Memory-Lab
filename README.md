# Grammar Memory Lab 3.0 — Complete Grammar Edition

**Final content-focused release.**

The stable v2.1.1 learning architecture has been preserved in spirit and expanded with a comprehensive external grammar curriculum.

## Coverage

- English: 30 structured lessons
- Spanish: 30 structured lessons
- French: 30 structured lessons
- Levels A1 through C1
- 90 lessons total
- Hundreds of example sentences, mistakes and recall prompts

Every lesson contains:
- Rule
- When to use
- Formation / pattern
- Memory hook
- Multiple example sentences
- Common mistakes
- Recall questions
- Level

## Main learning cycle

**Learn → Understand → Remember → Recall → Rate → Review**

## Application features

- Language selector
- Structured grammar curriculum
- Practice questions
- Again / Hard / Good / Easy mastery rating
- Persistent local progress
- Recall accuracy
- Streak
- Review dashboard
- Cross-language comparison
- Personal memory notes
- Modern PySide6 UI

## Run on Windows

```powershell
cd "C:\Users\singh\Downloads\Grammar_Memory_Lab_3.0_Complete"
py -m pip install PySide6
py grammar_memory_lab.py
```

Progress is stored locally in `grammar_progress.json`.

## Important

The grammar database is separated into `data/grammar.json`, so future content corrections or additions do not require rewriting the application.

## Final-version philosophy

The application should now be treated as a **stable learning platform**. Future work should primarily be:
1. grammar corrections,
2. additional verified examples,
3. content expansion,
4. bug fixes.

Avoid unnecessary UI/architecture rewrites.
