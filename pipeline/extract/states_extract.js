const fs = require('fs');

// 1. Load raw data
function extractStatesData() {
  const rawData =
      fs.readFileSync('./data/states_raw.json', 'utf-8');


  return JSON.parse(rawData);
}

module.exports = {extractStatesData};