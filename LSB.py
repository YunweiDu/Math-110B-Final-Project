from PIL import Image

def int2bin(rgb):
    r, g, b = rgb
    return (f'{r:08b}',f'{g:08b}',f'{b:08b}')

def bin2int(rgb):
    r, g, b = rgb
    return (int(r, 2),int(g, 2),int(b, 2))

def merge(img1, img2):
    if img2.size[0] > img1.size[0] or img2.size[1] > img1.size[1]:  
        raise ValueError('Image 2 should not be larger than Image 1!')
        
    pixel_map1 = img1.load()
    pixel_map2 = img2.load()
    new_image = Image.new(img1.mode, img1.size)
    pixels_new = new_image.load()
    for i in range(img1.size[0]):
        for j in range(img1.size[1]):
            rgb1 = int2bin(pixel_map1[i, j])

            rgb2 = int2bin((0, 0, 0))

            if i < img2.size[0] and j < img2.size[1]:
                rgb2 = int2bin(pixel_map2[i, j])

            # Merge the two pixels and convert it to a integer tuple
            r1, g1, b1 = rgb1
            r2, g2, b2 = rgb2
            rgb = (r1[:4] + r2[:4],
                   g1[:4] + g2[:4],
                   b1[:4] + b2[:4])

            pixels_new[i, j] = bin2int(rgb)

    return new_image
            

def unmerge(img):
  

        # Load the pixel map
        pixel_map = img.load()

        # Create the new image and load the pixel map
        new_image = Image.new(img.mode, img.size)
        pixels_new = new_image.load()

        # Tuple used to store the image original size
        original_size = img.size

        for i in range(img.size[0]):
            for j in range(img.size[1]):
                # Get the RGB (as a string tuple) from the current pixel
                r, g, b = int2bin(pixel_map[i, j])

                # Extract the last 4 bits (corresponding to the hidden image)
                # Concatenate 4 zero bits because we are working with 8 bit
                rgb = (r[4:] + '0000',
                       g[4:] + '0000',
                       b[4:] + '0000')

                # Convert it to an integer tuple
                pixels_new[i, j] = bin2int(rgb)

                # If this is a 'valid' position, store it
                # as the last valid position
                if pixels_new[i, j] != (0, 0, 0):
                    original_size = (i + 1, j + 1)

        # Crop the image based on the 'valid' pixels
        new_image = new_image.crop((0, 0, original_size[0], original_size[1]))

        return new_image
        
img1 = Image.open('img1.jpg')
img2 = Image.open('img2.jpg')
img3 = merge(img1,img2)
img3.show()

img4 = unmerge(img3)
img4.show()
           
