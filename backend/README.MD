```
backend/
|-- app/
|      |-- views/           # 视图函数
|          |-- auth.py      # 包含登录和注销的视图函数
|          |-- admin.py     # 包含设备管理相关的视图函数
|          |-- control.py   # 处理客户端控制操作
|          |-- client.py    # 处理有关客户端
|          |-- billing.py   # 生成账单和详单的视图函数
|          |-- query.py     # 包含数据查询相关的视图函数
|          |-- room.py      # 包含房间相关的视图函数
|      |-- config.py        # 配置文件
|      |-- run.py           # 构建实例
|      |-- models.py        # 数据库模型
|      |-- utils.py         # 存储辅助函数和工具函数
|-- data/
|      |-- buptse.db        # Sqlite 数据库
|-- cli.py          		# 运行文件
```
## 后端部分交互使用说明文档

> Written by @Conqueror712 🤗

要测试route是否可用，以便进行下一步的开发与使用，请确保拥有以下测试环境：

> 注：并非一定要用这些环境才能进行测试，仅供参考

- OS: Windows 10/11
- API测试工具: Apifox/Postman
- Python环境: requirements.txt中所需的所有第三方库
- Project src: git clone git@github.com:Cloud0310/BUPT-2023-SE-Homework.git
- DBMS: SQLite

### 1. 打开SQLite并创建数据库

请确保你正确安装了SQLite并添加了相应的环境变量，随后打开一个PowerShell输入命令以打开SQLite:

```
sqlite3
```

可以使用以下方法创建一个数据库（方法不唯一，这种方法如果`xxx.db`存在则直接会打开，不存在就创建它）:

```
sqlite>.open buptse.db
```

> 注意，这条命令前面的`sqlite>`不需要我们输入，另外，这会在当前目录下创建，请确保你的路径正确，在本项目中，默认在相对路径`/backend/db/`下

你可以使用以下指令来查看是否成功创建，当然也可以在文件夹中直接查看:

```
>sqlite>.databases
```

另外，如果你发现你的terminal中的输出并不直观，可以使用以下命令来开启格式化输出:

```
sqlite>.header on
sqlite>.mode column
sqlite>.timer on
```

可以使用以下命令来查看你的SQLite配置:

```
sqlite>.show
```

如果你倦了，那么可以使用以下命令来退出SQLite，请尽量不要暴力退出:

```
sqlite>.quit
```

当你想导出完整的`.sql`文件的时候，可以使用如下命令:

```
sqlite3 xxx.db .dump > xxx.sql
```

当然，也可以由`.sql`恢复成`.db`:

```
sqlite3 xxx.db < xxx.sql
```

> 注：这里导出的`.sql`文件的编码格式为ASCII

### 2. 初始化数据库配置

> 注：这里的表结构不一定是最终版的表结构，只是为了便于进行测试

首先当然是要明确我们需要几张表，每张表里有什么，例如:

- Devices表：
    - room：TEXT类型，表示房间号
    - public_key：TEXT类型，表示设备的公钥
        check_ins表：
    - room：TEXT类型，表示房间号
    - check_in_time：存储入住时间的字段，具体类型取决于你希望使用的时间表示方式
    - check_out_time：存储退房时间的字段，具体类型取决于你希望使用的时间表示方式
    - timestamp：存储时间戳的字段，用于记录操作发生的时间

明确了需求，现在我们就来着手创建一下，`CREATE TABLE`语句的基本语法如下:

```
CREATE TABLE database_name.table_name(
   column1 datatype  PRIMARY KEY(one or more columns),
   column2 datatype,
   column3 datatype,
   .....
   columnN datatype,
);
```

> 注：`database_name`在你选定好数据库的时候可以省略

对于我们的项目而言，可以创建这样的表（虽然大小写不敏感，但还是区分为好）:

```
sqlite> CREATE TABLE records(
   id INT PRIMARY KEY     NOT NULL,
   room           TEXT    NOT NULL
);
```

> 注：`NOT NULL`的约束表示在表中创建纪录时这些字段不能为`NULL`

你可以使用以下命令来查看表是否被成功创建:

```
sqlite>.tables
```

更进一步地，你可以使用以下命令得到表的完整信息:

```
sqlite>.schema table_name
```

![image](/img/1.png)

### 3. 完整的创建表命令

```
sqlite> CREATE TABLE Users(
   username TEXT PRIMARY KEY NOT NULL,
   role TEXT NOT NULL
);

sqlite> CREATE TABLE Devices(
   room TEXT PRIMARY KEY NOT NULL,
   public_key TEXT NOT NULL
);

sqlite> CREATE TABLE RoomStatus(
   room TEXT PRIMARY KEY NOT NULL,
   temperature INT NOT NULL,
   wind_speed INT NOT NULL,
   mode TEXT NOT NULL,
   sweep BOOLEAN NOT NULL,
   is_on BOOLEAN NOT NULL,
   last_update TEXT NOT NULL
);

sqlite> CREATE TABLE Reports(
   room TEXT NOT NULL,
   start_time TEXT NOT NULL,
   end_time TEXT NOT NULL,
   temperature INT NOT NULL,
   wind_speed INT NOT NULL,
   mode TEXT NOT NULL,
   sweep BOOLEAN NOT NULL,
   duration INT NOT NULL,
   cost INT NOT NULL,
   PRIMARY KEY (room, start_time),
   FOREIGN KEY (room) REFERENCES RoomStatus(room)
);
```

