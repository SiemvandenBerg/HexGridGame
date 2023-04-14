# import numpy as np
# from PIL import Image
# from terrain_types import terrain_types
# import os

# # for each terrain type in terrain_types
# for terrain in terrain_types:
#     # append. jpg to terrain

#     # replace spaces with underscores in terrain 
#     terrain = terrain.replace(' ', '_')

#     # if that terrain already has a .txt file, skip it
#     if terrain + '.txt' in os.listdir('terrain_arrays'):
#         print(f'{terrain} already has a .txt file')
#         continue

#     terrain_image = terrain + '.jpg'

#     # open image from terrain_image folder 
#     image = Image.open(f'terrain_images/{terrain_image}')

#     # image = Image.open('image.jpg')
#     colors = np.array(image)

#     terrainArray = terrain + '.txt'

#     # write to file in terrain_arrays folder
#     with open(f'terrain_arrays/{terrainArray}', 'w') as f:
#         f.write(str(colors.tolist()))