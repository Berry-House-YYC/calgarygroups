const fs = require("fs");
const path = require("path");

module.exports = function () {
  const filePath = path.resolve(__dirname, "..", "..", ".github", "FUNDING.yml");

  let raw = "";
  try {
    raw = fs.readFileSync(filePath, "utf8");
  } catch {
    return { raw: {}, supportLinks: [] };
  }

  const data = {};

  for (const line of raw.split(/\r?\n/)) {
    const trimmed = (line || "").trim();
    if (!trimmed || trimmed.startsWith("#")) continue;

    const match = trimmed.match(/^([A-Za-z0-9_]+):\s*(.*)$/);
    if (!match) continue;

    const key = match[1];
    let value = (match[2] || "").trim();

    if (!value) continue;

    value = value.split("#")[0].trim();
    value = value.replace(/^['"]|['"]$/g, "");

    if (value) data[key] = value;
  }

  const supportLinks = [];

  if (data.github) supportLinks.push({ label: "GitHub Sponsors", url: `https://github.com/sponsors/${data.github}` });
  if (data.patreon) supportLinks.push({ label: "Patreon", url: `https://www.patreon.com/${data.patreon}` });
  if (data.ko_fi) supportLinks.push({ label: "Ko-fi", url: `https://ko-fi.com/${data.ko_fi}` });
  if (data.buy_me_a_coffee) supportLinks.push({ label: "Buy Me a Coffee", url: `https://www.buymeacoffee.com/${data.buy_me_a_coffee}` });

  return { raw: data, supportLinks };
};
