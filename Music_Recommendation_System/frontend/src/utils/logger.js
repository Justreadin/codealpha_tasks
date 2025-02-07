/* eslint-disable prettier/prettier */

const logger = {
  info(message, ...optionalParams) {
    if (process.env.NODE_ENV !== "production") {
      console.info(`[INFO]: ${message}`, ...optionalParams);
    }
  },

  warn(message, ...optionalParams) {
    if (process.env.NODE_ENV !== "production") {
      console.warn(`[WARN]: ${message}`, ...optionalParams);
    }
  },

  error(message, ...optionalParams) {
    console.error(`[ERROR]: ${message}`, ...optionalParams);
  },

  debug(message, ...optionalParams) {
    if (process.env.NODE_ENV !== "production") {
      console.debug(`[DEBUG]: ${message}`, ...optionalParams);
    }
  },
};

export default logger;
