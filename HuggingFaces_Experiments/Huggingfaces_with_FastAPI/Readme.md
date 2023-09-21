# Fast API based application

# to install torch with CUDA support
pip install torch==2.0.1+cu118  torchvision -f https://download.pytorch.org/whl/torch_stable.html cudatoolkit=11.8 -c pytorch

## Run the application
```
uvicorn main:app --reload --port=8000 --host=127.0.0.1
```

[Check](http://127.0.0.1:8000) to ensure that app is running 

[After, proceed to](http://127.0.0.1:8000/docs)
![Alt text](HuggingFaces_Experiments\Huggingfaces_with_FastAPI\src\static\Main_Screen.png)


### uvicorn

[Helpful tutorial](https://www.tutorialspoint.com/fastapi/fastapi_uvicorn.htm)


### Note:
If you are seeing warning about model you might need to downgrade the version of PYDANTIC.

```
pip install pydantic=1.10.11 --upgrade
```



pip install nvidia-smi