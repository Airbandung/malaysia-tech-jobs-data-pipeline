const {Client} = require('pg');

const client = new Client({
  user: 'admin',
  host: 'localhost',
  database: 'malaysia',
  password: 'admin123',
  port: 5432,
});

async function test() {
  try {
    await client.connect();
    console.log('✅ Connected to PostgreSQL successfully!');
    await client.end();
  } catch (err) {
    console.error('❌ Connection failed:', err);
  }
}

test();