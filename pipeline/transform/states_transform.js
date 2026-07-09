function transformStates(rawData) {
  return rawData.map(state => ({
                       name: state.name,
                       population: Number(state.population.replace(/,/g, '')),
                     }));
}

module.exports = {transformStates};