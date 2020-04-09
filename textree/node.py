from anytree import NodeMixin, RenderTree
import re


class TNode(NodeMixin):
    sections = [
        'document', 'part', 'chapter',
        'section', 'subsection', 'subsubsection',
        'paragraph','subparagraph'
    ]
    def __init__(self, name, tag, ts, te=-1, parent=None, children=None):
        self.lvl = -1 if tag not in TNode.sections else TNode.sections.index(tag)
        self.desc = '<TNode [{}]: {} ({}, {})>'
        self.name = name
        self.tag = tag
        self.ts = ts
        self.te = te
        self.id = None
        self.contents = []
        self.commands = []
        self.comments = []
        self.references = []
        self.citations = []
        self.texts = []
        self.word_count = 0
        self.groups = []
        self.label = None
        self.parent = parent
        if children:  # set children only if given
            self.children = children

    def __repr__(self):
        #return f'<TNode[{self.tag}]: {self.name} ({self.ts}, {self.te})'
        return str(self)

    def __str__(self):
        return self.desc.format(self.tag, self.name, self.ts, self.te)

    def __eq__(self, other):
        return other.ts == self.ts and self.te == other.te

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return self.ts < other.ts

    def __le__(self, other):
        return self.ts <= other.ts

    def __gt__(self, other):
        return self.ts > other.ts

    def __ge__(self, other):
        return self.ts >= other.ts

    def __contains__(self, other):
        return self.ts < other.ts and self.te >= other.ts

    def __len__(self):
        return self.te - self.te

    def pretty_print(self):
        """ Print the tree """
        for pre, _, node in RenderTree(self):
            treestr = u"%s%s" % (pre, node)
            print(treestr.ljust(8))

    def to_graph(self):
        """ Convert the tree into a hashable graph with context:

            graph = {
                'nodes': [
                    {'id': '', 'name':'', ...},
                    ...
                ]
                'edges': [
                    {'from': id, 'to': id, 'weight': }
                ]

            }

            Traverses the tree downward from current node.
            Ignores possible siblings of current node.
        """
        for pre, _, node in RenderTree(self):
            treestr = u"%s%s" % (pre, node)
            print(treestr.ljust(8))


    def to_gephi_csv(self, filename='textree', delim=','):
        """ Save two csv files which can be visualised with gephi

            edges.csv:
                ID, Source, Target, Weight

            nodes.csv:
                ID, Tag, Name, ...
        """
        nodes = [n for _, _, n in RenderTree(self)]
        labels = {}

        # 1. The nodes:
        with open(filename+'_nodes.csv', 'w') as f:
            f.write(delim.join([
                'ID','Name','Tag','Label','Word Count',
                'N Comments','N Commands','N References','N Citations\n'
            ])
            )

            for n in nodes:
                # Print the node info:
                f.write(delim.join([str(v) for v in [
                    n.id, n.name, n.tag, n.label, n.word_count,
                    len(n.comments), len(n.commands),
                    len(n.references), len(n.citations)]
                ])+'\n')
                # Save the label s we can refer to correct node:
                if n.label is not None:
                    labels[n.label] = n.id

        # 2. The edges:
        with open(filename+'_edges.csv', 'w') as f:
            f.write(delim.join(['ID','Source','Target','Weight','Type\n']))
            for i, n in enumerate(nodes):
                # Skip root (no parent):
                if n.parent is None:
                    print('parent none')
                    continue

                # Link to the parent:
                f.write(delim.join([str(v) for v in [
                    f'p{i}', n.parent.id, n.id, 1, 'Undirected\n']
                ]))

                # Link all the references:
                for j, r in enumerate(n.references):
                    target = labels.get(r, False)
                    if not target:
                        print("did not find a reference:", r)
                        continue
                    f.write(delim.join([str(v) for v in [
                        f'r{i}-{j}', n.id, target, 0.5, 'Directed\n']
                    ]))

    def parse_contents(self, texts):
        """ Analyse contents for commands, text, groups and label
        """
        # regex for tags:
        w = r'[\w\s\.\,\:]'

        # Join the texts to be analysed
        txt = '\n'.join([texts[l[0]:l[1]] for l in self.contents])

        # 1. Find comments and remove them:
        self.comments = [c.group(0) for c in re.finditer(r'[^\\](%.*)', txt)]
        for fluff in self.comments:
            txt = txt.replace(fluff, ' ')

        # 2. Find commands and remove them:
        cmds = re.finditer(r'\\\w+(\['+w+r'*\])*(\{'+w+r'*\})*', txt)
        self.commands = [c.group(0) for c in cmds]
        for fluff in self.commands:
            txt = txt.replace(fluff, ' ')

        # 3. Find label from commands:
        cmds_str = ''.join(self.commands)
        m = re.search(r'\\label\{('+w+r'*)\}', cmds_str)
        self.label = m.group(1) if m else None

        # 4. Find references from commands:
        m = re.finditer(r'\\ref\{('+w+r'*)\}', cmds_str)
        self.references = [r.group(1) for r in m]

        # 5. Find citations from commands:
        m = re.finditer(r'\\cite\{('+w+r'*)\}', cmds_str)
        self.citations = [r.group(1) for r in m]

        # 6. parse text (everything not comment or command):
        self.texts = [t for t in txt.split('\n\n') if t and not t.isspace()]
        self.word_count = sum([len(t.split()) for t in self.texts])


class TEnv(TNode):
    def __init__(self, tag, ts, te=-1, parent=None, children=None):
        super().__init__('env', tag, ts, te)
        self.desc = '<TEnv [{}]>: {} ({}, {})'