const mongoose = require('mongoose');

const ProductSchema = new mongoose.Schema({
  legacyId: { type: Number, unique: true },
  name: String,
  salePriceCents: Number,
  stock: Number,
  isActive: Boolean
}, { timestamps: true });

module.exports = mongoose.models.Product || mongoose.model('Product', ProductSchema);
