module.exports = function () {
  return {
    year: new Date().getFullYear(),
    generatedAt: new Date().toISOString()
  };
};
