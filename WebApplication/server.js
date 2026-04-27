import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';
import mysql from 'mysql2/promise';
import { CosmosClient } from "@azure/cosmos";

dotenv.config();

const app = express();

// needed for __dirname in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Cosmos
const client = new CosmosClient({
  endpoint: process.env.COSMOS_ENDPOINT,
  key: process.env.COSMOS_KEY
});

const database = client.database("iotdb");
const container = database.container("container1");

// serve static files
app.use(express.static('public'));

const db = mysql.createPool({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    waitForConnections: true
})

app.get('/simulation', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'simulation.html'));
});

app.get('/api/test-db', async (req, res) => {
    try {
        const [rows] = await db.query('SELECT 1 AS connected');
        res.json({ success: true, result: rows[0] });
    } catch (error) {
        console.error(error);
        res.status(500).json({ success: false, error: 'Database connection failed' });
    }
});

app.get('/api/latest', async (req, res) => {
    try {
        const [rows] = await db.query(`
            SELECT temperature, luminosite, ouverture, mode, status, date
            FROM data
            ORDER BY date DESC
            LIMIT 1
        `);

        if (rows.length === 0) {
            return res.json(null);
        }

        res.json(rows[0]);
    } catch(error) {
        console.error(error);
        res.status(500).json({ error: 'Error fetching last data '});
    }
});

// API
app.get("/api/data", async (req, res) => {
  try {
    const { resources } = await container.items
      .query("SELECT * FROM c ORDER BY c.Body.date DESC")
      .fetchAll();

    res.json(resources);
  } catch (err) {
    console.error(err);
    res.status(500).send("error");
  }
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});