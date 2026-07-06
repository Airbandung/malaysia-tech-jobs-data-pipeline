require('dotenv').config();
const fs = require('fs');
const {Client} = require('pg');

// 1. Load raw data
const rawData = JSON.parse(fs.readFileSync('./data/states_raw.json', 'utf-8'));

// 2. Connect to PostgreSQL
const client = new Client({
  user: process.env.DB_USER,
  host: process.env.DB_HOST,
  database: process.env.DB_NAME,
  password: process.env.DB_PASSWORD,
  port: process.env.DB_PORT,
});

async function run() {
  try {
    await client.connect();
    console.log('Connected to database');

    // 3. Insert each row
    for (let state of rawData) {
      const population = Number(state.population.replace(/,/g, ''));

      await client.query(
          'INSERT INTO states (name, population) VALUES ($1, $2)',
          [state.name, population]);
    }

    console.log('Data inserted successfully');
  } catch (err) {
    console.error('Error:', err);
  } finally {
    await client.end();
  }
}

run();