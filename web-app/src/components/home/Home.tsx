import axios from "axios";
import { useState } from "react";
import styled from "styled-components";
import _ from "lodash";
import { environment } from "../../environments/environment-prod";

const Container = styled.div`
  display: flex;
  justify-content: center;
  margin-top: 20px;
`;

const SelectionContainer = styled.div``;

const Button = styled.button`
  background: inherit;
  border: 2px solid lightgrey;
  color: white;
  margin: 0 1em;
  padding: 15px;
  position: center;
  color: white;
  font-size: 20px;
  font-family: inherit;
  border-radius: 5px;
  cursor: pointer;
`;

const EditorInput = styled.textarea`
  margin: 2px;
  border: none;
  border: 3px solid black;
  font-family: inherit;
  font-size: 50%;
  position: center;
  width: 35vw;
  height: 50vh;
  background: lightgrey;
  resize: none;
  boxshadow: 10px 10px 10px #f4aab9;
`;

const EditorOutput = styled.div`
  margin: 2px;
  border: none;
  border: 3px solid black;
  font-family: inherit;
  font-size: 50%;
  width: 35vw;
  height: 50vh;
  background: lightgrey;
  resize: none;
  position: center;
  bottom: 0;
  overflow-y: scroll;
  white-space: pre;
  margin: 0;
  padding: 0;
  justify-content: start;
`;

const LanguageSelection = styled.select`
  background: inherit;
  border-radius: 2px;
  border: 2px solid lightgrey;
  color: white;
  padding: 5px;
  font-size: 50%;
  font-family: inherit;
`;

const codeLanguages = [
  { label: "Python", value: "PYTHON3" },
  { label: "Java", value: "JAVA" },
  { label: "Kotlin", value: "KOTLIN" },
];

const Home = () => {
  const [value, setValue] = useState("");
  const [highlighting, setHighlighting] = useState(null);
  const [language, setLanguage] = useState("PYTHON3");
  const [latency, setLatency] = useState(null);

  const highlight = async (src: String) => {
    const start = performance.now();

    const response = await axios
      .post(environment.restApi.highlightUrl, {
        sourceCode: src,
        codeLanguage: language,
      })
      .then((res) => {
        const end = performance.now();
        const latency = end - start;

        setLatency(Math.round(latency * 100) / 100);
        return res?.data;
      })
      .catch((err) => {
        return [];
      });
    setHighlighting(response);
  };

  const getStyles = () => {
    return (
      <style>
        {`.ANY {
        color: black;
        font-weight: normal;
        font-style: normal;
    }
    .KEYWORD {
        color: purple;
        font-weight: bold;
        font-style: normal;
    }
    .LITERAL {
        color: lightskyblue;
        font-weight: bold;
        font-style: normal;
    }
    .CHAR_STRING_LITERAL {
        color: #8FBC8F;
        font-weight: normal;
        font-style: normal;
    }
    .COMMENT {
        color: #A9A9A9;
        font-weight: normal;
        font-style: italic;
    }
    .CLASS_DECLARATOR {
        color: blue;
        font-weight: bold;
        font-style: normal;
    }
    .FUNCTION_DECLARATOR {
        color: #FF00FF;
        font-weight: bold;
        font-style: normal;
    }
    .VARIABLE_DECLARATOR {
        color: purple;
        font-weight: bold;
        font-style: normal;
    }
    .TYPE_IDENTIFIER {
        color: #008000;
        font-weight: bold;
        font-style: normal;
    }
    .FUNCTION_IDENTIFIER {
        color: dodgerblue;
        font-weight: normal;
        font-style: normal;
    }
    .FIELD_IDENTIFIER {
        color: red;
        font-weight: normal;
        font-style: normal;
    }
    .ANNOTATION_DECLARATOR {
        color: #F5F5DC;
        font-weight: normal;
        font-style: italic;
    }`}
      </style>
    );
  };

  const getFormatting = () => {
    const result = [];
    highlighting.result.forEach((token, index) => {
      if (index === 0) {
        result.push({
          token: highlighting.src.substring(0, token.start),
          class: token.class,
        });
      } else {
        const prev = highlighting.result[index - 1];
        result.push({
          token: highlighting.src.substring(prev.end + 1, token.start),
          class: token.class,
        });
      }

      result.push({
        token: highlighting.src.substring(token.start, token.end + 1),
        class: token.class,
      });
    });

    const filtered = _.uniq(result, "start");

    return (
      <EditorOutput>
        {getStyles()}
        <code style={{ verticalAlign: "left" }}>
          {filtered.map((r) => {
            return <span className={r.class}>{r.token}</span>;
          })}
        </code>
      </EditorOutput>
    );
  };

  return (
    <div>
      <SelectionContainer>
        <LanguageSelection
          value={language}
          onChange={(e) => {
            setLanguage(e.target.value);
          }}
        >
          {codeLanguages.map((option) => (
            <option value={option.value}>{option.label}</option>
          ))}
        </LanguageSelection>
        <p
          style={{
            color: "#00FF00",
            fontSize: "50%",
          }}
        >
          {latency ? latency + " ms" : ""}
        </p>
      </SelectionContainer>
      <Container>
        <EditorInput
          value={value}
          onChange={(event) => {
            setValue(event.target.value);
          }}
        />
        {highlighting ? getFormatting() : null}
      </Container>

      <Container>
        <Button
          disabled={!value}
          onClick={() => {
            highlight(value);
          }}
        >
          Highlight
        </Button>
      </Container>
    </div>
  );
};
export default Home;
