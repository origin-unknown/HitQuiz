
# Setup backend

```
% cd backend
% python3 -m venv .
% source bin/activate
% pip install -r requirements.txt
% flask --app src/app.py db upgrade 
% flask --app src/app.py --debug run
```

# Setup frontend

```
% cd frontend 
% npm install
% npm run dev -- --open
```

# Build frontend

```
% npm run build
```
