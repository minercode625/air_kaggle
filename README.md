# AIR Lab Kaggle Project

This is a project for CAU AIR Lab. Similar to Kaggle.

## Requirements

Mysql  
Python (Flask)  
Pytorch (Optional)

## Initialization

Change name "auth_temp.dat" file to "auth.dat"  
Fill configuration  
Turn on Mysql and make db file

```sql
CREATE DATABASE user_auth;
USE user_auth;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    username VARCHAR(50),
    password VARCHAR(50)
);
```
