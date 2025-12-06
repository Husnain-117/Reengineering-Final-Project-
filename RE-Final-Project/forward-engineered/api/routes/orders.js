const express = require('express');
const Order = require('../models/order');

const router = express.Router();

router.get('/', async (req, res, next) => {
  try {
    const limit = Math.min(parseInt(req.query.limit || '50', 10), 200);
    const skip = parseInt(req.query.skip || '0', 10);
    const start = req.query.start ? new Date(req.query.start) : null;
    const end = req.query.end ? new Date(req.query.end) : null;
    const filter = {};
    if (start || end) {
      filter.orderedAt = {};
      if (start && !isNaN(start)) filter.orderedAt.$gte = start;
      if (end && !isNaN(end)) filter.orderedAt.$lte = end;
    }
    const items = await Order.find(filter).sort({ orderedAt: -1 }).skip(skip).limit(limit).lean();
    const count = await Order.countDocuments(filter);
    res.json({ items, count });
  } catch (e) {
    next(e);
  }
});

module.exports = router;
