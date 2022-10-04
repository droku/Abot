//const { default: axios } = require("axios");
const { GameRunner } = require("./AntEngine/GameRunner");
const { Config } = require("./AntEngine/Config");

const fs = require("fs");

const iterationsToRun = 10;

// const SimulationName = "May09WR";
// const mapURL = "https://antgame.io/assets/dailyMaps/May_09_2022_424328.json";
// const homeLocations = [
//   [20, 8],
//   [49, 71],
//   [58, 93],
//   [62, 37],
//   [111, 8],
//   [161, 25],
//   [169, 82],
//   [172, 109],
// ];
// const runTime = 75;

const SimulationName = "May06WR";
const mapURL = "https://antgame.io/assets/dailyMaps/Apr_30_2022_305163.json";
const homeLocations = [
  [24, 14],
  [50, 96],
  [54, 41],
  [92, 96],
  [93, 32],
  [177, 12],
  [180, 54]
];
const runTime = 70;

const RunSimulations = async () => {
  //const mapData = (await axios.get(mapURL)).data.Map;
  const mapData = Config.Map;
  const data = {
    mapURL,
    homeLocations,
    runTime,
    scores: [],
    timing: {
      start: new Date().toISOString(),
    },
  };
  for (let i = 0; i < iterationsToRun; i++) {
    const seed = Math.round(Math.random() * 1e8);
    const mapCopy = mapData.map(line => line.slice());

    const { score } = GameRunner.SimulateRun({
      time: runTime,
      mapData: mapCopy,
      homeLocations,
      seed,
    });

    data.scores.push({ seed, score });
    console.log(new Date().toISOString(), `${i + 1}/${iterationsToRun}`, score, seed);
  }

  data.timing.end = new Date().toISOString();

  const fileName = `score.json`;
  fs.writeFileSync(fileName, JSON.stringify(data));
};

RunSimulations();
