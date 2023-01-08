# Python - JavaScript scripts

### Using pip install for Python script

- Run following command in terminal or bash first: `pip install lxml beautifulsoup4 requests pandas`

### Run Python script locally in terminal

- `python study_case.py date product zone instrument time_period
`
- Values of the variables:

  1. date should be in **YYYY-MM-DD** format.
  2. product should be between EL or NG.
  3. zone should be between ES, PT, FR, DE, ES-PT, PT-ES.
  4. instrument should be between FTB, FTK, FWB, SWB, OEB, FTS
  5. time_period accepts D for day, WE for weekend, Wk for week, M for month, Q for quarter, YR for year, PPA for purchase price allocation

- The following command is an example on how to run the script:

```bash
  $ python study_case.py 2022-12-20 EL ES FTB YR
```

- It's very important to clarify that this script was created to work only with YR, the script could work with the other values but will need an upload.

---

### Using NPM for JavaScript script

- Run `npm install` to install the project dependencies

### Run JavaScript script locally in terminal

```bash
  $ node studyCase.js
```

### HTML table vizualisation

- Open the html file in any browser

- There is a file named `'html_visualization_table_2022-12-20_EL_ES_FTB'` and this example will work to test the pagination because the original table only has 10 rows.

```

```
