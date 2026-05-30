# Smart AutoComplete System

A smart **AutoComplete System** designed to provide fast and intelligent query suggestions based on user input.

The system is built using the **text8 dataset** stored in **Apache Cassandra** for scalable vocabulary storage. A **Trie Data Structure** is used as an in-memory LRU-style cache to provide extremely fast prefix-based suggestions, while an **N-Gram Language Model** is used to assign probabilities to words and rank suggestions based on contextual relevance.
