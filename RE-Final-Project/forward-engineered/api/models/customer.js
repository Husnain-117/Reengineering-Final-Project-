const mongoose = require('mongoose');

const CustomerSchema = new mongoose.Schema({
  phone: { type: String, unique: true, index: true }
}, { timestamps: true });

module.exports = mongoose.models.Customer || mongoose.model('Customer', CustomerSchema);
