from src.graph.scatter import main
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("USAGE: python -m src.graph <file-name>")
        sys.exit()
    with open(sys.argv[1]) as file:
        main(file)
    print('exiting')
    sys.exit()