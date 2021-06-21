import numpy as np
from PIL import Image
import math
    

def analyzeTileset(tileset):
    #open image
    try: 
        img  = Image.open(tileset) 
    except IOError:
        pass
    
    #convert to rgb
    img = img.convert('RGB')

    #width, height etc
    with img as image:
        width, height = image.size

    tiles_x = int(width/8)
    tiles_y = int(height/8)
    tiles = tiles_x * tiles_y


    #create empty lists for the tiles including flipped
    data_normal = list()
    data_flip_x = list()
    data_flip_y = list()
    data_flip_x_y = list()

    for i in range(tiles_y):
        for j in range(tiles_x):
            #cut out tile
            img_tmp = img.crop([j*8, i*8, j*8+8, i*8+8])
            #print(j*8, i*8, j*8+8, i*8+8)
            img_tmp = img_tmp.convert('RGB')
            #create flipped version
            img_tmp_flip_x = img_tmp.transpose(Image.FLIP_LEFT_RIGHT)
            img_tmp_flip_y = img_tmp.transpose(Image.FLIP_TOP_BOTTOM)
            img_tmp_flip_x_y = img_tmp_flip_x.transpose(Image.FLIP_TOP_BOTTOM)
            #turn img data into numpy array
            data_tmp_normal = np.array(img_tmp)
            data_tmp_flip_x = np.array(img_tmp_flip_x)
            data_tmp_flip_y = np.array(img_tmp_flip_y)
            data_tmp_flip_x_y = np.array(img_tmp_flip_x_y)
            #reshape 8x8 to 64x1
            data_tmp_normal = np.reshape(data_tmp_normal, [64,3])
            data_tmp_flip_x = np.reshape(data_tmp_flip_x, [64,3])
            data_tmp_flip_y = np.reshape(data_tmp_flip_y, [64,3])
            data_tmp_flip_x_y = np.reshape(data_tmp_flip_x_y, [64,3])
            #add to lists
            data_normal.append(data_tmp_normal)
            data_flip_x.append(data_tmp_flip_x)
            data_flip_y.append(data_tmp_flip_y)
            data_flip_x_y.append(data_tmp_flip_x_y)
            


        
    #create "empty" list for uniquiness
    unique = list()
    for i in range(tiles):
        unique.append([999, ''])
    #determine if the tile is unique or a duplicate
    for i in range(tiles):
        test_val = data_normal[i]
        for j in range(tiles):
            if i==j:
                continue
            if unique[j][0] != 999:
                continue
            if (np.array_equal(test_val, data_normal[j])):
                if ((j>i) and (i < unique[j][0])):
                    unique[j] = [i, 'D']
            elif (np.array_equal(test_val, data_flip_x[j])):
                if ((j>i) and (i < unique[j][0])):
                    unique[j] = [i, 'x']
            elif (np.array_equal(test_val, data_flip_y[j])):
                if ((j>i) and (i < unique[j][0])):
                    unique[j] = [i, 'x']
            elif (np.array_equal(test_val, data_flip_x_y[j])):
                if ((j>i) and (i < unique[j][0])):
                    unique[j] = [i, 'xy']
    
    #replace unique values with a u (for readability)
    for i in range(tiles):
        if unique[i][0] == 999:
            unique[i] = 'u'+str(math.floor(i/16))+'/'+str(i%16)
    #print(unique)

    return data_normal, tiles, unique
    
    

def makeReducedTileset(tileset_base, tiles, unique):
    #if unique tile add to list
    tileset_new = list()
    for i in range(tiles):
        if (unique[i] == 'u'):
            tileset_new.append(tileset_base[i])

    #determine amount of new tiles
    removed_tiles = tiles-len(tileset_new)
    print('removed tiles: ' + str(removed_tiles))
    tiles = len(tileset_new)
    tiles_y = math.floor(tiles/16)+1
    #print(tiles)
    #print(tiles_y)
    
    #reshape back to 8x8 tiles
    for i in range(tiles):
        tileset_new[i] = np.reshape(tileset_new[i], [8,8,3])
        
    #combine all 8x8 tiles to one image
    a = tileset_new[0]
    for i in range(tiles-1):
        a = np.concatenate((a, tileset_new[i+1]), axis=1)
    
    #add empty tiles to the end for a rectangular image
    for i in range(tiles_y*16 - tiles):
        a = np.concatenate((a, tileset_new[0]), axis=1)

    #change shape to a 16 x tiles_y
    b = a[0:8,0:128]
    for i in range(tiles_y-1):
        start = 128+i*128
        end = 256+i*128
        b = np.concatenate((b, a[0:8,start:end]), axis=0)    


    #convert numpy array to image
    img_tmp = Image.fromarray(b, 'RGB')
    img_tmp.show()
    img_tmp.save('test.png')
    
    
def main():
    tileset_base, tiles, unique = analyzeTileset('./tiles.png')
    print(unique)
    makeReducedTileset(tileset_base, tiles, unique)


if __name__ == "__main__":
    main()