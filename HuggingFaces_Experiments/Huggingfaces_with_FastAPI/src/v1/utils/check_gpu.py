""" the most basic script to check if CUDA is available """
import torch

def get_gpu_info() -> str:
    if torch.cuda.is_available():
        device_count = torch.cuda.device_count()
        current_device = torch.cuda.current_device()
        device_name = torch.cuda.get_device_name(current_device)
        cuda_capability = torch.cuda.get_device_capability(current_device)
        cuda_memory = torch.cuda.get_device_properties(current_device).total_memory / (1024 ** 3)  # Convert to GB
        cuda_memory_free = torch.cuda.memory_reserved(current_device) / (1024 ** 3)  # Convert to GB
        cuda_memory_allocated = torch.cuda.memory_allocated(current_device) / (1024 ** 3)  # Convert to GB

        return f"Number of CUDA devices: {device_count},\n" +\
            f"Current CUDA device: {current_device},\n" + \
            f"Device Name: {device_name},\n" +\
            f"CUDA Capability: {cuda_capability},\n" +\
            f"Total GPU Memory: {cuda_memory:.2f} GB,\n" +\
            f"GPU Memory Allocated: {cuda_memory_allocated:.2f} GB,\n" +\
            f"GPU Memory Free: {cuda_memory_free:.2f} GB"
    else:
        return "CUDA is not available on your system."

if __name__ == "__main__":
    get_gpu_info()
