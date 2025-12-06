const mongoose = require('mongoose');

const OrderItemSchema = new mongoose.Schema({
  legacyProductId: { type: Number, required: true },
  name: { type: String, required: true },
  qty: { type: Number, required: true, min: 0 },
  unitPriceCents: { type: Number, required: true, min: 0 }
}, { _id: false });

const TotalsSchema = new mongoose.Schema({
  subtotalCents: { type: Number, required: true, min: 0 },
  taxCents: { type: Number, required: true, min: 0 },
  discountCents: { type: Number, required: true, min: 0 },
  grandCents: { type: Number, required: true, min: 0 }
}, { _id: false });

const OrderSchema = new mongoose.Schema({
  orderKey: { type: String, unique: true, index: true },
  orderedAt: { type: Date, index: true },
  cashierUsername: { type: String },
  items: { type: [OrderItemSchema], default: [] },
  totals: { type: TotalsSchema, required: true },
  source: { type: String, default: 'legacy' }
}, { versionKey: false });

module.exports = mongoose.models.Order || mongoose.model('Order', OrderSchema);
