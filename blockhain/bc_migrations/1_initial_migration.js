const fs = require('fs');

// save the file path on a variable
file = "/app/contracts/Tournament";
// print the file path system wide

const Tournament = artifacts.require(file);

module.exports = async function (deployer) {
    try {
        console.log('File path: ' + file);

        // Deploy the contract
        await deployer.deploy(Tournament);

        // Retrieve the deployed instance of the contract
        const deployedTournament = await Tournament.deployed();

        // Print the contract address
        console.log('Contract deployed at address: ' + deployedTournament.address);
        // save the contract address on a file
        fs.writeFileSync('/app/output/contract_address.txt', deployedTournament.address, 'utf8');
    } catch (error) {
        console.log('Error: ' + error + ' File path: ' + file);
    }
};
