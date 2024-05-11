

import matplotlib.pyplot as plt
import matplotlib.patches as patches

import math


def catalan(n):
    return int(math.comb(2*n,n)/(n+1))



class CatalanSquare():
    def __init__(self, representation, all_previous = set()):
        self.n = len(representation)
        self.representation = representation
        self.all_previous = all_previous

    def __str__(self):
        return "".join(str(x) for x in self.representation)
    
    def plot(self, ax):
        a = zip(self.representation,range(1, self.n+1))
        for (depth, ix) in sorted(a):
            x = ix
            y = self.n - ix + 1
            square = patches.Rectangle((x, y), self.n, self.n, edgecolor='purple', facecolor='skyblue',linewidth=2)
            ax.add_patch(square)
        
        ax.set_xlim(0,2*self.n+1)
        ax.set_ylim(0, 2*self.n+1)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(str(self))
        return None

    def __eq__(self, other):
        if self.representation == other.representation:
            return True

        return False

    def __iter__(self):
        return self
 
 
    def __next__(self):
        return self.next()
    
    def next(self):
        n = self.n


        for j in range(n,0,-1):
            #print("i",i)
            representation = self.representation
            for i in range(1,n):
                #print("j",j)
                ix = representation.index(j)
                if ix+i < n:
                        candidate = self.jump(ix, ix+i,1)
                        if candidate and candidate.is_231_avoiding() and candidate not in self.all_previous:
                                return candidate
                if ix-i >= 0:
                        candidate = self.jump(ix-i, ix,-1)
                        if candidate and candidate.is_231_avoiding() and candidate not in self.all_previous:
                                return candidate
        
        print("No next Catalan square found")
        return None
    
    def is_231_avoiding(self):
        #TODO implement a more efficient algorithm
        for i in range(self.n):
            for j in range(i+1,self.n):
                for k in range(j+1,self.n):
                    if self.representation[i] < self.representation[j] and self.representation[j] > self.representation[k] and self.representation[i] > self.representation[k]:
                        return False
        return True
    
    def jump(self, i, j,direction):
        # jump the elements at positions i and j, one of elements is bigger than all in between
        hill = max(self.representation[i], self.representation[j])
        for k in range(i,j+1):
            if self.representation[k] > hill:
                # jump not possible
                return False
            
        representation = self.representation.copy()
        if direction == 1:
            interval = representation[i+1:j+1]
            representation[j] = representation[i]
            representation[i:j] = interval
        if direction == -1:
            interval = representation[i:j]
            representation[i] = representation[j]
            representation[i+1:j+1] = interval
        return CatalanSquare(representation, self.all_previous.union({self}))
    
    def __hash__(self):
        return hash(str(self.representation))


def visualize_catalan_squares(n):

    cat_num = catalan(n)
    cs1 = CatalanSquare(list(range(1,n+1)))

    fig, axs = plt.subplots(6,7)
    fig.set_size_inches(20, 10)
    fig.tight_layout()

    i = 0
    axs = axs.flatten()
    while i < cat_num and cs1 is not None:
        cs1.plot(axs[i])
        cs1 = cs1.next()
        i += 1

    for ax in axs:
        ax.axis('off')
    
    plt.show()


if __name__ == '__main__':
    visualize_catalan_squares(5)