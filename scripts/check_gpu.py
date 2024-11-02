import torch
import psutil
import multiprocessing


if torch.cuda.is_available():
    print(f"CUDA is available. Number of GPUs: {torch.cuda.device_count()}")
    for i in range(torch.cuda.device_count()):
        print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
        print(f"  Memory Allocated: {torch.cuda.memory_allocated(i) / (1024**3):.2f} GB")
        print(f"  Memory Reserved: {torch.cuda.memory_reserved(i) / (1024**3):.2f} GB")
else:
    print("CUDA is not available. Using CPU.")


ram = psutil.virtual_memory()
print(f"Total RAM: {ram.total / (1024**3):.2f} GB")
print(f"Available RAM: {ram.available / (1024**3):.2f} GB")

print(f"Number of CPU cores: {multiprocessing.cpu_count()}")
