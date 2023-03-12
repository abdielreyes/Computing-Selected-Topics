import numpy as np
from pprint import pprint
from PIL import Image

class Automata:
    
    def get_cell_value(self,x: int, y :int)->int:
        if x >= self.width:
            x -= self.width
        elif x < 0:
            x += self.width
        if y >= self.height:
            y -= self.height
        elif y < 0:
            y += self.height
        return self.world[(y * self.width) + x]
    def update():
        for y in range (self.height):
            for x in range (self.width):
                neighbors = [
                    self.get_cell_value(x + 1, y - 1),
                    self.get_cell_value(x , y - 1),
                    self.get_cell_value(x - 1, y - 1),
                    self.get_cell_value(x - 1, y),
                    self.get_cell_value(x + 1, y),
                    self.get_cell_value(x - 1, y + 1),
                    self.get_cell_value(x , y + 1),
                    self.get_cell_value(x + 1, y + 1),
                ]
                alive_count = neighbors.count(self.live)
                current = self.get_cell_value(x,y)
                if current == self.live:
                    if alive_count not in self.alive:
                        current = self.dead
                else:
                    if alive_count in self.born:
                        current = self.live
                self.new_world[(y * self.width) + x] = current


def main():
    size = 2
    m = size*size
    res = []
    for k in range(0,(2**m)):
        a = np.binary_repr(k, m)
        b = []
        for i in range(0,size):
            b.append(list((a[size*i:size*(i+1)])))
        res.append(b)
    res = np.array(res).astype(np.uint8)
    print(res)


    # final_image = Image.new("RGB",(m,m))
    # for index ,r in enumerate(res):
    #     # im = Image.fromarray(r*255).resize((50,50),resample=Image.NEAREST)
    #     im = Image.fromarray(r*255).resize((50,50))
    #     final_image.copy
    #     images.append(im)

        
    print("Finished")
        



if __name__ == '__main__':
    main()