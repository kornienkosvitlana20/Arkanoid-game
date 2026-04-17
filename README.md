# Arkanoid — Python + Pygame

> Лабораторна робота: Pipeline CI/CD — Plan, Code, Build  
> Гра: **Arkanoid** | Рівень: Стандартний 

---

## Команда

| Учасник | Гілка | Відповідальність |
|---------|-------|-----------------|
| **Player 1** (Корнієнко Світлана) | `feature/game-logic` | Ігрова логіка: Ball, Paddle, Brick, BrickGrid, Game |
| **Player 2** (Вялкова Поліна) | `feature/ui-graphics` | UI/Графіка: UI (HUD, меню, екрани), Settings, main.py |

---

## Архітектура (UML)

```
main.py
  └── Game (game.py)
        ├── Settings (settings.py)       ← конфіг, аргументи CLI
        ├── Ball (ball.py)               ← фізика м'яча
        ├── Paddle (paddle.py)           ← керування платформою
        ├── BrickGrid (brick_grid.py)    ← сітка цеглин
        │     └── Brick (brick.py)      ← одна цеглина
        └── UI (ui.py)                  ← весь інтерфейс
```

**Принципи проектування:**
- **DRY** — кольори, розміри, швидкості зібрані в `Settings`, не дублюються
- **KISS** — кожен клас відповідає за одну річ
- **SOLID** — Single Responsibility: `Ball` = фізика, `UI` = рендер, `Game` = стан

---

## Запуск

### Встановлення

```bash
git clone https://github.com/<your-org>/arkanoid.git
cd arkanoid
pip install -r requirements.txt
```

### Запуск

```bash
cd src
python main.py
```

### Аргументи командного рядка (argparse)

```bash
# Складність
python main.py --difficulty easy
python main.py --difficulty medium   # за замовчуванням
python main.py --difficulty hard

# Колір фону
python main.py --bg-color dark_blue    # за замовчуванням
python main.py --bg-color black
python main.py --bg-color dark_purple
python main.py --bg-color dark_green

# Кількість життів
python main.py --lives 5

# Повноекранний режим
python main.py --fullscreen

# Комбінація
python main.py --difficulty hard --bg-color dark_purple --lives 1
```

---

## Керування

| Клавіша | Дія |
|---------|-----|
| `←` / `→` або `A` / `D` | Рух платформи |
| Миша | Керування платформою |
| `SPACE` | Запустити м'яч / Продовжити |
| `P` | Пауза / Зняти паузу |
| `R` | Рестарт (після програшу/перемоги) |
| `ESC` | Вийти |

---

## Структура проекту

```
arkanoid/
├── src/
│   ├── main.py          # Точка входу, argparse
│   ├── game.py          # Головний ігровий цикл і стани
│   ├── settings.py      # Всі налаштування
│   ├── ball.py          # Логіка м'яча і фізика
│   ├── paddle.py        # Логіка платформи
│   ├── brick.py         # Цеглина (одна)
│   ├── brick_grid.py    # Сітка цеглин
│   └── ui.py            # Весь графічний інтерфейс
├── docs/
│   ├── use_case.md      # Діаграма варіантів використання
│   ├── activity.md      # Діаграма діяльності
│   └── class.md         # Діаграма класів
├── requirements.txt
└── README.md
```

---

## Git Workflow 

### Перший раз (Player 1 — створює репозиторій)

```bash
git init
git add .
git commit -m "chore: initial project structure"
git branch -M main
git remote add origin https://github.com/<your-org>/arkanoid.git
git push -u origin main
```

### Player 1 — Ігрова логіка 

```bash
git checkout -b feature/game-logic

# Коміт 1: базові класи
git add src/ball.py src/paddle.py
git commit -m "feat(logic): add Ball and Paddle classes with basic movement"

# Коміт 2: логіка цеглин
git add src/brick.py src/brick_grid.py
git commit -m "feat(logic): implement Brick with HP system and BrickGrid generator"

# Коміт 3: колізії м'яча з цеглинами
git add src/ball.py
git commit -m "feat(logic): add ball-brick collision detection with reflection"

# Коміт 4: колізія з платформою
git add src/ball.py
git commit -m "feat(logic): add angle-based paddle collision for ball control"

# Коміт 5: втрата м'яча
git add src/ball.py
git commit -m "feat(logic): implement ball lost detection"

# Коміт 6: система підрахунку очок
git add src/brick.py src/game.py
git commit -m "feat(logic): add scoring system based on brick HP"

# Коміт 7: рівні складності
git add src/settings.py
git commit -m "feat(logic): implement difficulty levels with speed scaling"

# Коміт 8: зростання швидкості м'яча
git add src/ball.py
git commit -m "feat(logic): ball speed increases gradually per hit"

# Коміт 9: багаторівнева гра
git add src/game.py
git commit -m "feat(logic): add multi-level progression (3 levels)"

# Коміт 10: стани гри і GameState
git add src/game.py
git commit -m "feat(logic): implement GameState machine (start, playing, paused, game_over, win)"

git push origin feature/game-logic
```

### Player 2 — UI/Graphics ( Діаграми)

```bash
git checkout main
git pull
git checkout -b feature/ui-graphics

# Коміт 1: налаштування і конфіг
git add src/settings.py
git commit -m "feat(ui): add Settings class with all game constants"

# Коміт 2: фон і сітка
git add src/ui.py
git commit -m "feat(ui): implement background rendering with grid effect"

# Коміт 3: HUD (score, lives, level)
git add src/ui.py
git commit -m "feat(ui): add HUD with score, lives hearts, level and difficulty"

# Коміт 4: стартовий екран
git add src/ui.py
git commit -m "feat(ui): create start screen overlay with controls info"

# Коміт 5: екран паузи
git add src/ui.py
git commit -m "feat(ui): add pause screen overlay"

# Коміт 6: екрани game over і перемоги
git add src/ui.py
git commit -m "feat(ui): implement game over and win screen with final score"

# Коміт 7: відображення м'яча з glow-ефектом
git add src/ball.py
git commit -m "feat(ui): add glow and shine effect to ball rendering"

# Коміт 8: відображення платформи з highlight
git add src/paddle.py
git commit -m "feat(ui): add highlight and border to paddle drawing"

# Коміт 9: відображення цеглин з crack effect
git add src/brick.py
git commit -m "feat(ui): add crack effect on damaged bricks and color fade"

# Коміт 10: argparse і main.py
git add src/main.py
git commit -m "feat(ui): add argparse for difficulty, bg-color, lives, fullscreen"

git push origin feature/ui-graphics
```

### Злиття гілок (разом)

```bash
git checkout main
git pull

# Merge Player 1
git merge feature/game-logic
git push

# Merge Player 2
git merge feature/ui-graphics
# Вирішити конфлікти якщо є, потім:
git add .
git commit -m "merge: combine game-logic and ui-graphics branches"
git push
```

---

## Етапи Pipeline CI/CD

### Plan
- Аналіз гри Arkanoid
- Розподіл ролей між учасниками
- Діаграми: варіантів використання, діяльності, класів

### Code
- Розробка у гілках `feature/game-logic` та `feature/ui-graphics`
- Мінімум 10 комітів від кожного учасника
- Pull Request і Code Review перед злиттям

### Build
- `pip install -r requirements.txt`
- `python src/main.py`
- Перевірка запуску з різними аргументами CLI

---

## Вимоги до оцінювання

- [x] Графічний інтерфейс (pygame)
- [x] Принципи DRY, KISS, SOLID
- [x] Argparse (складність, колір, кількість життів, fullscreen)
- [x] Git: гілки, мінімум 10 комітів від кожного
- [x] Злиття гілок
