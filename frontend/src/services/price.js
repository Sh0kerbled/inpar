export const formatNiceKztPrice = (value) => {
  const price = Math.round(Number(value) || 0);
  if (!price) return "0";

  const remainder = price % 100;
  if (remainder === 0) return String(price);
  if (remainder <= 50) return String(price - remainder + 99);
  return String(price - remainder + 100);
};

export const calculateKztFromUsd = (usdPrice, exchangeRate) => {
  const usd = Number(usdPrice || 0);
  const rate = Number(exchangeRate || 0);
  return usd * rate;
};

export const formatNiceKztFromUsd = (usdPrice, exchangeRate) => {
  const raw = calculateKztFromUsd(usdPrice, exchangeRate);
  return formatNiceKztPrice(raw);
};
