"""
Sample Question Bank for GATE Computer Science & Engineering.
Contains categorized questions with metadata, explanations, and options.
"""

QUESTIONS_DB = [
    {
        "id": "GATE-CS-2024-Q1",
        "exam": "GATE CS",
        "year": "2024",
        "topic": "Algorithms",
        "subtopic": "Graph Algorithms & Shortest Path",
        "difficulty": "Medium",
        "marks": 2,
        "question": (
            "What is the worst-case time complexity of the Floyd-Warshall algorithm "
            "to find all-pairs shortest paths on a directed graph with $V$ vertices and $E$ edges?"
        ),
        "options": [
            "O(V · E)",
            "O(V³)",
            "O(V² log V + V · E)",
            "O(E log V)"
        ],
        "correct_option_index": 1,
        "explanation": (
            "The Floyd-Warshall algorithm computes all-pairs shortest paths using dynamic programming. "
            "It iterates through three nested loops from 1 to $V$ (for each intermediate vertex $k$, "
            "source $i$, and destination $j$), updating the distance matrix. "
            "Thus, the running time is $\\Theta(V^3)$ regardless of the edge count $E$."
        )
    },
    {
        "id": "GATE-CS-2024-Q2",
        "exam": "GATE CS",
        "year": "2024",
        "topic": "Operating Systems",
        "subtopic": "Memory Management & Paging",
        "difficulty": "Medium",
        "marks": 2,
        "question": (
            "Consider a virtual memory system with 32-bit virtual addresses and a 4 KB page size. "
            "If each page table entry (PTE) occupies 4 bytes, what is the size of a single-level page table?"
        ),
        "options": [
            "2 MB",
            "4 MB",
            "1 MB",
            "8 MB"
        ],
        "correct_option_index": 1,
        "explanation": (
            "Page size = 4 KB = $2^{12}$ bytes. Virtual address space = $2^{32}$ bytes.\n"
            "Number of virtual pages = $2^{32} / 2^{12} = 2^{20}$ entries.\n"
            "Each page table entry requires 4 bytes ($2^2$ bytes).\n"
            "Total single-level page table size = $2^{20} \\times 4\\text{ bytes} = 4\\text{ MB}$."
        )
    },
    {
        "id": "GATE-CS-2023-Q1",
        "exam": "GATE CS",
        "year": "2023",
        "topic": "Theory of Computation",
        "subtopic": "Regular Languages & Finite Automata",
        "difficulty": "Easy",
        "marks": 1,
        "question": (
            "Which of the following languages defined over the alphabet $\\Sigma = \\{0, 1\\}$ is regular?"
        ),
        "options": [
            "L₁ = {0ⁿ 1ⁿ | n ≥ 1}",
            "L₂ = {w wᴿ | w ∈ {0, 1}*}",
            "L₃ = {w ∈ {0, 1}* | number of 0s in w is divisible by 3}",
            "L₄ = {0ᵖ | p is a prime number}"
        ],
        "correct_option_index": 2,
        "explanation": (
            "$L_3$ can be recognized by a Deterministic Finite Automaton (DFA) with 3 states "
            "(representing remainders 0, 1, and 2 modulo 3). Hence $L_3$ is regular.\n"
            "$L_1$ and $L_2$ require an infinite stack memory (CFLs), and $L_4$ cannot be pumped (non-regular)."
        )
    },
    {
        "id": "GATE-CS-2023-Q2",
        "exam": "GATE CS",
        "year": "2023",
        "topic": "Computer Networks",
        "subtopic": "TCP Congestion Control",
        "difficulty": "Hard",
        "marks": 2,
        "question": (
            "In TCP Reno congestion control, suppose the congestion window (`cwnd`) is currently 32 MSS "
            "when a severe packet loss occurs due to a retransmission timeout (RTO). "
            "What will be the updated values of `ssthresh` (slow start threshold) and `cwnd`?"
        ),
        "options": [
            "ssthresh = 16 MSS, cwnd = 1 MSS",
            "ssthresh = 16 MSS, cwnd = 16 MSS",
            "ssthresh = 32 MSS, cwnd = 1 MSS",
            "ssthresh = 16 MSS, cwnd = 8 MSS"
        ],
        "correct_option_index": 0,
        "explanation": (
            "Upon a timeout event in TCP Tahoe and Reno:\n"
            "1. `ssthresh` is set to $\\max(\\text{cwnd}/2, 2\\text{ MSS}) = 32 / 2 = 16\\text{ MSS}$.\n"
            "2. `cwnd` is reset back to 1 MSS, restarting the transmission from the Slow Start phase."
        )
    },
    {
        "id": "GATE-CS-2022-Q1",
        "exam": "GATE CS",
        "year": "2022",
        "topic": "Database Management Systems",
        "subtopic": "Relational Normalization & BCNF",
        "difficulty": "Medium",
        "marks": 2,
        "question": (
            "Given a relation schema $R(A, B, C, D)$ with functional dependencies "
            "$F = \\{A \\to B,\\; B \\to C,\\; C \\to D,\\; D \\to A\\}$. "
            "Which of the following is the highest normal form satisfied by $R$?"
        ),
        "options": [
            "1NF but not 2NF",
            "2NF but not 3NF",
            "3NF but not BCNF",
            "BCNF (Boyce-Codd Normal Form)"
        ],
        "correct_option_index": 3,
        "explanation": (
            "Taking closures:\n"
            "$A^+ = ABCD$, $B^+ = ABCD$, $C^+ = ABCD$, $D^+ = ABCD$.\n"
            "All attributes $A, B, C, D$ are individual candidate keys.\n"
            "For every non-trivial functional dependency $X \\to Y$ in $F$, the determinant $X$ is a superkey.\n"
            "Therefore, $R$ satisfies BCNF (and trivially 3NF and 2NF)."
        )
    },
    {
        "id": "GATE-CS-2022-Q2",
        "exam": "GATE CS",
        "year": "2022",
        "topic": "Data Structures",
        "subtopic": "Binary Search Trees",
        "difficulty": "Medium",
        "marks": 2,
        "question": (
            "The preorder traversal sequence of a Binary Search Tree (BST) is:\n"
            "**15, 10, 12, 11, 20, 18, 25**.\n"
            "Which of the following is the correct postorder traversal of the tree?"
        ),
        "options": [
            "11, 12, 10, 18, 25, 20, 15",
            "10, 11, 12, 18, 20, 25, 15",
            "11, 12, 18, 25, 20, 10, 15",
            "12, 11, 10, 18, 25, 20, 15"
        ],
        "correct_option_index": 0,
        "explanation": (
            "For any BST, the inorder traversal is strictly ascending sorted order: "
            "10, 11, 12, 15, 18, 20, 25.\n"
            "Root is 15 (first element in preorder).\n"
            "Left subtree contains keys < 15: {10, 12, 11}. Root of left subtree is 10. "
            "Right child of 10 is 12; left child of 12 is 11.\n"
            "Right subtree contains keys > 15: {20, 18, 25}. Root is 20 with left child 18 and right child 25.\n"
            "Postorder (Left, Right, Root): 11, 12, 10, 18, 25, 20, 15."
        )
    },
    {
        "id": "GATE-CS-2021-Q1",
        "exam": "GATE CS",
        "year": "2021",
        "topic": "Computer Organization",
        "subtopic": "Cache Memory Mapping",
        "difficulty": "Hard",
        "marks": 2,
        "question": (
            "A cache system contains 64 cache lines/blocks with 32 bytes per block. "
            "The main memory is byte-addressable with 16-bit physical addresses. "
            "If the cache is organized as 4-way set associative, what are the widths of the Tag, Set Index, and Block Offset fields?"
        ),
        "options": [
            "Tag = 7 bits, Set = 4 bits, Offset = 5 bits",
            "Tag = 8 bits, Set = 3 bits, Offset = 5 bits",
            "Tag = 6 bits, Set = 5 bits, Offset = 5 bits",
            "Tag = 9 bits, Set = 2 bits, Offset = 5 bits"
        ],
        "correct_option_index": 0,
        "explanation": (
            "1. Block Offset: Block size = 32 bytes = $2^5$ bytes $\\implies$ 5 bits.\n"
            "2. Total blocks = 64. Associativity = 4-way $\\implies$ Number of sets = 64 / 4 = 16 sets = $2^4$ sets $\\implies$ 4 bits.\n"
            "3. Total address size = 16 bits $\\implies$ Tag = 16 - (4 + 5) = 7 bits.\n"
            "So Tag = 7 bits, Set = 4 bits, Offset = 5 bits."
        )
    },
    {
        "id": "GATE-CS-2021-Q2",
        "exam": "GATE CS",
        "year": "2021",
        "topic": "Compiler Design",
        "subtopic": "Grammar & Ambiguity",
        "difficulty": "Medium",
        "marks": 1,
        "question": (
            "Consider the Context-Free Grammar $G$ with production rules:\n"
            "$$S \\to aSb \\mid SS \\mid \\epsilon$$\n"
            "Which of the following statements correctly characterizes this grammar?"
        ),
        "options": [
            "It is unambiguous and LL(1)",
            "It generates all strings with equal number of a's and b's",
            "It is unambiguous and generates balanced parenthesis strings",
            "It is ambiguous and generates strings of well-nested balanced brackets"
        ],
        "correct_option_index": 3,
        "explanation": (
            "The grammar generates the Dyck language (well-balanced bracket strings, where $a$ is opening and $b$ is closing).\n"
            "It is ambiguous because strings like $ab$ have two distinct leftmost derivations:\n"
            "1) $S \\to aSb \\to a\\epsilon b = ab$\n"
            "2) $S \\to SS \\to (aSb)S \\to ab\\epsilon = ab$."
        )
    }
]

EXAM_OPTIONS = ["GATE CS", "GATE DA (Data Science & AI)", "ISRO CS", "UGC NET CS"]

YEAR_OPTIONS = ["All Years", "2024", "2023", "2022", "2021"]

TOPIC_OPTIONS = [
    "All Topics",
    "Algorithms",
    "Operating Systems",
    "Theory of Computation",
    "Computer Networks",
    "Database Management Systems",
    "Data Structures",
    "Computer Organization",
    "Compiler Design"
]
