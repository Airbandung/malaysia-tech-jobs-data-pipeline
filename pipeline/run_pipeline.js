const extractStates = require('./extract/states_extract');

const transformStates = require('./transform/states_transform');

const {loadStatesData} = require('./load/states_load');
const logger = require('../utils/logger');


async function runPipeline() {
  try {
    logger.log('Starting data pipeline...');

    // 1. Extract raw data
    const rawData = extractStates.extractStatesData();
    logger.log('Raw data extracted.');

    // 2. Transform data
    const transformedData = transformStates.transformStates(rawData);

    logger.log(`Data transformed. ${
        transformedData.length} records ready for loading.`);

    // 3. Inject transformed data
    await loadStatesData(transformedData);
    logger.log(`Loaded ${transformedData.length} records.`);

    logger.log('Data pipeline executed successfully!');
  } catch (error) {
    logger.log('Error executing data pipeline:', error);
  }
}

runPipeline().catch(error => {
  logger.log('Error executing data pipeline:', error);
});