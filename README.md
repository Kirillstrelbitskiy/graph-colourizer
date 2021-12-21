# Graph Colourizer
Алгоритм, що розмальовує кожну вершину неорієнтованого граф в один з трьох кольорів `(червоний, зелений, синій)`, крім того який був початковим для певної вершини.
Після виконання основної функції, повертається список пар `(номер вершини, новий колір)`.

**Автори:**
- Стрельбицький Кирило
- Краснянський Тимур
- Ніколайченко Іван
- Марків Олена
- Сітарчук Марія

## Запуск модуля
Для запуску модуля необхідно виконати
```console
$ python3 main.py -file /path_to_graph
```
Де `/path_to_graph` - шлях до **csv** файлу, що зберігає граф.

## Формат введення графу
Нехай в графі **n** вершин, тоді кожній вершині відповідає номер **v<sub>i</sub>** такий, що <code>1 ≤ v<sub>i</sub> ≤ n</code>.<br>Кольори задаються латинськими літерами `R, G, B`, які позначають червоний, зелений і синій кольори відповідно.<br>
Граф задається через **csv** файл, що має таку структуру колонок: 
1. перша вершина ребра
2. друга вершина ребра
3. колір першої вершини
4. колір другої вершини.

## Аналіз задачі
Кожна вершина графа має бути розфарбована в один з трьох кольорів. Розглянемо деяку вершину **a** і введемо булеві змінні <code>a<sub>r</sub>, a<sub>g</sub>, a<sub>b</sub></code>, тоді:
- якщо для a обрано червоний колір, то змінна <code>a<sub>r</sub> = true, a<sub>g</sub> = false, a<sub>b</sub> = false</code>.
- якщо для a обрано зелений колір, то змінна <code>a<sub>r</sub> = false, a<sub>g</sub> = true, a<sub>b</sub> = false</code>.
- якщо для a обрано синій колір, то змінна <code>a<sub>r</sub> = false, a<sub>g</sub> = false, a<sub>b</sub> = true</code>.

### Умови існування валідного розфарбування
1. Обмеження, що дві вершини, наприклад **a** і **b**, з'єднані ребром `(a, b)` не можуть бути одного кольори, можна записати так:
<code>(~a<sub>r</sub> ∨ ~b<sub>r</sub>) ∧ (~a<sub>g</sub> ∨ ~b<sub>g</sub>) ∧ (~a<sub>b</sub> ∨ ~b<sub>b</sub>)</code>.
2. Кожна вершина повинна бути пофарбовано в якийсь колір, отже
<code>(a<sub>r</sub> ∨ a<sub>g</sub> ∨ a<sub>b</sub>)</code>.
3. Кожна вершина має бути пофарбована лише в один колір
<code>(~a<sub>r</sub> ∨ ~a<sub>g</sub>) ∧ (~a<sub>g</sub> ∨ ~a<sub>b</sub>) ∧ (~a<sub>r</sub> ∨ ~a<sub>b</sub>)</code>.

Ми отримали умови для кожної **вершини** та **ребра**.

### Знаходження значень змінних
Для знаходження значень кожної з змінних, застосуємо принципи розв'язку **2-SAT** задачі.<br>
Перепишем диз'юнкції у вигляді імплікацій застошувавши перетворення 
`a ∨ b` еквівалентно `(~a⇒b) ∧ (~b⇒a)`. Та побудуємо орієнтований граф імплікацій, в якому ребро <code>(x<sub>1</sub>, x<sub>2</sub>)</code> позначає імплікацію <code>x<sub>1</sub>⇒x<sub>2</sub></code>.<br>

Умови **1** та **3** переписати в такий вигляд можливо, але умова **2** має вигляд виразу в формі **3-SAT**. Задача **3-SAT** є NP-повною, тож не може бути розв’язана за поліноміальний час. Отже нам треба звести умову до **2-SAT** задачі, і для цього ми використаємо факт наданий в умові – *кожна вершина не може бути пофарбована в початковий колір*.<br>

Використання цього факту дає нам можливість виключити з розгляду одну вершину, адже якщо цей колір використовувати **не можна**, її значення одразу є `false` і не впливатиме на рішення. Через ту саму причину, не будемо включати в граф імплікацій ребра, які є інцидентними до забороненої вершини.
Отже ми отримаємо нові умови, де <code>a<sub>1</sub></code> і <code>a<sub>2</sub></code> позначають перший та другий дозволені кольори:
1. <code>(~a<sub>1</sub> ∨ ~b<sub>2</sub>) ∧ (~a<sub>1</sub> ∨ ~b<sub>2</sub>)</code>
2. <code>(a<sub>1</sub> ∨ a<sub>2</sub>)</code>
3. <code>(~a<sub>1</sub> ∨ ~a<sub>2</sub>)</code>.

Побудувавши граф імплікацій, ми можемо використати розв'язок **2-SAT** для знаходження значень кожної вершини графу імплікацій, які б задовольняли накладеним умовам, та отримати рішення за поліноміальний час. 

### Визначення кольорів
Тепер якщо значення <code>a<sub>r</sub> = true</code> і червоний не є заблокованим кольором для цієї вершини, то перефарбувати цю вершину потрібно в червоний.<br>
**Так само перевіряємо інші кольори для всіх вершин графу.**

## Реалізація

### Функція запиту в користувача шляху до файлу з графом
```python
def parse_file_path()
```
Пробує отримати файл заданий аргументом під час запуску модуля. Якщо аргумент пустий, то пробує знайти файл `graph.csv`. Перевіряє існування файлу за цим шляхом. Якщо файл існує, то функція повертає шлях до нього, інакше виводить повідомлення та завершує виконання програми.


### Функція для читання графу з файлу
```python
def read_data(file_path, colors_names)
```
Отримує шлях до файлу з графом та назнчені абревіатури для кольорів. Після цього читає граф з заданого файлу та повертає його у вигляді списку пар, що позначають ребро. Також функція повертає масив початкових кольорів, для кожної вершини.


### Основна функція, яка відповідає за організацію взаємодії між іншими функціями
```python
def colourize_graph(initial_graph, initial_colors, colors_names):
    num_colors = 3

    implications_graph = build_implications_graph(
        initial_graph, initial_colors, num_colors)

    two_sat_solution = find_2_sat(implications_graph)

    if two_sat_solution == None:
        print("No solution")
        return

    ans_colors = find_colors(
        two_sat_solution, initial_colors, num_colors, colors_names)

    return ans_colors
```
Отримує від `build_implications_graph` граф імплікацій, який потім передається в `find_2_sat`. Рішення отримане від `find_2_sat` передається `find_colors`, яка повертає розмалювання графу, якщо воно існує.


### Функція, що будує граф імплікацій
```python
def build_implications_graph(initial_graph, initial_colors, num_colors)
```
Функція отримує неорієнтований граф, а повертає граф імплікацій, що задовільняє всім трьом умовам та є підготованим для використання в `find_2_sat`.

### Функція для знаходження розв'язку 2-SAT задачі
```python
def find_2_sat(graph)
```
Отримує підготовлений граф імплікацій, а повертає значення `True|False` для кожної вершини або `None`, якщо рішення **не** існує. 
Для пошуку рішення використовується 'Kosaraju's algorithm'.


### Функція для виконання топологічного сортування
```python
def dfs_type_1(graph)
```
Є допоміжною функцію для `find_2_sat` та виконує ітеративне топологічне сортування.
> Використання ітеративної реалізації було зумовленно обмеженням на глибину рекурсії в `1,000` заходів.


### Функція для виконання пошуку компонент зв'язності
```python
def dfs_type_2(start, color, components, graph)
```
Є допоміжною функцію для `find_2_sat` та виконує ітеративний пошук в глибину під час якого, помічає всі вершини, що належать поточній компоненті.
> Використання ітеративної реалізації було зумовленно обмеженням на глибину рекурсії в `1,000` заходів.

### Функція пошуку фінального розмалювання
```python
def find_colors(sat_solution, init_colors, num_colors, colors_names)
```
Отримає рішення від `find_2_sat`, а повертає список пар `(вершина, колір)`.

### Функція розрахунку позицій вершини
```python
def vertex_idx(vertex, color, opp, num_colors)
```
Кожній вершині з певним кольором початкового графу відповідає індекс розрахований за формулою<br>
```
index = vertex_idx * number_colors * 2 + choosen_color * 2 + is_it_~
```

## Висновки
Було реалізовано проект, що виконує поставлену задачу.<br>
Алгоритм було протестовано на сгенерованих великих тестах.<br>
Часова складність отриманого алгоритма складає: `O(n + m)`, де `n` - кількість вершин, `m` - кількість ребер.