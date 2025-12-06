require('dotenv').config();
const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
const { MongoMemoryServer } = require('mongodb-memory-server');
const fs = require('fs');
const path = require('path');
let useMemory = false;
const memory = { products: [], rentalItems: [] };

const Order = require('./models/order');
const Rental = require('./models/rental');
const Customer = require('./models/customer');
const Product = require('./models/product');
const RentalItem = require('./models/rentalItem');
const ordersRouter = require('./routes/orders');
const rentalsRouter = require('./routes/rentals');
const customersRouter = require('./routes/customers');
const errorHandler = require('./middleware/error');

function toCents(v) {
  if (v === undefined || v === null || v === '') return 0;
  const n = Number(v);
  if (Number.isNaN(n)) return 0;
  return Math.round(n * 100);
}

function parseProducts(filePath) {
  const text = fs.readFileSync(filePath, 'utf8');
  const lines = text.split(/\r?\n/).filter(Boolean);
  const items = [];
  for (const line of lines) {
    const parts = line.trim().split(/\s+/);
    if (parts.length < 4) continue;
    const legacyId = parseInt(parts[0], 10);
    const name = parts[1];
    const priceCents = toCents(parts[2]);
    const stock = parseInt(parts[3], 10);
    if (Number.isNaN(legacyId) || Number.isNaN(stock)) continue;
    items.push({ legacyId, name, priceCents, stock, isActive: true });
  }
  return items;
}

async function connect() {
  try {
    const uri = process.env.MONGODB_URI;
    if (uri) {
      await mongoose.connect(uri);
      return;
    }
    const mem = await MongoMemoryServer.create({ instance: { storageEngine: 'wiredTiger' } });
    const memUri = mem.getUri();
    await mongoose.connect(memUri);
  } catch (e) {
    useMemory = true;
  }
}

async function seed() {
  const repoRoot = path.resolve(__dirname, '..', '..');
  const dbDir = path.join(repoRoot, 'Database');
  const saleItems = parseProducts(path.join(dbDir, 'itemDatabase.txt')).map(i => ({
    legacyId: i.legacyId,
    name: i.name,
    salePriceCents: i.priceCents,
    stock: i.stock,
    isActive: i.isActive
  }));
  const rentItems = parseProducts(path.join(dbDir, 'rentalDatabase.txt')).map(i => ({
    legacyId: i.legacyId,
    name: i.name,
    rentalPriceCents: i.priceCents,
    stock: i.stock,
    isActive: i.isActive
  }));
  if (useMemory) {
    memory.products = saleItems;
    memory.rentalItems = rentItems;
  } else {
    await Product.deleteMany({});
    await RentalItem.deleteMany({});
    if (saleItems.length) await Product.insertMany(saleItems);
    if (rentItems.length) await RentalItem.insertMany(rentItems);
  }
}

async function start() {
  await connect();
  await seed();
  const app = express();
  app.use(cors());
  app.get('/api/health', (req, res) => res.json({ ok: true }));
  app.get('/api/products', async (req, res) => {
    const limit = Math.min(parseInt(req.query.limit || '50', 10), 200);
    const skip = parseInt(req.query.skip || '0', 10);
    if (useMemory) {
      const items = memory.products.slice(skip, skip + limit);
      res.json({ items, count: memory.products.length });
    } else {
      const docs = await Product.find({}).sort({ legacyId: 1 }).skip(skip).limit(limit).lean();
      res.json({ items: docs, count: await Product.countDocuments({}) });
    }
  });
  app.get('/api/rental-items', async (req, res) => {
    const limit = Math.min(parseInt(req.query.limit || '50', 10), 200);
    const skip = parseInt(req.query.skip || '0', 10);
    if (useMemory) {
      const items = memory.rentalItems.slice(skip, skip + limit);
      res.json({ items, count: memory.rentalItems.length });
    } else {
      const docs = await RentalItem.find({}).sort({ legacyId: 1 }).skip(skip).limit(limit).lean();
      res.json({ items: docs, count: await RentalItem.countDocuments({}) });
    }
  });
  if (!useMemory) {
    app.use('/api/orders', ordersRouter);
    app.use('/api/rentals', rentalsRouter);
    app.use('/api/customers', customersRouter);
  }
  const port = process.env.PORT_FWD ? parseInt(process.env.PORT_FWD, 10) : 3001;
  app.listen(port, () => {
    process.stdout.write(`http://localhost:${port}/\n`);
  });
  app.use(errorHandler);
}

start();
