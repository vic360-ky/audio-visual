import wave #open wav file
import struct #unpack stereo
import math #make square
from PIL import Image, ImageFilter #create image
import os
import colorsys #rainbow color


#OPEN AUDIO FILE, GET SAMPLES, CONVERT TO BINARY

#file = "twinkle twinkle.wav"
blur_radius = .5


def generate_visual_from_audio(file):
    with wave.open(file, "rb") as wav_file:
        os.makedirs('frames', exist_ok=True)
        n_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        n_frames = wav_file.getnframes()
    
        sample_rate = wav_file.getframerate()
        samples_per_second = sample_rate
        total_seconds = int(n_frames / sample_rate)

        for second in range(total_seconds):
            wav_file.setpos(second * samples_per_second)
            frames = wav_file.readframes(samples_per_second)
        
            # Unpack stereo samples
            num_samples = len(frames) // 2  # each sample is 2 bytes for 16-bit audio
            samples = struct.unpack("<" + "h" * num_samples, frames)

            # Average L & R channels to get mono
            mono_samples = []
            for i in range(0, len(samples), 2):  # step by 2 for stereo pairs
                left = samples[i]
                right = samples[i + 1]
                mono = int((left + right) / 2)
                mono_samples.append(mono)

            # Convert mono samples to binary
            binary_samples = [format(sample & 0xFFFF, '016b') for sample in mono_samples]

            #CREATE COLORS FROM BINARY

            colors = []
            #HSV
            for val in binary_samples:
                val_int = int(val, 2)
                h = val_int / 255  # hue from 0 to 1
                s = 1.0
                v = 1.0
                r, g, b = colorsys.hsv_to_rgb(h, s, v)
                colors.append((int(r * 255), int(g * 255), int(b * 255)))


            #CALCULATE IMAGE SQUARE

            length = len(colors)
            side = math.ceil(math.sqrt(length))

            length = len(colors)
            side = math.ceil(math.sqrt(length))

            # Pad with black (0, 0, 0) if needed
            while len(colors) < side * side:
                colors.append((0, 0, 0)) 

            #CREATE IMAGE

            img = Image.new('RGB', (side, side))

            for i, color in enumerate(colors):
                x = i % side
                y = i // side
                img.putpixel((x, y), color)

            blurred = img.filter(ImageFilter.GaussianBlur(radius=blur_radius)) 
            blurred.save(f'frames/audio_colors_{second:04d}.png')

        frames = []
        for i in range(total_seconds - 1):
            img1 = Image.open(f"frames/audio_colors_{i:04d}.png")
            img2 = Image.open(f"frames/audio_colors_{i+1:04d}.png")
            frames.append(img1)

            # Generate transition frames
            for alpha in [0.2, 0.4, 0.6, 0.8]:
                blended = Image.blend(img1, img2, alpha)
                frames.append(blended)

        # Add last frame
        frames.append(Image.open(f"frames/audio_colors_{total_seconds-1:04d}.png"))

        # Save as GIF 
        frames[0].save("transitions.gif", save_all=True, append_images=frames[1:], duration=200, loop=0)

    print("GIF created at", os.path.abspath("transitions.gif"))
    return "transitions.gif"


