from src.packages.graphics import Image, Point, color_rgb, GraphicsObject
from utils import generate_empty_array

class Texture(Image):
    def __init__(self, texture_filename: str, p1: tuple, p2: tuple) -> Image:
        """ Returns a Image with the giving texture and coords """
        self.p1 = p1
        self.p2 = p2

        resized_width, resized_height = (abs(int(p1[0]-p2[0])), abs(int(p1[1]-p2[1])))

        Image.__init__(self, Point(0, 0), resized_width, resized_height)

        # Load original texture
        original_texture = Image(Point(0, 0), f"src/textures/{texture_filename}.ppm")
        width, height = original_texture.getWidth(), original_texture.getHeight()

        # All empty array
        texture_array = generate_empty_array(width, height) # For the original 
        resized_texture_array = generate_empty_array(resized_width, resized_height) # For the resized

        # Copy every pixel from the original texture
        for y in range(height):
            for x in range(width):
                texture_array[y][x] = original_texture.getPixel(x, y)
    
        # Resize image
        for y in range(resized_height):
            for x in range(resized_width):
                # Map (x, y) in resized image to (src_x, src_y) in original
                src_x = int(x * width / resized_width)
                src_y = int(y * height / resized_height)
                resized_texture_array[y][x] = texture_array[src_y][src_x]

        # Copy pixel a pixel to the Image
        for i in range(resized_width):
            for j in range(resized_height):
                r, g, b = resized_texture_array[j][i]
                color = color_rgb(r, g, b)
                self.setPixel(i, j, color)
        
        # Move to the correct location
        self.move(p1[0]+resized_width/2, p1[1]+resized_height/2)
    
    def getP1(self):
        return Point(*self.p1)
    
    def getP2(self):
        return Point(*self.p2)
