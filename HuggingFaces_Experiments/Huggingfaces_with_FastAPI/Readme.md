# FastAPI-based Application Installation and Execution Guide

This guide provides instructions for setting up and running a FastAPI-based application. It includes installing Torch with CUDA support, running the application, and addressing common issues.

## Step 1: Install Torch with CUDA Support

To install Torch with CUDA support, use the following pip command:

```bash
pip install torch==2.0.1+cu118 torchvision -f https://download.pytorch.org/whl/torch_stable.html cudatoolkit=11.8 -c pytorch
```

## Step 2: Run the Application

Run the FastAPI application using Uvicorn with the following command:

```bash
uvicorn main:app --reload --port=8000 --host=127.0.0.1
```

You can check if the application is running by opening [http://127.0.0.1:8000](http://127.0.0.1:8000) in your web browser.

## Step 3: Explore the Application

After confirming that the application is running, proceed to the API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to explore the available endpoints and interact with the API.

![Application Main Screen](HuggingFaces_Experiments/Huggingfaces_with_FastAPI/src/static/Main_Screen.png)

## Additional Resources

- If you need assistance with using Uvicorn, you can refer to the [Uvicorn tutorial](https://www.tutorialspoint.com/fastapi/fastapi_uvicorn.htm).

## Note: Addressing Model Warning

If you encounter warnings related to the model, it may be necessary to downgrade the version of Pydantic. You can do this using the following command:

```bash
pip install pydantic==1.10.11 --upgrade
```

## Useful GPU Utilization Tool

If you want to monitor GPU utilization, you can use the command-line utility `nvidia-smi`. Install it with the following command:

```bash
pip install nvidia-smi
```

With these steps, you should have the FastAPI-based application up and running, Torch with CUDA support installed, and solutions to common issues. Enjoy using your application!