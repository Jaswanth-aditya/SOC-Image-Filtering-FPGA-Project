from pynq import Overlay, allocate
import numpy as np
import cv2
import matplotlib.pyplot as plt
import time

# Step 1: Capture frame FIRST, release camera
cap = cv2.VideoCapture(0)
time.sleep(2)
ret, frame = cap.read()
cap.release()  # Free camera before touching DMA

if not ret:
    print("Camera failed")
else:
    gray = cv2.resize(frame, (128, 128))
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    print("Input shape:", gray.shape)
    
    # Step 2: NOW load overlay and do DMA
    overlay = Overlay("design_1_wrapper.bit", download=True)
    dma = overlay.axi_dma_0
    
    CHUNK = 4095
    input_data = gray.flatten().astype(np.uint32)
    output_data = np.zeros_like(input_data)
    
    for i in range(0, len(input_data), CHUNK):
        chunk = input_data[i:i+CHUNK]
        
        in_buffer = allocate(shape=chunk.shape, dtype=np.uint32)
        out_buffer = allocate(shape=chunk.shape, dtype=np.uint32)
        
        in_buffer[:] = chunk
        
        dma.recvchannel.transfer(out_buffer)
        dma.sendchannel.transfer(in_buffer)
        dma.sendchannel.wait()
        dma.recvchannel.wait()
        
        output_data[i:i+len(chunk)] = out_buffer
        
        del in_buffer, out_buffer
    
    output_img = output_data.reshape(gray.shape)
    output_img = np.clip(output_img, 0, 255).astype(np.uint8)
    
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.title("Camera Input")
    plt.imshow(gray, cmap='gray')
    plt.subplot(1, 2, 2)
    plt.title("FPGA Output")
    plt.imshow(output_img, cmap='gray')
    plt.show()