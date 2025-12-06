const mongoose = require('mongoose');

const RentalSchema = new mongoose.Schema({
  rentalKey: { type: String, unique: true, index: true },
  customerPhone: { type: String, required: true, index: true },
  legacyRentalItemId: { type: Number, required: true, index: true },
  rentedAt: { type: Date },
  returnedAt: { type: Date },
  legacyDateStr: { type: String },
  status: { type: String, enum: ['rented', 'returned'], required: true },
  source: { type: String, default: 'legacy' }
}, { timestamps: true });

module.exports = mongoose.models.Rental || mongoose.model('Rental', RentalSchema);
