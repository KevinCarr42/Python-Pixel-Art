from PIL import Image, ImageFilter
import numpy as np
import palettes


def make_square(img_input_path):
    img = Image.open(img_input_path)
    w, h = img.size
    img_output_path = f'{img_input_path.split(".")[0]}_square.{img_input_path.split(".")[1]}'

    if h != w:
        if w > h:
            pad = (w - h) // 2
            top = img.crop((0, 0, w, 1)).resize((w, pad), Image.NEAREST)
            bottom = img.crop((0, h - 1, w, h)).resize((w, w - h - pad), Image.NEAREST)
            new_img = Image.new("RGB", (w, w))
            new_img.paste(top, (0, 0))
            new_img.paste(img, (0, pad))
            new_img.paste(bottom, (0, pad + h))
        else:
            pad = (h - w) // 2
            left = img.crop((0, 0, 1, h)).resize((pad, h), Image.NEAREST)
            right = img.crop((w - 1, 0, w, h)).resize((h - w - pad, h), Image.NEAREST)
            new_img = Image.new("RGB", (h, h))
            new_img.paste(left, (0, 0))
            new_img.paste(img, (pad, 0))
            new_img.paste(right, (pad + w, 0))

    new_img.save(img_output_path)


def posterize_pixelate(image_path, img_output_path=None, w_out=640, h_out=360, palette=None, crop=False,
                       blur_before_posterize=False, blur_radius=0.5, method='BOX'):

    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')

    if not img_output_path:
        img_output_path = f'{image_path.split(".")[0]}_pixel.{image_path.split(".")[1]}'

    if palette is None:
        palette = palettes.cyan_magenta_palette

    resampling_method = getattr(Image.Resampling, method, 'BOX')

    if crop:
        aspect_ratio = w_out / h_out
        w_img, h_img = img.size
        if w_img / h_img > aspect_ratio:
            w_img_cropped = int(h_img * aspect_ratio)
            left = (w_img - w_img_cropped) // 2
            img = img.crop((left, 0, left + w_img_cropped, h_img))
        else:
            h_img_cropped = int(w_img / aspect_ratio)
            top = (h_img - h_img_cropped) // 2
            img = img.crop((0, top, w_img, top + h_img_cropped))
        img = img.resize((w_out, h_out), resampling_method)

    else:
        img = img.resize((w_out, h_out), resampling_method)

    if blur_before_posterize:
        img = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    img_array = np.array(img)
    posterized = np.zeros_like(img_array)
    palette_array = np.array(palette)

    height, width = img_array.shape[:2]
    for y in range(height):
        for x in range(width):
            pixel = img_array[y, x]
            distances = np.sum(np.abs(palette_array - pixel), axis=1)
            closest_idx = np.argmin(distances)
            posterized[y, x] = palette_array[closest_idx]

    new_img = Image.fromarray(posterized.astype('uint8'))
    new_img.convert("P", palette=Image.ADAPTIVE, colors=256).save(img_output_path.replace("jpg", "png"))


if __name__ == '__main__':
    input_files = [
        r'D:\2D Assets\_stock_images\toronto\pexels-souvenirpixels-1519088.jpg',
        r'D:\2D Assets\_stock_images\toronto\pexels-harrisonhaines-2973098.jpg',
        r'D:\2D Assets\_stock_images\toronto\pexels-mateusz-17796165.jpg',
    ]
    output_folder = r'D:\2D Assets\Python'

    for input_file in input_files:
        filename = input_file.rsplit('\\', 1)[-1]
        print('processing:', filename)
        output_file = output_folder + '\\' + filename.replace('.jpg', '_pixel.png')
        posterize_pixelate(input_file, img_output_path=output_file, crop=True)
