README – FPGA Image Filtering Project 

This Google Drive folder contains all the files required to understand and run the FPGA-based image filtering project implemented on the PYNQ board.

**Contents:**

* **/pynq-image-filter/** – Contains the Vivado block design and hardware files (including the bitstream and hardware description files). This defines the programmable logic (PL) design with AXI DMA and the custom filter module.
* **design_1_wrapper.bit / .hwh** – These files are used by the PYNQ board to program the FPGA and describe the hardware configuration.
* **image-filter.py** – The Processing System (PS) code written in Python. This script captures an image from a camera, sends it to the FPGA using AXI DMA, receives the processed output, and displays the result.

**How it works:**
The system uses AXI DMA to transfer image data between the processor (PS) and FPGA (PL). The Python code captures an image, preprocesses it, and sends pixel data to the FPGA. The custom hardware filter processes the data in a streaming manner, and the output is returned back to the processor for display.

**Steps to run:**

1. Copy the `.bit` and `.hwh` files to the PYNQ board.
2. Open the provided Python script or Jupyter notebook on the PYNQ environment.
3. Ensure the camera is connected.
4. Run the script to capture input, process it on FPGA, and display the output.

**Note:**

* The design uses chunk-based DMA transfers due to buffer size limitations.
* Display is done using matplotlib for compatibility with the PYNQ environment.
* The project demonstrates hardware acceleration of image processing using FPGA.

