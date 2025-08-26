# Data structures

In computer science a data structure is a data organization and storage format that enables efficient access and modification of the data.

Developer are interested in time and space complexity associated with the fourth fundamental operations: `Access`, `search`, `Insertion`, And `Deletion`.

A data structure is a way of organizing and storing data in a computer so that it can be access and use efficiently. It's the defined relationship between the data and the operation that can be performed on the data.

**Reference**

- [Data Structure](https://www.geeksforgeeks.org/data-structures/)
- [Data structure in Javascript](https://www.geeksforgeeks.org/courses/data-structures-and-algorithms-in-javascript?utm_source=geeksforgeeks&utm_medium=article_bottom_text_dsa&utm_campaign=courses)

## Why data as structure

- **Efficient data management**: They enable efficient storage and retrieval of data, Reducing processing time and improving performance.

- **Data organization**: They organize data and all logical matter, making it easier to understand and access.

- **Data obstruction**: They can hide the implementation detail of the data storage.

- **Reusability**: Common data structure can be used in multiple application, saving time and effort and development.

- **Algorithm optimization**: The choice of the appropriate date structure can Significantly impact the efficiency of algorithm that operate on the data.

## Big O Notation

Big O Notation is a way to describe the performance or complexity of an algorithm, particularly in terms of:

Time Complexity – How the runtime of an algorithm grows as the input size increases.

Space Complexity – How memory usage grows with input size.

It's used to describe the worst-case scenario, helping us understand how an algorithm scales.

![Big O Notation](https://www.bigocheatsheet.com/img/big-o-cheat-sheet-poster.png)

| Big O        | Name          | Example Scenario                                    | Growth        |
| ------------ | ------------- | --------------------------------------------------- | ------------- |
| `O(1)`       | Constant time | Accessing array element by index                    | ⚡ Fastest     |
| `O(log n)`   | Logarithmic   | Binary search                                       | 📉 Efficient  |
| `O(n)`       | Linear        | Looping through an array                            | ➡️ Steady     |
| `O(n log n)` | Linearithmic  | Merge sort, quicksort (average case)                | 🔁 Fast Sorts |
| `O(n²)`      | Quadratic     | Nested loops (e.g., bubble sort)                    | 🐢 Slow       |
| `O(2ⁿ)`      | Exponential   | Recursive Fibonacci without memoization             | 💣 Explodes   |
| `O(n!)`      | Factorial     | Brute-force permutations (e.g., traveling salesman) | 🧨 Very Slow  |

## Classification of the structure

- **Linear data structures**: Store data in a sequential order is allowing for easy insertion and deletion operation. Example: Array, linked list, stack And queues.

- **Non-linear data structure**: These structures store data in a hierarchical, or interconnected manner, this allowing for more complex relationships between data elements. Example: Trees, Graphs and hash tables.

- **Advanced**:

| **Category**         | **Data Structure**              | **Description**                                                                 |
|----------------------|----------------------------------|----------------------------------------------------------------------------------|
| **Linear**           | Array                            | Contiguous elements with O(1) access via indices                                 |
|                      | Linked List (Singly/Doubly)     | Nodes linked by pointers; efficient insert/delete                                |
|                      | Stack                            | LIFO access (Last-In, First-Out)                                                 |
|                      | Queue                            | FIFO access (First-In, First-Out)                                                |
|                      | Deque                            | Double-ended queue with insert/delete at both ends                               |
| **Non-Linear**       | Tree (General)                   | Hierarchical structure of parent-child nodes                                     |
|                      | Binary Tree                      | Tree where each node has at most 2 children                                      |
|                      | Binary Search Tree (BST)         | Binary tree with ordered left < root < right                                     |
|                      | AVL Tree                         | Height-balanced BST for efficient searching                                      |
|                      | Red‑Black Tree                   | Self-balancing BST used in libraries and OS                                      |
|                      | Heap (Min/Max)                   | Binary tree maintaining min/max-heap property                                    |
|                      | Trie                             | Tree for string prefix storage and lookups                                       |
|                      | Graph (Adjacency List/Matrix)   | Nodes (vertices) connected by edges, for complex relationships                   |
| **Hash-Based**       | Hash Table                       | Stores key-value pairs with constant average-time operations                     |
|                      | Hash Map                         | Hash table implementation supporting object keys                                 |
|                      | Hashing                          | Technique to map data to fixed-size values for fast access                       |
| **Mapped Structures**| Map (Dictionary)                 | Stores key-value pairs; can preserve insertion order (in JS: `Map<K, V>`)         |
| **Grid-Based**       | Matrix                           | 2D array of elements; used in image data, graph adjacency, etc.                  |
| **Advanced**         | Segment Tree                     | Tree supporting efficient range queries and updates                              |
|                      | Fenwick Tree (Binary Indexed Tree)| Supports prefix sums efficiently                                                |
|                      | Disjoint Set (Union-Find)        | Keeps track of elements partitioned into disjoint subsets                        |
| **Miscellaneous**    | Misc                              | Placeholder for special-purpose or domain-specific structures (e.g., KD-Tree)    |

## Linear Data structures

Store data in a sequential order is allowing for easy insertion and deletion operation.

- Array
- Linked List
- Queue
- Stack

### Advantage of linear data structures

- **Efficient data access**: Element can be easily accessed by the position in the sequence.

- **Dynamic sizing**: Linear data, structure and dynamically, adjust their size as element or added or removed.

- **Ease of implementation**: Linear data structure can be easily implemented using array or linked lists.

- **Versatility**: Linear data structure can be used for searching sorting and manipulation of data.

- **Simple algorithms**: Riddance use in linear data structure are simple and straightforward.

### This advantage of linear data structures

- **Limited data access**: Accessing elements not sorted at the end, or at the beginning of a sequence can be time consuming.

- **Memory overhead**: Maintaining the links between elements in the linked lists and pointers in stack in queues can consume additional memory.

- **Complex algorithms**: Some algorithms use it in linear data structure, such as searching and sorting can be complex and time-consuming.

- **Inefficient use of memory**: Linear data structure in result in any efficient use of memory if there's a gap in memory location.

- **Unsuitable for certains operations**: Linear data structure may not be suitable for operation that require constant Random access to elements, such as searching for an element in a large dataset.

#### Array

Array is a collection of element stored in a continuous memory locations. Array data structure can be fixed length or dynamic length. Array use zero base index.

Random access: Array provide constant time `O(1)`, access to elements.

```ts
const newArray = ["a", "b", "c", "d"];
newArray.push("Seb");
```

![Array](./img/array.png)

### Multidimensional Array

It is possible to create a two-dimensional array, also refer as a matrix or a array of array.

#### Linked list

A linked list is a linear data structure which look like a chain of node where each note contains a data value and a reference link to the next node in the list.

Unlike array Linked list element are not stored in a continuous location in memory. Link list is a dynamic data structure that came allocate and deallocate memory at runtime.

- **Node**: Each element in a link list is represented by a node, Which contain two component.
- **Data**: The actual data or value associate with the element.
- **Next Pointer (Link)**: Reference to the next node.

The first known is called the **head**. It serve as the starting point for travelling the list.
Last node is called the **tail**. The value of the link is NULL.

#### Operations

- **Accessing Elements**: Accessing a specific element in a linked list take O(n) time.

- **Searching**: Searching of a node in linked list O(n) time as whole list needs to traversed in worst case.

- **Insertion**: Insertion takes O(1) time if we at the position where we have to insert an element.

- **Deletion**: Delete takes O(1) time if we know the position of the element to e deleted.

![Linked-list](./img/double_vs_single_linked_lists.png)

#### Singly Linked Lists

The singly Linked list as every node store the address of the next node in the list, the last node has thr reference as NULL.

[Single linked list](https://medium.com/swlh/singly-linked-list-in-javascript-a0e58d045561)

[Github Linked Lists](<https://github.com/Apress/js-data-structures-and-algorithms/blob/master/Chapter13(LL).js>)

```ts
function SinglyLinkedListNode(data) {
  this.data = data;
  this.next = null;
}

function SinglyLinkedList() {
  this.head = null;
  this.size = 0;
}

SinglyLinkedList.prototype.isEmpty = function () {
  return (this.size = 0);
};

SinglyListList.prototype.insert = function (value) {
  // if first node
  if (this.head === null) {
    this.head = SinglyLinkedListNode(value);
  } else {
    let temp = this.head;
    this.head = new SinglyLinkedListNode(value);
    this.head.next = temp;
  }
  this.size++;
};
let sll1 = new SinglyLinkedList();
sll1.insert(1);
```

#### Doubly Linked Lists

Doubly linked list each node has two pointers, one pointer to the next note and one pointer to the previous node. This bidirectional singly linked list allowing for efficient traversal in both direction.

#### Circular Linked Lists

A circular Linked list is the type of Linked list in which the first and the last note are also connected to each other to form a circle. There is not NULL link.

## Advanced Data Structure

#### Stack

A stack is a linear data structure in which only the last inserted element can be removed and access. That follow the last-In-First-Out(LIFO) principle.

Stack is great because it is fast, Since it is now, then the last element is to be removed, The look up and insertion happened in a constant time of `O(1)`.

![Stack](./img/stack.png)

##### Stack Operations

- **push()**: Element is added on top of the stack.
- **pop()**: An element is removed from the top of the stack.
- **top() || peek()**: This operation returned the last inserted element that is on top of the stack without removing it.
- **size()**: This operation returned the total number of element present in the stack.
- **isEmpty()**: This operation indicate whether the stack is empty or not.

- **Fixed size Stack**: As the name suggests, a fixed size has a fixed size and cannot grow shrink dynamically. If the stack is full, and an attempt is made to add element to it, an overflow error occurs. If the stack is empty and an attempt is made to remove an element from it an underflow error a cure.

- **Dynamic size Stack**: A dynamic size that can grow or shrink dynamically. This type of stack is implemented use a link list as it allows for easy resizing of the stack.

#### Queue

A queue is a linear data structure, You can remove only the first added element. That follow the First-In-First-Out (FIFO) principle.
Queue have linear time operation `O(1)`. Adding to a `enqueuing` push() is call in queueing and removing from the queue is called `dequeuing` or shift().

## Non-linear data structures

These structures store data in a hierarchical, or interconnected manner, this allowing for more complex relationships between data elements.

- Maps (Dictionary)
- Hash maps
- Binary Tree
- Binary Search
- Tree
- Heap
- Hashing
- Graph
- Matrix
- Misc
- Advanced Data Structure

#### Trees

The three data structure is composed of nodes. The first/top node that do not have any parent node is called the `root node`, The other nodes are called `children nodes`.

#### Binary trees

The binary tree is a type of tree that has only two children node left and right.

Traversal techniques are pre-order traversal, post-order traversal, in-order, traversal and level-order traversal.

[Binary tree](https://www.geeksforgeeks.org/introduction-to-binary-tree-data-structure-and-algorithm-tutorials/)

##### Pre-order traversal

#### Binary search trees

#### self-balancing binary search trees

### Heaps

Heap is a type of tree-like data structure in which the parent is bigger than its children, (if Max Heap) or smaller than its children (if Min Heap).

Heap can store any value of any type: strings, integer and even custom class.

Heaps can return the Max or Min value in O(1) time. Heap use an array to store data instead of having pointer to their children.

for example: [10, 15,30, 40, 50, 100, 40]

![Heaps](./img/heaps.png)

In a min Heap the elements at the root must be lower than the element at the tip of the branch.

In the max heap, the route node that has the higher value, and each node value is greater than its children.

**Percolation Bubbling Up and Down**

When element or added or remove, the structure of the heat must remain. Percolation takes O(log2(n)) in time.

### Graphs

- **Vertex**: A Vertex is the node from which graph or formed.

- **Edge**: An edge is the connection between node in a graph. Graphically it is the line between the vertex. Vertex can have a direction

### Hash tables

Is a fixed size data structure in which the size is defined at the creation.

Hash stable contain two main function, `put()` and `get()`, Boats of those function have a time complexity of `O(1)`.

`localStorage` Is an example of data structure based on hash stable.

## Data structures in Javascript/Typescript

- Set
- Weak Set
