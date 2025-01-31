// src/utils/logger.js
import winston from "winston";

// Configure the logger
const logger = winston.createLogger({
  level: "info",
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.printf(
      ({ level, message, timestamp }) =>
        `[${timestamp}] ${level.toUpperCase()}: ${message}`,
    ),
  ),
  transports: [
    new winston.transports.Console(), // Log to the console
    // Add a file transport if needed
    new winston.transports.File({ filename: "app.log" }),
  ],
});

export default logger;
