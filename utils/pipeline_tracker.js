const client = require('../config/db');


async function createPipelineRun(name) {
  await client.connect();

  const result = await client.query(
      `
        INSERT INTO pipeline_runs (pipeline_name, status)
        VALUES ($1, $2)
        RETURNING id;
        `,
      [name, 'RUNNING']);

  return result.rows[0].id;
}


async function finishPipelineRun(id, status, records) {
  await client.query(
      `
        UPDATE pipeline_runs
        SET status = $1,
            records_processed = $2,
            finished_at = NOW()
        WHERE id = $3;
        `,
      [status, records, id]);

  await client.end();
}


module.exports = {
  createPipelineRun,
  finishPipelineRun
};