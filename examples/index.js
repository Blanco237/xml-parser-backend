
var path = './catalog.xml';
if (!path) throw new Error('path required');

var fs = require('fs');
var parse = require('..');
var xml = fs.readFileSync(path, 'utf8');
var inspect = require('util').inspect;

var obj = parse(xml);
fs.writeFileSync('./output.json', JSON.stringify(obj));