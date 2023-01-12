const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');

// initializing the input parameters
let date = '2022-12-20';
let year = +date.split('-')[0];
let product = 'EL';
let zone = 'ES';
let instrument = 'FTB';
let time_period = 'YR'; // accepts: D for day, WE for weekend, Wk for week, M for month, Q for quarter, YR for year, PPA for purchase price allocation

// making the requests
let url = `https://www.omip.pt/en/dados-mercado?date=${date}&product=${product}&zone=${zone}&instrument=${instrument}`;

let filename = `predictions_${date}_${product}_${zone}_${instrument}`;

const JSONToCSV = (objArray, keys) => {
  let csv = keys.join(',');
  objArray.forEach((row) => {
    let values = [];
    keys.forEach((key) => {
      values.push(row[key] || '');
    });
    csv += '\n' + values.join(',');
  });
  return csv;
};

function range(start, stop) {
  // setting up default values for start and stop
  // calling range(i) is equal to calling range(0, i)
  if (stop === undefined) {
    stop = start;
    start = 0;
  }

  if (start > stop) return [];

  return new Array(stop - start).fill(start).map((el, i) => el + i);
}

async function scrapeData(url, time_period, filename, year) {
  const { data } = await axios.get(url);
  var scraped_data = { d: [], d1: [] };
  var $ = cheerio.load(data);
  $(
    '#market-data > div[rel="FTB - YR"] > table > tbody > tr[class="odd"] > td:nth-child(15)'
  ).each((idx, elem) => {
    scraped_data.d.push($(elem).text());
  });

  $(
    '#market-data > div[rel="FTB - YR"] > table > tbody > tr[class="odd"] > td:nth-child(16)'
  ).each((idx, elem) => {
    scraped_data.d1.push($(elem).text());
  });

  // shift works to pull out an element from an array
  scraped_data.d.shift(0);
  scraped_data.d1.shift(0);

  let years = range(year + 1, year + 11);
  let json_data = [];

  for (let i = 0; i < scraped_data.d.length; i++) {
    json_data.push({
      year: years[i],
      d: scraped_data.d[i],
      d1: scraped_data.d1[i],
    });
  }

  let csv_data = JSONToCSV(json_data, ['year', 'd', 'd1']);

  fs.writeFile(`${filename}.csv`, csv_data, (err) => {
    if (err) throw err;
  });

  //console.log(csv_data);
  //console.log(json_data);
}

scrapeData(url, time_period, filename, year);
