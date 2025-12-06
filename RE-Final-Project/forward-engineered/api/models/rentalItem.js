const mongoose = require('mongoose');

const RentalItemSchema = new mongoose.Schema({
  legacyId: { type: Number, unique: true },
  name: String,
  rentalPriceCents: Number,
  stock: Number,
  isActive: Boolean
}, { timestamps: true });

module.exports = mongoose.models.RentalItem || mongoose.model('RentalItem', RentalItemSchema);
