# views.py函数简介：

### Blueprint
> 用于组织和管理路由和视图函数

### login
> 用户登录认证：
> 
> 如果用户名和密码正确，将生成一个JWT token，并将其保存到session中

### logout
> 用户注销，从会话中移除token，不解释

### record
> 保存数据记录到数据库

### admin/device
> 保存设备信息到数据库

### admin/devices
> 获取所有设备的信息

### status/<room_id>
> 获取特定房间的设备状态

### status
> 获取设备状态

### room/check_in
> 保存入住时间到数据库

### room/check_out
> 保存退房时间到数据库

### check_auth
> 使用JWT检查请求是否经过身份验证

### unauthorized
> 处理未经授权的访问，返回401错误