const express = require('express');
const Rental = require('../models/rental');

const router = express.Router();

router.get('/', async (req, res, next) => {
  try {
    const limit = Math.min(parseInt(req.query.limit || '50', 10), 200);
    const skip = parseInt(req.query.skip || '0', 10);
    const status = req.query.status;
    const phone = req.query.phone;
    const itemId = req.query.itemId ? parseInt(req.query.itemId, 10) : null;
    const filter = {};
    if (status) filter.status = status;
    if (phone) filter.customerPhone = phone;
    if (!Number.isNaN(itemId) && itemId) filter.legacyRentalItemId = itemId;
    const items = await Rental.find(filter).sort({ updatedAt: -1 }).skip(skip).limit(limit).lean();
    const count = await Rental.countDocuments(filter);
    res.json({ items, count });
  } catch (e) {
    next(e);
  }
});

module.exports = router;
