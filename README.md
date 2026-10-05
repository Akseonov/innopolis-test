# innopolis-test

https://github.com/Akseonov/innopolis-test/tree/dev

## Что было сделано

- `src/config.py` — файл конфига
- `src/load_data.py` — загрузка и хранение данных датасета о бух учете компаний
- `src/analysis.py` — код с выполнением анализа датасета

## Запуск прокта

```bash
make deps
make up-d
make shell
python ./src/load_data.py
python ./src/analysis.py
```
