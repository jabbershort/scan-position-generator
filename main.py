from mesher.Grid import Grid as G
import numpy as np

def main():
    g = G(1,3,0.1,3,0.1,True)
    g.base_point = np.array([1,1,1])
    g.draw(True)

if __name__ == "__main__":
    main()