# RAG

## Create

```
docker build -t cosci .
docker run -itd \
--name cosci\
--gpus all\
-v C:\Users\angel\Desktop\EduACT\Cosci\src\backend\RAG:\app \ 
cosci:latest \ 
/bin/bash
docker exec -it cosci bash
```

## Execute
```
python util.py
```

## Relative info
[Cosci API](https://hackmd.io/@squall/H1d7GBxa1g)