# guacamole

Контейнеризованный стенд Apache Guacamole c PostgreSQL-бэкендом, сервером записей сессий и дополнительным VPN-периметром на WireGuard.

## Требования

- Docker 24+ и Docker Compose v2
- GNU Make
- Пользователь с правами `sudo` (цель `make deploy` меняет владельца `_data/guacd/record`)
- Свободные порты: 80/tcp, 8080/tcp, 8081/tcp, 8999/tcp, 5000/tcp, 51820/udp

## Состав стенда

| Сервис | Образ | Назначение | Порты/URL |
| --- | --- | --- | --- |
| `nginx` | `nginx:1.27-alpine` | Обратный прокси для Guacamole и просмотра записей, WebSocket-терминация | `80 -> /guacamole` и `/recordings` |
| `guacamole` | `guacamole/guacamole:1.6.0` | Веб-клиент Apache Guacamole (Tomcat) | `8080:8080`, также проброшен через `nginx` |
| `guacd` | `guacamole/guacd:1.6.0` | Демон протоколов VNC/RDP/SSH/Telnet | 4822/tcp (внутри сети `guacnetwork_compose`) |
| `postgres` | `postgres:18.0-alpine3.21` | Хранилище конфигураций и пользователей | 5432/tcp (внутри сети) |
| `pgadmin` | `dpage/pgadmin4:9.8.0` | UI для управления PostgreSQL | `8999:80` |
| `guacamole_recordings` | `tomcat:10.1-jdk17` | Отдаёт записи сессий из `_data/guacd/record` | `8081:8080`, также доступно как `/recordings` через `nginx` |
| `wireguard` | `linuxserver/wireguard:v1.0.20210914-ls6` | VPN-шлюз WireGuard + проброс порта для UI | `51820/udp` для клиентов, `5000/tcp` для UI |
| `wireguard-ui` | `ngoduykhanh/wireguard-ui:latest` | Веб-панель управления WireGuard (делит сеть с `wireguard`) | Доступна через `http://localhost:5000` |

Все сервисы подключены к пользовательской подсети `172.29.0.0/24` с фиксированными IP-адресами (см. `docker-compose.yml`).

## Структура репозитория

- `docker-compose.yml` – точное описание всех сервисов, сетей, volume и healthcheck'ов.
- `Makefile` – цели `pull`, `deploy`, `down`, `prune`; каждая запускает `docker compose -p guacamole -f docker-compose.yml`.
- `env_files/*.env` – параметры PostgreSQL, Guacamole и PgAdmin.
- `_data/guacd/record` – каталог записей; примонтирован в `guacd`, `guacamole` и `guacamole_recordings`.
- `_data/guacd/drive` – общий «диск» для операций копирования файлов.
- `_data/guacamole` – конфигурация Guacamole (`guacamole.properties`, tar-пакеты расширений).
- `_data/postgres` – SQL-инициализация БД (включая создание пользователя `guacadmin`).
- `_data/tomcat/conf/...` – описание контекста `/recordings` для Tomcat.
- `_data/wireguard/{config,db}` – конфигурации сервера и данные UI.
- `nginx/nginx.conf`, `nginx/conf.d/default.conf` – прокси-логика и правила WebSocket.

## Настройка окружения

### env_files

- `env_files/postgres.env` – значения `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`. Используются как в контейнере Postgres, так и PgAdmin при подключении.
- `env_files/guacamole.env` – флаги `RECORDING_ENABLED`, `RECORDING_SEARCH_PATH=/record`, `QUICKCONNECT_ENABLED`, а также DSN к PostgreSQL. Здесь же включено автоматическое создание пользователей (`POSTGRESQL_AUTO_CREATE_ACCOUNTS=true`).
- `env_files/pgadmin.env` – логин/пароль PgAdmin. После входа добавьте сервер с хостом `postgres`, портом `5432`, пользователем `guacamole` и паролем `guacamole`.

Пересоберите стек после изменения любого файла `.env`.

### Постоянные каталоги

Команда `make deploy` гарантирует существование `_data/guacd/record` и выставляет владельца `1000:1001` с правами `775` (именно эти UID/GID используются в официальном образе `guacamole`). Остальные каталоги создаются Docker автоматически, но их можно подготовить вручную:

- `_data/guacamole/extensions` – положите дополнительные расширения Guacamole (`.tar.gz`).
- `_data/wireguard/config` – хранит `wg0.conf`; не удаляйте при обновлениях.
- `_data/wireguard/db` – база `wireguard-ui` со списком клиентов.

## Развертывание

1. Скачать образы:
   ```bash
   make pull
   ```
2. Запустить все сервисы (требует `sudo` для подготовки каталога записей):
   ```bash
   make deploy
   ```
3. Остановить и удалить стек вместе с volume (будьте осторожны – данные будут удалены):
   ```bash
   make down
   ```
4. Очистить Docker-хост:
   ```bash
   make prune
   ```

Для ручного запуска используйте `docker compose -f docker-compose.yml -p guacamole up -d`.

## Доступ к сервисам и учетные данные

| Назначение | URL/порт | Учетные данные по умолчанию | Примечание |
| --- | --- | --- | --- |
| Guacamole через `nginx` | `http://localhost/guacamole/` | `guacadmin / guacadmin` (создаётся в `_data/postgres/01_create_guacamole_db.sql`) | Смените пароль после первого входа |
| Guacamole напрямую | `http://localhost:8080/guacamole/` | те же | Удобно для отладки Tomcat |
| Просмотр записей | `http://localhost/recordings/` или `http://localhost:8081/recordings/` | не требуется | Файлы лежат в `_data/guacd/record/${HISTORY_UUID}` |
| PgAdmin 4 | `http://localhost:8999` | `pgadmin4@pgadmin.org / admin` | Добавьте сервер `postgres:5432` |
| PostgreSQL | `postgres:5432` (внутренняя сеть) | `guacamole / guacamole` | Используется Guacamole и PgAdmin |
| WireGuard UI | `http://localhost:5000` | `admin / CyberDSTPASS` | Значения задаются в `docker-compose.yml`, рекомендуем заменить |
| WireGuard VPN | `<ваш_хост>:51820/udp` | ключи генерируются в UI | Конфигурации сохраняются в `_data/wireguard/config` |

## Конфигурация записи сессий

В контейнере Guacamole включены флаги `RECORDING_ENABLED=true` и `RECORDING_SEARCH_PATH=/record`, поэтому достаточно указать путь в настройках подключения:

1. Перейдите в `http://<host>/guacamole/#/settings/postgresql/connections` под `guacadmin`.
2. Создайте или отредактируйте подключение:
   - **Recording path:** `/record/${HISTORY_UUID}`
   - **Recording name:** `session` (или любое другое)
   - **Create recording path automatically:** включить.
3. Сохраните подключение и выполните тестовую сессию. Файлы появятся в `_data/guacd/record/<UUID>/session.guac`.

Сервер `guacamole_recordings` монтирует тот же каталог в режиме `ro` и публикует его через Tomcat, а `nginx` проксирует `/recordings` наружу.

## Управление и диагностика

- Проверить состояние контейнеров:
  ```bash
  docker compose -p guacamole -f docker-compose.yml ps
  ```
- Общие логи:
  ```bash
  docker compose -p guacamole -f docker-compose.yml logs -f
  ```
- Логи конкретного сервиса:
  ```bash
  docker compose -p guacamole -f docker-compose.yml logs guacd
  ```
- Переcтартовать сервис:
  ```bash
  docker compose -p guacamole -f docker-compose.yml restart guacamole
  ```

## Траблшутинг записей

**Записи не отображаются в каталоге**

1. Убедитесь, что права каталога корректны:
   ```bash
   ls -la _data/guacd/record/
   # ожидается: drwxrwxr-x 1000 1001
   ```
2. При необходимости восстановите владельца:
   ```bash
   sudo chown -R 1000:1001 _data/guacd/record
   sudo chmod -R 775 _data/guacd/record
   ```
3. Проверьте, что в настройках подключения указан путь `/record/${HISTORY_UUID}` (без `${HISTORY_PATH}`).
4. Проанализируйте логи `guacd`:
   ```bash
   docker compose logs guacd | grep -i recording
   ```

**Ошибка `No such file or directory` в `guacd`**

- Опция *Create recording path automatically* должна быть включена.
- Директория `_data/guacd/record` должна существовать до старта контейнера.

**Запись не воспроизводится в браузере**

- Проверьте, что файлы есть в `_data/guacd/record/<UUID>/`.
- Убедитесь, что `guacamole` и `guacamole_recordings` имеют доступ только для чтения (права `775`).
- Перезапустите Tomcat-подсистему:
  ```bash
  docker compose restart guacamole guacamole_recordings
  ```

## WireGuard

- Конфигурация сервера хранится в `_data/wireguard/config/wg0.conf`, а база UI – в `_data/wireguard/db`.
- Параметры `PostUp`/`PostDown` нужно задать в интерфейсе `wireguard-ui` (раздел Server settings). Для подсети `10.100.0.0/24` используйте:
  ```bash
  # PostUp
  iptables -A FORWARD -i %i -o eth0 -j ACCEPT; iptables -A FORWARD -i eth0 -o %i -m state --state RELATED,ESTABLISHED -j ACCEPT; iptables -t nat -A POSTROUTING -s 10.100.0.0/24 -o eth0 -j MASQUERADE

  # PostDown
  iptables -D FORWARD -i %i -o eth0 -j ACCEPT; iptables -D FORWARD -i eth0 -o %i -m state --state RELATED,ESTABLISHED -j ACCEPT; iptables -t nat -D POSTROUTING -s 10.100.0.0/24 -o eth0 -j MASQUERADE
  ```
- После перезагрузки хоста убедитесь, что `wireguard` поднят (`docker compose ps`) и что правила NAT применены заново.

## Вклад

1. Вносите изменения в конфигурацию.
2. Проверяйте развертывание: `make deploy`.
3. Прогоняйте smoke-тесты (вход в Guacamole, открытие `/recordings`, доступ в PgAdmin).
4. Документируйте новые особенности перед созданием PR.
