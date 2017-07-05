#!/usr/bin/env node

const commandLineArgs = require('command-line-args')
const spawn = require('child_process').spawn

const optionDefinitions = [
	{name: 'suites', alias: 's', type: String},
	{name: 'taf_profiles', alias:'p', type: String},
	{name: 'taf_clusterId', alias: 'c', type: Number},
	{name: 'maven_profiles', alias: 'm', type: String},
	{name: 'skip_tests', alias: 't', type: Boolean},
	{name: 'log_name', alias: 'l', type: String}
]

const options = commandLineArgs(optionDefinitions)

var mvnArgs = ['clean', 'install'];
if(options.suites){
  mvnArgs.push('-Dsuites=' + options.suites);
}
if(options.taf_profiles){
  mvnArgs.push('-Dtaf.profiles=' + options.taf_profiles);
}
if(options.taf_clusterId){
  mvnArgs.push('-Dtaf.clusterId=' + options.taf_clusterId);
}
if(options.maven_profiles){
  mvnArgs.push('-P' + options.maven_profiles);
}
if(options.skip_tests){
  mvnArgs.push('-DskipTests=true');
}
console.log(mvnArgs);

mvn = spawn('mvn', mvnArgs)
tee = spawn('tee', ['console.log'])

mvn.stdout.pipe(tee.stdin)

mvn.stdout.on('end', () => {
  mvn.emit('close');
});

mvn.on('close', (code) => {
  console.log(`mvn exited with exit code ${code}`);
});

tee.stdout.on('data', (data) => {
  console.log(data.toString());
});

tee.on('close', (code) => {
  console.log(`tee exited with exit code ${code}`);
  allureG = spawn('allure', ['generate', 'target/allure-results']);
  allureG.stdout.on('data', (data) => {
    console.log(data.toString());
});
  allureG.stdout.on('end', () => {
    allureD = spawn('allure', ['report', 'open'])
    allureD.stdout.on('data', (data) => {
      console.log(data.toString());
    });
});
});
