# BreachDB

## About

This project is a submission to the DeepCode challenge. It aims to achieve the following:

- Parse breach data from large text files.
- Store it in a relational database (MySQL).
- Enrich the data with additional information.
- Allow users to search the database and filter breach data.

## Technologies Used

- Python
  - pandas
- MySQL

## Challenges Faced

- determining whether a page has a captcha
- determining whether a page has a login form
- ensuring optimal parsing performance

# Prerequisites (for Windows 11):

1. Set Up MySQL

   - **Install MySQL**

     - Download the MySQL Community Edition from the [official MySQL website](https://dev.mysql.com/downloads/installer/).

     - Run the installer and select Server Only (or the configuration that suits your needs).

     - Include the MySQL binary directory in your system PATH environment variable

   - **Create a Database**

     - Open CMD

     - Enter command `mysql -u root -p`, then enter the root password.

     - Create a database called "breach_data" using command `CREATE DATABASE breach_data;`

     - Select database "breach_data" using command `USE breach_data`

2.
