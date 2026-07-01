from collections import deque

class AhoCorasickNode:
    _id_counter = 0

    def __init__(self, char="#"):
        self.id = AhoCorasickNode._id_counter
        AhoCorasickNode._id_counter += 1
        self.char = char
        self.transitions = {}
        self.parts_info = []
        self.suff_link = None
        self.exit_link = None

def build_trie(parts):
    AhoCorasickNode._id_counter = 0
    root = AhoCorasickNode()
    
    print("--- 1. Построение бора (TRIE) ---")
    for idx, (pattern, offset) in enumerate(parts, 1):
        print(f"\nДобавляем подстроку №{idx}: '{pattern}' (смещение в шаблоне: {offset})")
        curr = root
        for char in pattern:
            if char not in curr.transitions:
                new_node = AhoCorasickNode(char)
                curr.transitions[char] = new_node
                print(f"  Создаем новый узел №{new_node.id} по символу '{char}' из узла №{curr.id}")
            else:
                print(f"  Переходим в существующий узел №{curr.transitions[char].id} по символу '{char}'")
            curr = curr.transitions[char]
        curr.parts_info.append((offset, len(pattern)))
        print(f"  Узел №{curr.id} становится терминальным для подстроки '{pattern}'")
    return root

def build_automaton(root):
    print("\n--- 2. Построение суффиксных и конечных ссылок (BFS) ---")
    queue = deque()
    
    for char, child in root.transitions.items():
        child.suff_link = root
        child.exit_link = None
        print(f"Узел первого уровня №{child.id} ('{char}'): суф. ссылка -> Корень №{root.id}")
        queue.append(child)
        
    while queue:
        curr = queue.popleft()
        for char, child in curr.transitions.items():
            temp = curr.suff_link
            while temp is not None and char not in temp.transitions:
                temp = temp.suff_link
            
            if temp is None:
                child.suff_link = root
            else:
                child.suff_link = temp.transitions[char]
            
            suff = child.suff_link
            if suff.parts_info:
                child.exit_link = suff
            else:
                child.exit_link = suff.exit_link
                
            print(f"Узел №{child.id} ('{char}'): "
                  f"суф. ссылка -> №{child.suff_link.id}, "
                  f"кон. ссылка -> №{child.exit_link.id if child.exit_link else 'None'}")
            queue.append(child)

def get_all_nodes(root):
    """Сбор всех вершин автомата для анализа структуры"""
    nodes = []
    queue = deque([root])
    while queue:
        curr = queue.popleft()
        nodes.append(curr)
        for child in curr.transitions.values():
            queue.append(child)
    return nodes

def calculate_longest_chains(root):
    """Реализация Варианта 3: вычисление максимальных длин цепочек ссылок"""
    nodes = get_all_nodes(root)
    max_suff_chain = 0
    max_exit_chain = 0
    
    for node in nodes:
        suff_len = 0
        curr = node.suff_link
        while curr is not None and curr != root:
            suff_len += 1
            curr = curr.suff_link
        if curr == root:
            suff_len += 1
        max_suff_chain = max(max_suff_chain, suff_len)
        
        exit_len = 0
        curr = node.exit_link
        while curr is not None:
            exit_len += 1
            curr = curr.exit_link
        max_exit_chain = max(max_exit_chain, exit_len)
        
    return max_suff_chain, max_exit_chain

def search_text(text, root, pattern_len, C):
    print("\n--- 3. Процесс поиска в тексте ---")
    n = len(text)
    curr = root
    for i in range(n):
        char = text[i]
        print(f"Символ [{i+1}]: '{char}'. Текущий узел автомата: №{curr.id}")
        
        while curr is not None and char not in curr.transitions:
            print(f"  Нет перехода по '{char}'. Откатываемся: №{curr.id} -> №{curr.suff_link.id if curr.suff_link else 'None'}")
            curr = curr.suff_link
            
        if curr is None:
            curr = root
            print(f"  Вернулись в корень №{root.id}")
        else:
            curr = curr.transitions[char]
            print(f"  Успешный переход в узел №{curr.id} ('{char}')")
            
        temp = curr
        while temp is not None:
            for offset, length in temp.parts_info:
                start_pos = i - offset - length + 1
                if 0 <= start_pos <= n - pattern_len:
                    C[start_pos] += 1
                    print(f"  -> Найдено совпадение подстроки! Смещение в шаблоне: {offset}, Длина: {length}")
                    print(f"     Увеличиваем счетчик совпадений для стартовой позиции {start_pos + 1} (C[{start_pos + 1}] = {C[start_pos]})")
            temp = temp.exit_link

def main():
    text = input("Введите текст: ").strip()
    pattern = input("Введите шаблон с джокерами: ").strip()
    joker = input("Введите символ джокера: ").strip()
    
    parts = []
    current_part = []
    start_idx = -1
    
    print("\n--- Подготовка шаблона ---")
    for idx, char in enumerate(pattern):
        if char != joker:
            if start_idx == -1:
                start_idx = idx
            current_part.append(char)
        else:
            if current_part:
                parts.append(("".join(current_part), start_idx))
                print(f"Выделена чистая подстрока: '{''.join(current_part)}', смещение: {start_idx}")
                current_part = []
                start_idx = -1
    if current_part:
        parts.append(("".join(current_part), start_idx))
        print(f"Выделена чистая подстрока: '{''.join(current_part)}', смещение: {start_idx}")
        
    if not parts:
        print("Ошибка: шаблон состоит только из джокеров.")
        return
        
    C = [0] * len(text)
    
    root = build_trie(parts)
    build_automaton(root)
    
    search_text(text, root, len(pattern), C)
    
    max_suff, max_exit = calculate_longest_chains(root)
    
    print("\n--- Итоговые результаты ---")
    print("Вхождения полного шаблона (Стартовые позиции):")
    for idx in range(len(text) - len(pattern) + 1):
        if C[idx] == len(parts):
            print(idx + 1)
            
    print(f"\n Самая длинная цепочка суффиксных ссылок: {max_suff}")
    print(f" Самая длинная цепочка конечных ссылок: {max_exit}")

if __name__ == "__main__":
    main()