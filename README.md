![Centerspoke Logo](./imgs/centerspoke.jpg)
## Centerspoke - The open-source cloud data management CLI

![GitHub Repo stars](https://img.shields.io/github/stars/VisionKernel/Centerspoke)
![GitHub forks](https://img.shields.io/github/forks/VisionKernel/Centerspoke)
![GitHub watchers](https://img.shields.io/github/watchers/VisionKernel/Centerspoke)
![GitHub License](https://img.shields.io/github/license/VisionKernel/Centerspoke)
![GitHub issues](https://img.shields.io/github/issues/VisionKernel/Centerspoke)

## About

Introducing Centerspoke, your go-to open-source command-line companion for the seamless management and insightful analysis of cloud data. As a collaborative project driven by a community of passionate developers, Centerspoke aims to simplify and enhance your data-centric workflows.

Centerspoke offers an inclusive and intuitive interface for effortlessly connecting to diverse cloud databases, providing a robust foundation for your data-driven endeavors. Our open-source ethos ensures transparency, flexibility, and continuous improvement as we work together to shape the future of cloud data management.


### Getting Started

Centerspoke allows you to connect to a cloud database from your preferred provider. Adding a database is as easy as running the `python main.py aws` (you can subsitute aws with your preffered cloud provider) command and following the prompts. Once a database is added, you are able to access the previously setup tables and export data to them.

### Importing data

Importing data is easy once connected. Simply select which local Excel files or sheets you want to upload, and import them to new or prexisting tables within your database. The program will automatically recognize the number of columns and data types upon creation of a new table from an Excel sheet. This feature is designed to optimize queries and save space in your database.

### Exporting data

Calling upon a specific table within your database allows for the analysis of that data. As the name suggests, we offer a wide variety of ways to spoke your data. From charts and graphs to formulas and equations you can analyze your data however you want at optimized speeds.

### Converting data 

Converting data is simple with our `convert` option. Easily convert a file such as .txt, .xml, .json, .csv or .xls into a different supported file type. The convert feature allows for the quick conversion of data into a more readable or preferred type. Synatax is `python main.py convert example.csv name_of_new_file.xlxs`.

### Connecting Cloud Database

To connect to your cloud database you will need certain information that is unique for every database and every cloud provider. 
* AWS RDS: Instance Identifier, Database Name, Username, Password, Port (Default 5432)
* Azure SQL: Server Name, Database Name, Username
* Google Cloud SQL: Instance Connection Name, Database Name, Username
* Google Cloud Storage: Bucket Name
* IBM Cloud:
* Orcale Cloud:

### API implementation



### Adding services

  

### Thank you!

Thank you for checking out Centerspoke! As this is an open-source project, we encourage you to contribute to the project in any way you can. Whether its by submitting issue tickets or contributing code to the repo, a little help goes a long way and is always appreciated. 
