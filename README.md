# Workmate-Test-Task
> Тестовое задание на позицию Python Backend-developer

##  О проекте

Скрипт расчета медианы трат студентов на кофе за период сессии. Обрабатывает **csv** файлы с заголовками **student** и **coffee_spent**.

## Требования
Перед началом работы убедитесь, что на вашей системе установлены:
- **Python**

## Установка

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/serejka-xaker/Workmate-Test-Task.git
cd Workmate-Test-Task
```
### 2.1 Создайте и активируйте виртуальное окружение и установите зависимости (Windows cmd)
```cmd
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```
### 2.1 Создайте и активируйте виртуальное окружение и установите зависимости (Windows powershell)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
### 2.1 Создайте и активируйте виртуальное окружение и установите зависимости (Linux)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Запуск скрипта
## Доступные отчеты
- **median-coffee**

### 1. Запуск скрипта на Linux
```bash
python3 main.py --files <путь к файлу/файлам через пробел> --report <название отчета>
```
### 2. Запуск скрипта на Windows
```bash
python main.py --files <путь к файлу/файлам через пробел> --report <название отчета>
```
### 3. Пример запуска скрипта
<img width="1890" height="807" alt="image" src="https://github.com/user-attachments/assets/0deba2af-77df-42e9-951c-c70e17f20dc0" />

