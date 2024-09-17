module.exports = {
  networks: {
    development: {
      host: "ganache",
      port: 8545,
      network_id: "5777"  // Match Ganache's network id
    }
  },
  compilers: {
    solc: {
      version: "0.8.19"  // Specify the Solidity version here
    }
  }
};
