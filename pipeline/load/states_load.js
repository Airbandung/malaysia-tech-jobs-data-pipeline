const client = require('../../config/db');

async function loadStatesData(statesData) {
  await client.connect();

  const query =
      'INSERT INTO states (name, population) VALUES ($1, $2) ON CONFLICT (name) DO UPDATE SET population = EXCLUDED.population;';

  for (const state of statesData) {
    await client.query(query, [state.name, state.population]);
  }
  await client.end();
}

module.exports = {loadStatesData};