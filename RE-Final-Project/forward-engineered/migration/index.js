const fs = require('fs');
const path = require('path');
const mongoose = require('mongoose');
const dotenv = require('dotenv');

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
  const errors = [];
  for (const line of lines) {
    const parts = line.trim().split(/\s+/);
    if (parts.length < 4) { errors.push({ file: path.basename(filePath), line }); continue; }
    const legacyId = parseInt(parts[0], 10);
    const name = parts[1];
    const priceCents = toCents(parts[2]);
    const stock = parseInt(parts[3], 10);
    if (Number.isNaN(legacyId) || Number.isNaN(stock)) { errors.push({ file: path.basename(filePath), line }); continue; }
    items.push({ legacyId, name, priceCents, stock, isActive: true });
  }
  return { items, errors };
}

function parseEmployees(filePath) {
  const text = fs.readFileSync(filePath, 'utf8');
  const lines = text.split(/\r?\n/).filter(Boolean);
  const users = [];
  const errors = [];
  for (const line of lines) {
    const parts = line.trim().split(/\s+/);
    if (parts.length < 5) { errors.push({ file: path.basename(filePath), line }); continue; }
    const username = parts[0];
    const role = parts[1];
    const first = parts[2];
    const last = parts[3];
    const password = parts[4];
    const name = `${first} ${last}`;
    users.push({ username, role, name, password });
  }
  return { users, errors };
}

function parseUserDatabase(filePath) {
  const text = fs.readFileSync(filePath, 'utf8');
  const lines = text.split(/\r?\n/).filter(Boolean);
  const rentals = [];
  const customers = new Set();
  const errors = [];
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (i === 0) continue;
    const parts = line.trim().split(/\s+/).filter(Boolean);
    if (parts.length === 0) continue;
    const phone = parts[0];
    customers.add(phone);
    for (let j = 1; j < parts.length; j++) {
      const entry = parts[j];
      const segs = entry.split(',');
      if (segs.length < 3) { errors.push({ file: path.basename(filePath), line }); continue; }
      const legacyRentalItemId = parseInt(segs[0], 10);
      const dateStr = segs[1];
      const returned = String(segs[2]).toLowerCase() === 'true';
      const rentedAt = returned ? undefined : dateStr;
      const returnedAt = returned ? dateStr : undefined;
      rentals.push({ customerPhone: phone, legacyRentalItemId, rentedAt, returnedAt, returned });
    }
  }
  return { rentals, customers: Array.from(customers), errors };
}

function parseSales(filePath) {
  const text = fs.readFileSync(filePath, 'utf8');
  const lines = text.split(/\r?\n/);
  const orders = [];
  const errors = [];
  let current = null;
  const tsRegex = /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}$/;
  for (const raw of lines) {
    const line = raw ? raw.trim() : '';
    if (!line) continue;
    if (line.startsWith('Total with tax')) continue;
    if (tsRegex.test(line)) {
      if (current) orders.push(current);
      current = { createdAt: line, items: [] };
      continue;
    }
    const parts = line.split(/\s+/);
    if (parts.length < 4) { errors.push({ file: path.basename(filePath), line }); continue; }
    const legacyProductId = parseInt(parts[0], 10);
    const name = parts[1];
    const qty = parseInt(parts[2], 10);
    const lineTotalCents = toCents(parts[3]);
    if (Number.isNaN(legacyProductId) || Number.isNaN(qty)) { errors.push({ file: path.basename(filePath), line }); continue; }
    const unitPriceCents = qty > 0 ? Math.round(lineTotalCents / qty) : 0;
    if (!current) { current = { createdAt: null, items: [] }; }
    current.items.push({ legacyProductId, name, qty, unitPriceCents });
  }
  if (current) orders.push(current);
  const taxBps = 600;
  const filtered = orders.filter(o => Array.isArray(o.items) && o.items.length > 0);
  for (const o of filtered) {
    const subtotalCents = o.items.reduce((acc, it) => acc + it.qty * it.unitPriceCents, 0);
    const grandCents = Math.round(subtotalCents * (1 + taxBps / 10000));
    const taxCents = grandCents - subtotalCents;
    o.totals = { subtotalCents, taxCents, discountCents: 0, grandCents };
  }
  return { orders: filtered, errors };
}

function parseTimestamp(s) {
  if (!s) return null;
  const iso = s.replace(' ', 'T') + 'Z';
  const t = new Date(iso);
  return isNaN(t) ? null : t;
}

function parseMMDDYY(dateStr) {
  if (!dateStr) return null;
  const m = dateStr.match(/^(\d{1,2})\/(\d{1,2})\/(\d{2,4})$/);
  if (!m) return null;
  let [_, mm, dd, yy] = m;
  const month = parseInt(mm, 10) - 1;
  const day = parseInt(dd, 10);
  let year = parseInt(yy, 10);
  if (yy.length === 2) year += year >= 70 ? 1900 : 2000;
  const d = new Date(Date.UTC(year, month, day));
  return isNaN(d) ? null : d;
}

function main() {
  const dryRun = process.argv.includes('--dry-run');
  const root = path.resolve(__dirname, '..');
  const dbDir = path.join(root, 'Database');
  const products = parseProducts(path.join(dbDir, 'itemDatabase.txt'));
  const rentalItems = parseProducts(path.join(dbDir, 'rentalDatabase.txt'));
  const employees = parseEmployees(path.join(dbDir, 'employeeDatabase.txt'));
  const usersDb = parseUserDatabase(path.join(dbDir, 'userDatabase.txt'));
  const sales = parseSales(path.join(dbDir, 'saleInvoiceRecord.txt'));
  const summary = {
    counts: {
      products: products.items.length,
      rentalItems: rentalItems.items.length,
      employees: employees.users.length,
      customers: usersDb.customers.length,
      rentalsEntries: usersDb.rentals.length,
      orders: sales.orders.length
    },
    errors: {
      products: products.errors.length,
      rentalItems: rentalItems.errors.length,
      employees: employees.errors.length,
      userDatabase: usersDb.errors.length,
      sales: sales.errors.length
    }
  };
  const reportPath = path.join(__dirname, 'migration_report.json');
  fs.writeFileSync(reportPath, JSON.stringify(summary, null, 2));
  console.log(JSON.stringify(summary, null, 2));
  if (!dryRun) {
    // connect to MongoDB
    dotenv.config({ path: path.join(root, 'server', '.env') });
    const uri = process.env.MONGODB_URI;
    if (!uri) {
      console.error('Missing MONGODB_URI in server/.env');
      process.exit(1);
    }
    mongoose.set('strictQuery', true);
    mongoose.connect(uri).then(async () => {
      const Product = mongoose.model('Product', new mongoose.Schema({
        legacyId: { type: Number, unique: true },
        name: String,
        salePriceCents: Number,
        stock: Number,
        isActive: Boolean
      }));
      const RentalItem = mongoose.model('RentalItem', new mongoose.Schema({
        legacyId: { type: Number, unique: true },
        name: String,
        rentalPriceCents: Number,
        stock: Number,
        isActive: Boolean
      }));
      const Order = mongoose.model('Order', new mongoose.Schema({
        orderKey: { type: String, unique: true },
        orderedAt: { type: Date },
        cashierUsername: { type: String },
        items: [{ legacyProductId: Number, name: String, qty: Number, unitPriceCents: Number }],
        totals: { subtotalCents: Number, taxCents: Number, discountCents: Number, grandCents: Number },
        source: { type: String, default: 'legacy' }
      }));
      const Rental = mongoose.model('Rental', new mongoose.Schema({
        rentalKey: { type: String, unique: true },
        customerPhone: { type: String },
        legacyRentalItemId: { type: Number },
        rentedAt: { type: Date },
        returnedAt: { type: Date },
        legacyDateStr: { type: String },
        status: { type: String }
      }));
      const Customer = mongoose.model('Customer', new mongoose.Schema({
        phone: { type: String, unique: true }
      }));

      const prodWrites = products.items.map(p => ({
        updateOne: {
          filter: { legacyId: p.legacyId },
          update: { $set: { legacyId: p.legacyId, name: p.name, salePriceCents: p.priceCents, stock: p.stock, isActive: p.isActive } },
          upsert: true
        }
      }));
      const rentWrites = rentalItems.items.map(p => ({
        updateOne: {
          filter: { legacyId: p.legacyId },
          update: { $set: { legacyId: p.legacyId, name: p.name, rentalPriceCents: p.priceCents, stock: p.stock, isActive: p.isActive } },
          upsert: true
        }
      }));
      const orderWrites = sales.orders.map(o => {
        const orderedAt = parseTimestamp(o.createdAt);
        const orderKey = o.createdAt;
        return {
          updateOne: {
            filter: { orderKey },
            update: { $set: { orderKey, orderedAt, items: o.items, totals: o.totals, source: 'legacy' } },
            upsert: true
          }
        };
      });
      const custWrites = usersDb.customers.map(phone => ({
        updateOne: { filter: { phone }, update: { $set: { phone } }, upsert: true }
      }));
      const rentalWrites = usersDb.rentals.map(r => {
        const rentedAt = r.rentedAt ? parseMMDDYY(r.rentedAt) : null;
        const returnedAt = r.returnedAt ? parseMMDDYY(r.returnedAt) : null;
        const status = r.returned ? 'returned' : 'rented';
        const rentalKey = `${r.customerPhone}|${r.legacyRentalItemId}|${r.rentedAt || r.returnedAt}|${status}`;
        return {
          updateOne: {
            filter: { rentalKey },
            update: { $set: {
              rentalKey,
              customerPhone: r.customerPhone,
              legacyRentalItemId: r.legacyRentalItemId,
              rentedAt,
              returnedAt,
              legacyDateStr: r.rentedAt || r.returnedAt || null,
              status,
              source: 'legacy'
            } },
            upsert: true
          }
        };
      });

      if (prodWrites.length) await Product.bulkWrite(prodWrites, { ordered: false });
      if (rentWrites.length) await RentalItem.bulkWrite(rentWrites, { ordered: false });
      if (orderWrites.length) await Order.bulkWrite(orderWrites, { ordered: false });
      if (custWrites.length) await Customer.bulkWrite(custWrites, { ordered: false });
      if (rentalWrites.length) await Rental.bulkWrite(rentalWrites, { ordered: false });
      const dbSummary = {
        dbCounts: {
          products: await Product.countDocuments({}),
          rentalItems: await RentalItem.countDocuments({}),
          orders: await Order.countDocuments({}),
          customers: await Customer.countDocuments({}),
          rentals: await Rental.countDocuments({})
        }
      };
      console.log('Commit completed');
      console.log(JSON.stringify(dbSummary, null, 2));
      await mongoose.disconnect();
    }).catch(err => {
      console.error('Mongo connect failed:', err.message);
      process.exit(1);
    });
  }
}

main();
