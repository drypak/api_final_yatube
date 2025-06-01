<strong>Мой проект API для Yatube</strong>

<ins>Привет! Это API для работы с постами, комментариями, группами и подписками</ins>


**Что умеет API**

- *Создавать, читать, редактировать и удалять посты*  
- *Добавлять комментарии к постам и менять их*  
- *Просматривать группы и объеденять посты по группам*  
- *Подписываться на других пользователей и искать подписки по никнейму*  


**Как запустить локально**

**1.** <ins>Клонируйте репозиторий</ins>:
```bash
git clone https://github.com/drypak/api_final_yatube.git
cd api_final_yatube
```

**2.** <ins>Создайте и активируйте виртуальное окружение</ins>:
```bash
python -m venv venv
source venv\Scripts\activate или venv/bin/activate на Mac OS
```

**3.** <ins>Установите зависимости</ins>:
```bash
pip install -r requirements.txt
```

**4.** <ins>Сделайте миграции и запустите сервер</ins>:
```bash
python manage.py migrate
python manage.py runserver
```


**Примеры запросов**  
- *<ins>Получить список постов</ins>*:  
  ```http  
  GET /api/v1/posts/  
  ```  
  
- *<ins>Создать пост (требуется авторизация)</ins>*:  
  ```http  
  POST /api/v1/posts/  
  ```
- *<ins>Тело запроса</ins>*:  
  ```json  
  {  
  "text": "Мой первый пост!",  
  "group": 1,  
  "image": null  
  }  
  ```  
- *<ins>Добавить комментарий к посту</ins>*:  
  ```http  
  POST /api/v1/posts/{post_id}/comments/  
  ```  
- *<ins>Тело запроса*</ins>*:  
  ```json  
  {  
  "text": "Вау!"  
  }  
  ```  
- *<ins>Подписаться на пользователя</ins>*:  
  ```http  
  POST /api/v1/follow/  
  ```  
- *<ins>Тело запроса</ins>*:  
  ```json  
  {  
  "following": "username"  
  }  
  ```  


**Авторизация** 
- *Для создания и редактирования нужно авторизоваться. Используется JWT, токены можно получить тут*:
  <ins>Получить токен</ins>:
  ```http
 POST /api/v1/token/
 ```
<ins>Обновить токен</ins>
  ```http
POST /api/v1/token/refresh/
```


