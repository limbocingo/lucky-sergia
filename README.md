# Lucky Sergia
API para una página de apuestas. **Proyecto para portfolio.**

# How to run?
Clone the repo: 
```shell 
git clone https://github.com/limbocingo/lucky-sergia.git
```

Go to the directory:
```shell 
cd lucky-sergia/
```

Install all dependencies: 
```shell 
pip install -r backend/requirements.txt
```

Run it in Debug mode: 
```shell 
python backend/manage.py start
```

# Documentation
## Create a super User
You'll just have to run this command and give the password and the username of the new admin.
```shell
python backend/manage.py administrator
```

## Users
Users model.

### User Object

> `username [str]`

> `password [str]` 

> `email [str]` 

> `sid [str]` 

> `logged [bool]` 

> `administrator [bool]` 

> `balance [int]` 

> `winrate [int]` 

### List
`/api/v<version>/users/` -> GET

**Return**

Array of [User Object](./README.md#user-object)


### Create
`/api/v<version>/users/` -> POST

**Body** 
```json
{
    "username": "<username>",
    "password": "<password>",
    "email": "<name>@<domain>.<any>"
}
```

**Return**

[User Object](./README.md#user-object)


### Get
`/api/v<version>/users/<sid>` -> GET

**Return**

[User Object](./README.md#user-object)


### Update
`/api/v<version>/users/<sid>` -> PATCH


**Body Example**

```json
{
    // This can be any field you like.
    // NOTE: You can modify more than one at once if the field is valid.
    "username": "Sergi"
}
```


**Return**

[User Object](./README.md#user-object) 

### Remove
`/api/v<version>/users/<sid>` -> DELETE


**Return**

```json
{
    "message": "User removed from DB."
}
``` 

### Login
`/api/v<version>/users/<username>/login/` -> POST


**Body**
```json
{
    "password": "<valid-password>"
}
```

**Return**
```json
{
    "sid": "<sid>"
}
```

### Logout
`/api/v<version>/users/<sid>/logout/` -> POST
