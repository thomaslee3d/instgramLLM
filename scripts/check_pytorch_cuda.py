# check_pytorch_cuda.py

import torch

def test_cuda():
    try:
        print("Starting CUDA Test...")
        print("PyTorch Version:", torch.__version__)
        cuda_available = torch.cuda.is_available()
        print("CUDA Available:", cuda_available)
        if cuda_available:
            print("CUDA Version:", torch.version.cuda)
            print("Number of GPUs:", torch.cuda.device_count())
            print("GPU Name:", torch.cuda.get_device_name(0))
        else:
            print("CUDA is not available. Ensure PyTorch is installed with CUDA support.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_cuda()
