#!/usr/bin/env node
const net = require('net');
// Configuration
const args = process.argv.slice(2);
let host = null;
let port = null;
// List of sources to ignore
const IGNORED_SOURCES = new Set([ 
    'PGM',
    'PVW',
    'ME2 PGM',
    'ME3 PGM',
    'STOR 1',
    'STOR 5'
]);
// Process arguments
for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
        case '-h':
            host = args[++i];
            break;
        case '-p':
            port = parseInt(args[++i]);
            break;
        case '--debug':
            process.env.DEBUG = 'true';
            break;
        case '--help':
            console.log('Usage: node script.js [-h host] [-p port] [--debug]');
            process.exit(0);
    }
}
function cleanSourceName(text) { // The source names have some shitespace, or unused bytes at the start and end of the name, this needs to be removed in order to compared the sources against the 'Ignore List'
    return text
        .replace(/^\x00+/, '')     
        .replace(/\x00+$/, '')     
        .trim();                  
}
function interpretTallyStatus(controlByte, sourceName) {
    // Clean the source name
    const cleanName = cleanSourceName(sourceName);
    
    if (process.env.DEBUG) {
        console.log('=======================================');
        console.log(`Raw source: ${cleanName}`);
        console.log(`In ignore list?: ${IGNORED_SOURCES.has(cleanName)}`);
        console.log(`Control byte: 0x${controlByte.toString(16).toUpperCase()}`);
        console.log('=======================================');
    }
    
    // Check against ignore list
    if (IGNORED_SOURCES.has(cleanName)) {
        return null;
    }
    switch (controlByte) {
        case 0x90:
        case 0xA0:
            return `${cleanName}`;
        default:
            return null;
    }
}
function parseKahunaTally(data) {
    const messages = [];
    const chunkSize = 24;
    for (let offset = 0; offset < data.length; offset += chunkSize) {
        if (offset + chunkSize <= data.length) {
            const chunk = data.slice(offset, offset + chunkSize);
            const controlByte = chunk[8];
            const text = chunk.slice(10, 24).toString('ascii');
            const status = interpretTallyStatus(controlByte, text);
            if (status) {
                messages.push(status);
            }
        }
    }
    return messages;
}
const client = new net.Socket();
client.connect(port, host);
client.on('data', (data) => {
    const messages = parseKahunaTally(data);
    messages.forEach(msg => console.log(msg));
});
client.on('error', (err) => {
    console.error('Connection error:', err);
});
// Dissconnect
process.on('SIGINT', () => {
    client.destroy();
    process.exit(0);
});
