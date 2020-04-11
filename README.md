# TexTree
Create a tree object from a LaTeX project.


## 1. Features
This project was done to provide a way to handle / analyse LaTeX projects more easily.
Feature highlights:
- Support opening LaTeX projects consisting of multiple files (using `\include`)
- Extract several, maybe useful, stats on the file
- Create a traversable tree from the LaTeX project
    - Built upon the awesome `NodeMixin` of [`anytree`](https://github.com/c0fec0de/anytree)
- Export to a graph to support visualisation
    - A `dict` with __edges__ and __nodes__
    - Creates edges between references within the project
    - Specifically export to `.csv` files supported by [__Gephi__](https://gephi.org/)


## 2. Installation
1. Download / clone source, e.g.:
    ```
    $ git clone https://github.com/PebbleBonk/textree.git
    ```
2. Install required packages
    ```
    $ pip install -r requirements.txt
    ```
3. Import to your script and use:
    ```py
    import textree as tt
    txt = tt.open_tex_project('lorem.tex')
    ```


## 3. Usage
Basic workflow with the `TexTree` consists of two steps:
1. Load the tex file into text
2. Parse the text into a tree


### 3.1. Loading a LaTeX project into a tree
You can use the `textree.open_tex_project()` to load your LaTeX project into a string
```py
import textree as tt
txt = tt.open_tex_project('examples/lorem.tex')
```

Then you can simply parse the text into a tree:
```py
tree = tt.parse_tex_to_tree(txt) # >>> <TNode [Root]: Root (0, 5502)>
```
The function returns the root node of the created tree. You can traverse it with `.children` and `.parent` attributes.


#### 3.1.1. Tree node attributes
The node, describing a section or an evironment in the LaTeX project, contains some information about the containing text:

Attribute | Description | Example
----------|-------------|--------
`.commands` | List of found LaTeX commands in this node | ["\textbf", "\ref{fig:my_fig}"]
`.comments` | List of comments in this node | ["% A comment"]
`.word_count` | Number of words, excluding comments and commands | 527
`.label` | LaTeX label of the node if one exists | "fig:my_graph"
`.citations` | Cited labels | ["Lamport1984", "Rossum1991"]
`.texts` | Text contents | ["This is a paragraph.", "And another."]



### 3.2. Printing the tree
You can also pretty print the created tree for more information:
```py
tree.pretty_print()
```
Output:
>```
><TNode [Root]: Root (0, 5502)>
>└── <TEnv [document]>: None (114, 5500)
>    ├── <TNode [section]: S1 (144, 1129)>
>    │   ├── <TNode [subsection]: S1.S1 (619, 869)>
>    │   └── <TNode [subsection]: S1.S2 (870, 1129)>
>    ├── <TNode [section]: S2 (1130, 2542)>
>    │   └── <TNode [subsection]: S2.S1 (1460, 2542)>
>    │       ├── <TEnv [itemize]>: list:mylist (1606, 1867)
>    │       │   ├── <TEnv [itemize]>: None (1695, 1771)
>    │       │   └── <TEnv [itemize]>: None (1776, 1853)
>    │       ├── <TEnv [itemize]>: list:mylist (1869, 1959)
>    │       ├── <TEnv [tabular]>: table:synonyms (2032, 2136)
>    │       ├── <TNode [subsubsection]: S2.S1.S1 (2140, 2230)>
>    │       └── <TNode [subsubsection]: S2.S1.S2 (2231, 2542)>
>    ├── <TNode [section]: S3 (2543, 5485)>
>    │   ├── <TNode [paragraph]: This is a paragraph (3417, 4368)>
>    │   ├── <TNode [paragraph]: And have another paragraph (4369, 5299)>
>    │   └── <TNode [subsection]: S3.S1  (5300, 5484)>
>    └── <TEnv [appendices]>: None (5435, 5485)
>```

### 3.3. Exporting
To visualise your project as a network / graph with some external software you can export the project as a `dict` containing nodes and edges.
```py
graph = tree.to_graph()
print(graph['nodes'][0])
print(graph['edges'][0])
```

Output:
>```js
>{
>    'id': '$',
>    'name': 'Root',
>    'tag': 'Root',
>    'texlabel': None,
>    'word count': 0,
>    'n comments': 0,
>    'n commands': 5,
>    'n references': 0,
>    'n citations': 0,
>    'value': 0,
>    'label': '[Root]: Root',
>    'group': -1,
>    'title': 'words: 0'}
>{
>    'id': 'p1',
>    'from': '$',
>    'to': 'n0',
>    'weight': 1,
>    'type': 'undirected',
>    'value': 1,
>    'source': '$',
>    'target': 'n0'
>}
>```

Alternativaly, you can export to a `.csv` files combatible with [__Gephi__](https://gephi.org/):
```
tree.to_gephi_csv()
```
This will create two files, one containing the nodes and one containing the edges.

## 4. Notes
Some limitations of the project:
1. If you are laoding a project with includes, make sure the main file ends with `main.tex`
    - e.g. `my_latex_project_main.tex`
    - The files this includes, should be in the same directory