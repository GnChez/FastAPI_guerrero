from fastapi import FastAPI
app = FastAPI()


lista_users = ["hola", "uno", "dos", "tres"]

@app.post("/api/users", response_model=dict)
def crear(user: dict):
    for i in user.values():
        lista_users.append(i)
    return dict(zip(range(len(lista_users)),lista_users))

@app.get("/api/users/{idx}", response_model=dict)
def llegir(idx):
    id = int(idx)
    if id<len(lista_users):
        return {"user":lista_users[id]}
    return {"message":"User not found"}

@app.get("/api/users", response_model=dict)
def llegirTots():
    return dict(zip(range(len(lista_users)),lista_users))

@app.put("/api/users/{idx}", response_model=dict)
def update(idx, mod_user:dict):
    id =int(idx)
    if id < len(lista_users):
        for user in mod_user.values():
            lista_users[id] = user
        return {"user": lista_users[id]}
    return {"message":"User not found"}

@app.delete("/api/usuaris/{idx}", response_model=dict)
def delete(idx):
    lista_users.pop()
    return dict(zip(range(len(lista_users)),lista_users))

