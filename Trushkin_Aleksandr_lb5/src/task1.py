from collections import deque

class AhoCorasickNode:
    _id_counter = 0

    def __init__(self, char="#"):
        self.id = AhoCorasickNode._id_counter
        AhoCorasickNode._id_counter += 1
        self.char = char 
        self.transitions = {}
        self.pattern_indices = []
        self.suff_link = None
        self.exit_link = None

def build_trie(patterns):
    AhoCorasickNode._id_counter = 0 
    root = AhoCorasickNode()
    
    print("--- 1. Построение бора (TRIE) ---")
    for idx, pattern in enumerate(patterns, 1):
        print(f"\nДобавляем шаблон №{idx}: '{pattern}'")
        curr = root
        for char in pattern:
            if char not in curr.transitions:
                new_node = AhoCorasickNode(char)
                curr.transitions[char] = new_node
                print(f"  Создаем новый узел №{new_node.id} по символу '{char}' из узла №{curr.id}")
            else:
                print(f"  Переходим в существующий узел №{curr.transitions[char].id} по символу '{char}'")
            curr = curr.transitions[char]
        curr.pattern_indices.append(idx)
        print(f"  Узел №{curr.id} становится терминальным для шаблона №{idx}")
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
            if suff.pattern_indices:
                child.exit_link = suff
            else:
                child.exit_link = suff.exit_link
                
            print(f"Узел №{child.id} ('{char}'): "
                  f"суф. ссылка -> №{child.suff_link.id}, "
                  f"кон. ссылка -> №{child.exit_link.id if child.exit_link else 'None'}")
            queue.append(child)

def get_all_nodes(root):
    """Вспомогательная функция для сбора всех вершин автомата"""
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

def search_text(text, root, patterns):
    print("\n--- 3. Процесс поиска в тексте ---")
    results = []
    curr = root
    
    for i, char in enumerate(text):
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
            for idx in temp.pattern_indices:
                start_pos = i - len(patterns[idx - 1]) + 2
                print(f"   Найдено совпадение: шаблон №{idx} ('{patterns[idx-1]}') со стартовой позиции {start_pos}")
                results.append((start_pos, idx))
            temp = temp.exit_link
            
    return results

def main():
    text = input("Введите текст: ").strip()
    n = int(input("Введите количество шаблонов: ").strip())
    
    patterns = []
    for i in range(n):
        patterns.append(input(f"Шаблон №{i+1}: ").strip())
        
    root = build_trie(patterns)
    build_automaton(root)
    
    matches = search_text(text, root, patterns)
    
    matches.sort(key=lambda x: (x[0], x[1]))
    
    max_suff, max_exit = calculate_longest_chains(root)
    
    print("\n--- Итоговые результаты ---")
    print("Вхождения (Позиция Шаблон):")
    for pos, pattern_idx in matches:
        print(f"{pos} {pattern_idx}")
        
    print(f"\nСамая длинная цепочка суффиксных ссылок: {max_suff}")
    print(f"Самая длинная цепочка конечных ссылок: {max_exit}")

if __name__ == "__main__":
    main()
