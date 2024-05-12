import matplotlib.pyplot as plt
import matplotlib.patches as patches

from itertools import combinations

import math



class SetPartition():
    def __init__(self, representation, all_previous = set()):
        self.n = len(representation)
        self.representation = representation
        self.all_previous = all_previous

    def __str__(self):
        #insert | where numbers stop increasing, representation is a list of numbers
        lst = []
        for i in range(1,self.n):
            if self.representation[i] < self.representation[i-1]:
                lst.append(str(self.representation[i-1]))
                lst.append("|")
            else:
                lst.append(str(self.representation[i-1]))
        lst.append(str(self.representation[-1]))
        return " ".join(lst)

            

    
    def plot(self, ax):
        # visualize the set partition
        # scatter n points in a circle
        # draw lines between points that are in the same set

        blocks = str(self).split("|")
        colors = ['red','blue','green','yellow','purple','orange','black','pink','brown','cyan']

        x = [math.cos(2*math.pi*i/self.n) for i in range(self.n)]
        y = [math.sin(2*math.pi*i/self.n) for i in range(self.n)]
        ax.scatter(x,y)

        for j, block in enumerate(blocks):
            block = block.split()
            for i in range(1,len(block)):
                ax.plot([x[int(block[i-1])-1],x[int(block[i])-1]],[y[int(block[i-1])-1],y[int(block[i])-1]],linewidth=5, color = colors[j],marker='o', mfc = 'black', mec = 'black')
        ax.set_xlim(-1.5,1.5)
        ax.set_ylim(-1.5,1.5)
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
            representation = self.representation
            for i in range(1,n):
                ix = representation.index(j)
                if ix+i < n:
                        candidate = self.jump(ix, ix+i,1)
                        if candidate and candidate.avoids_pattern([1,3,2],1) and candidate not in self.all_previous:
                                return candidate
                if ix-i >= 0:
                        candidate = self.jump(ix-i, ix,-1)
                        if candidate and candidate.avoids_pattern([1,3,2],1) and candidate not in self.all_previous:
                                return candidate
        
        print("No next partition found")
        return None
    
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
        return SetPartition(representation, self.all_previous.union({self}))
    
    def __hash__(self):
        return hash(str(self.representation))

    def avoids_pattern(self,pattern,consecutive_ix = None):
        permutation = self.representation
        for patt in combinations(permutation,len(pattern)):
            if consecutive_ix is not None:
                permutation_ix = permutation.index(patt[consecutive_ix])
                if patt[consecutive_ix+1] != permutation[permutation_ix+1]:
                     continue

            a = zip(patt,range(0,len(pattern)))
            new = [0] * len(pattern)
            for i,pair in enumerate(sorted(a)):
                new[pair[1]] = i + 1
            if list(new) == list(pattern):
                return False
        return True


def visualize_set_partitions(n):

    sp = SetPartition(list(range(1,n+1)))

    fig, axs = plt.subplots(5,3)
    fig.set_size_inches(20, 10)
    fig.tight_layout()

    i = 0
    axs = axs.flatten()
    while sp is not None:
        sp.plot(axs[i])
        sp = sp.next()
        i += 1

    for ax in axs:
        ax.axis('off')
    
    plt.savefig("set_partitions_example.svg")
    plt.show()

        

if __name__ == '__main__':
    visualize_set_partitions(4)