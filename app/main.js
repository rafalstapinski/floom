module.paths.push('/usr/local/lib/node_modules');

const electron = require("electron");
const player = require("player");

const {app} = electron;
const {BrowserWindow} = electron;

let win;

function createWindow() {

  win = new BrowserWindow({width: 800, height: 600});
  win.loadURL(`file://${__dirname}/index.html`)
  win.webContents.openDevTools();

  win.on("closed", () => {
    win = null;
  });

}

app.on("ready", createWindow);

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("activate", () => {
  if (win === null) {
    createWindow();
  }
});
