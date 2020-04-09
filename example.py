import textree as ttree
import sys

if __name__ == "__main__":
    tex_file = sys.argv[1] if len(sys.argv) > 1 else 'examples/lorem.tex'
    csv_prefix = sys.argv[1] if len(sys.argv) > 2 else 'lorem'

    # Read the tex file and create a tree out of it:
    txt = ttree.open_tex_project(tex_file)

    tt = ttree.parse_tex_to_tree(txt)
    tt.pretty_print()
    tt.to_gephi_csv(csv_prefix)