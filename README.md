# AIR Lab Kaggle Project

This is a project for CAU AIR Lab. Similar to Kaggle.

## Requirements

Mysql  
Python (Flask)  
Pytorch (Optional)  
Scikit-learn

## Initialization

### Initialize Database

1. Change name "auth_temp.dat" file to "auth.dat"
2. Fill configuration
3. Turn on Mysql and make db file
4. Paste this code.

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

### Dataset

1. Put train dataset in a 'data/train/' folder.
2. Put test dataset in a 'data/test/' folder.
