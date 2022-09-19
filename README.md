# Syntax Highlighting Web Service with Continuous Fine-tuning

<p align="justify">A novel bachelor thesis implementation of a web service for code syntax highlighting using a deep learning approach. It consists of several micro services, in order to provide highlighting predictions and to carry out the necessary logic to build and validate potential new ML models for continuous fine-tuning and deployment.
</p>

## About

<p align="justify">With the presence of online collaborative tools such as GitHub, StackOverflow and Slack for software development, code is shared and consulted in an array of shapes and contexts be it code review, viewers and snippets. In the context of syntax highlighting, systems of regular expressions and lexing program files are state of practice and are utilized for approximating lexical as well as grammatical structures. Although systems of regular expressions require more work to develop and to maintain, it is preferred due to its fast and lightweight solution that can be applied to any language derivation. This thesis, however, implements a web service that aims to incorporate a statistical solution and improves with the number of incoming requests based on deep-learning to the domain of syntax highlighting. Furthermore, we train our models for the programming languages Python 3, Java and Kotlin by lexing and parsing the source codes of public repositories on GitHub. This thesis shows that with a constant prediction latency, the accuracy of the web service increases for both code files and code snippets as more source codes are supplied. The oracle data sets used for validating the service can also be found in this repository.</p>

### Deployed Instance (As of Sept. 2022)
[Demo](http://benlegiang.ch)

### Public REST Endpoint (As of Sept. 2022)
POST http://benlegiang.ch:8081/api/v1/highlight
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
* Gradle


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

