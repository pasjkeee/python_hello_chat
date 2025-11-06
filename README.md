## Запуск проекта на windows

`./.venv/Scripts/fastapi.exe dev main/main.py`

## Запуск проекта чтобы было видно логирование

`uvicorn main.main:app --reload --log-config logging.yaml --log-level info`

## Синхронизация зависимостей uv на windows

`./.venv/Scripts/uv.exe sync`