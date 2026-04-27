import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';
import { CosmosClient } from "@azure/cosmos";
import { Client } from 'azure-iothub';
import mysql from 'mysql2/promise';

dotenv.config();

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const connectionString = process.env.IOTHUB_CONNECTION_STRING;
const serviceClient = Client.fromConnectionString(connectionString);

// needed for __dirname in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const db = await mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'root',
  database: 'iotdb'
});

app.post("/api/command", async (req, res) => {
  const { command, value } = req.body;

  const message = JSON.stringify({
    command: command,
    value: value
  });

  try {
    await serviceClient.open();
    await serviceClient.send("collecteur_temp", message);
    res.send("Command sent");
  } catch (err) {
    console.error(err);
    res.status(500).send("Error sending command");
  }
});

// Cosmos
const client = new CosmosClient({
  endpoint: process.env.COSMOS_ENDPOINT,
  key: process.env.COSMOS_KEY
});

const database = client.database("iotdb");
const container = database.container("container1");

app.use(express.static('public'));


async function getCosmosData() {
  const querySpec = {
    query: "SELECT * FROM c ORDER BY c.Body.date DESC"
  };

  const { resources } = await container.items.query(querySpec).fetchAll();
  return resources;
}

app.get('/simulation', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'simulation.html'));
});

// API
app.get("/api/data", async (req, res) => {
  try {
    const cloudData = await getCosmosData();
    res.json(cloudData);

  } catch (err) {
    console.log("Cloud is down, using local DB");

    try {
      const [rows] = await db.execute(`
        SELECT * FROM data ORDER BY id DESC LIMIT 50
      `);

      const formatted = rows.map(row => ({
        Body: {
          temperature: row.temperature,
          luminosite: row.luminosite,
          ouverture_auto: row.ouverture,
          distance: row.distance,
          mode: row.mode,
          date: Math.floor(Date.now() / 1000)
        }
      }));

      res.json(formatted);

    } catch (e) {
      res.status(500).json({ error: "No data available" });
    }
  }
});
     

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});