# Syntax Highlighting Web Service with Continuous Fine-tuning

<p align="justify">A novel bachelor thesis implementation of a web service for code syntax highlighting using a deep learning approach. It consists of several micro services, in order to provide highlighting predictions and to carry out the necessary logic to build and validate potential new ML models for continuous fine-tuning and deployment.
</p>

## About

<p align="justify">Syntax Highlighting (SH) plays a substantial role in the daily lives of software developers and can be truly found everywhere where code is developed and shared. It enhances productivity by assigning different colors to text to not only serve the user information about the features and grammatical structure of a language but to also increase the readability of code. With the goal to provide a smart and user-friendly SH solution to the public for the mainstream programming languages Java, Kotlin and Python, we implement a web service that is quick to set up, easily accessible and requires no manual maintenance since it autonomously and continuously improves with the number of submitted requests by incorporating a fine-tuning logic for deep learning models. We show that our SH solution produces instantaneous response times and is able to continuously achieve decent to highly accurate SH results by learning from user requests.</p>

### Deployed Instance (As of Sept. 2022)
[Demo](http://api.benlegiang.ch)

### Public REST Endpoint (As of Sept. 2022)
POST http://api.benlegiang.ch:8081/api/v1/highlight
```json
 {
    "codeLanguage": "PYTHON3",
    "sourceCode": "from lib2to3.pygram import python_symbols\nimport pickle\nfrom datetime import datetime\nimport random\nfrom app.utils.SHModelUtils import JAVA_LANG_NAME, KOTLIN_LANG_NAME, PYTHON3_LANG_NAME, SHModel\nfrom app.utils.services.MongoDatabase import MongoDatabase\nimport logging\nimport requests\n\nlogging.basicConfig(filename=\"logs.txt\")"
}

```

### Built With

#### Languages
* Python
* TypeScript
* Java

#### Technologies
* Docker
* React
* MongoDB
* Express
* Gunicorn
* Flask
* Gradle with Spring Boot


## Getting Started

You can run the project locally by following these steps.

### Prerequisites

* Docker
* Docker Compose

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/benlegiang/syntax-highlighting-service.git
   ```
3. Change directory to repository
   ```sh
   cd syntax-highlighting-service
   ```
4. Start all services
   ```sh
   sh run.sh
   ```
## License [![MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License.


## Contact

Hoàng Ben Lê Giang - hoangben.legiang@uzh.ch

