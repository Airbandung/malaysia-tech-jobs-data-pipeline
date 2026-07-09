const extractStates = require('./extract/states_extract');

const transformStates = require('./transform/states_transform');

const {loadStatesData} = require('./load/states_load');

async function runPipeline() {
  try {
    console.log('Starting data pipeline...');

    // 1. Extract raw data
    const rawData = extractStates.extractStatesData();
    console.log('Raw data extracted.');

    // 2. Transform data
    const transformedData = transformStates.transformStates(rawData);
    console.log('Data transformed.');

    // 3. Inject transformed data
    await loadStatesData(transformedData);
    console.log('Transformed data loaded.');

    console.log('Data pipeline executed successfully!');
  } catch (error) {
    console.error('Error executing data pipeline:', error);
  }
}

runPipeline().catch(error => {
  console.error('Error executing data pipeline:', error);
});